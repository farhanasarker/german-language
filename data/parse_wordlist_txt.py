"""
Parse 'all word.txt' (text extracted from the Goethe B1 Wortliste PDF).

The PDF has a two-column layout. When pasted as text, word entries and example
sentences become interleaved. This script:
1. Extracts all word entries with grammatical info (article, plural, word type,
   partizip II, auxiliary)
2. Extracts example sentences and attempts best-effort pairing
3. Merges with existing CSVs (preserving English/Bangla translations)
4. Outputs a combined CSV with all words

Output: csv/alphabetisch_full.csv (complete word list from the PDF)
"""

import re
import csv
from pathlib import Path

ROOT = Path(__file__).parent.parent
INPUT_FILE = ROOT / "all word.txt"
OUTPUT_FILE = ROOT / "csv" / "alphabetisch_full.csv"

# Lines to skip (headers, footers, page markers)
SKIP_RE = re.compile(
    r'^(VS_03|WORTLISTE|ZERTIFIKAT B1|WORTSCHATZ|INHALT|VORWORT|\d+\s*$|'
    r'\d+\s+WORT|\d+\s+ZERTIFIKAT|WORT.*\d+$)'
)


def clean_lines(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if SKIP_RE.match(stripped):
            continue
        lines.append(stripped)
    return lines


def is_entry_line(line: str) -> dict | None:
    """
    Try to parse a line as a word entry. Returns parsed dict or None.

    Entry patterns:
    - "der/die/das Word, -plural"
    - "verb, conjugates, conjugated, hat/ist partizip"
    - "sich verb, ..."
    - "adjective" (single lowercase word)
    - "word, -en" (noun without article sometimes)
    """

    # Skip obvious sentences
    if re.match(r'^\d+\.\s', line):
        return None

    # Skip if line is too long and ends with sentence punctuation (likely a sentence)
    if len(line) > 80 and line[-1] in '.!?':
        return None

    result = {
        'word': '', 'article': '', 'plural': '', 'wordType': '',
        'partizipII': '', 'auxiliary': '',
    }

    # Pattern 1: Noun with article and plural
    # "die Abbildung, -en" or "der Abfall, ¨-e" or "das Amt, ¨-er"
    m = re.match(
        r'^(der|die|das|der/die|die/das|der/das)\s+'
        r'([A-ZÄÖÜ][\w\s()-]+?),\s*'
        r'([¨""\-\w/()e]+)\s*$',
        line
    )
    if m:
        result['article'] = m.group(1)
        result['word'] = m.group(2).strip()
        result['plural'] = m.group(3).strip()
        result['wordType'] = 'noun'
        return result

    # Pattern 1b: Noun with article, no plural
    # "die Angst" "das Internet"
    m = re.match(
        r'^(der|die|das|der/die|die/das|der/das)\s+'
        r'([A-ZÄÖÜ][\w()-]+)\s*$',
        line
    )
    if m:
        result['article'] = m.group(1)
        result['word'] = m.group(2).strip()
        result['wordType'] = 'noun'
        return result

    # Pattern 2: Verb with full conjugation
    # "abbiegen, biegt ab, bog ab, ist abgebogen"
    # "anfangen, fängt an, fing an, hat angefangen"
    m = re.match(
        r'^([\w()\s/]+?),\s+[\w\s]+,\s*[\w\s]+,\s*'
        r'(hat|ist|hat/ist|ist/hat)\s+([\wäöüß]+)\s*$',
        line
    )
    if m:
        result['word'] = m.group(1).strip()
        result['auxiliary'] = m.group(2)
        result['partizipII'] = m.group(3)
        result['wordType'] = 'verb'
        return result

    # Pattern 2b: Verb with partial conjugation on one line
    # "achten, achtet, achtete, hat geachtet (auf)"
    m = re.match(
        r'^([\w()\s/]+?),\s+\w+,\s*\w+,\s*'
        r'(hat|ist|hat/ist|ist/hat)\s+([\wäöüß]+)',
        line
    )
    if m and len(line) < 80:
        result['word'] = m.group(1).strip()
        result['auxiliary'] = m.group(2)
        result['partizipII'] = m.group(3)
        result['wordType'] = 'verb'
        return result

    # Pattern 2c: Multi-line verb (first line only, e.g., "abbiegen, biegt ab,")
    m = re.match(
        r'^([a-zäöüß][\w\s()]*?),\s+[\wäöüß]+(?:\s+\w+)?,\s*$',
        line
    )
    if m and len(line) < 50:
        result['word'] = m.group(1).strip()
        result['wordType'] = 'verb'
        return result

    # Pattern 2d: Reflexive verb
    # "sich amüsieren, amüsiert sich, amüsierte sich, hat sich amüsiert"
    m = re.match(
        r'^(?:\(sich\)\s+|sich\s+)([\wäöüß]+)',
        line
    )
    if m and ('hat' in line or 'ist' in line or ',' in line):
        word = line.split(',')[0].strip()
        result['word'] = word
        result['wordType'] = 'verb'
        aux_m = re.search(r'(hat|ist)\s+(?:sich\s+)?([\wäöüß]+)\s*$', line)
        if aux_m:
            result['auxiliary'] = aux_m.group(1)
            result['partizipII'] = aux_m.group(2)
        return result

    # Pattern 3: Noun with article, plural, and cross-reference
    # "der Abwart, -e ... → D, A: Hausmeister"
    m = re.match(
        r'^(der|die|das|der/die|die/das|der/das)\s+'
        r'([A-ZÄÖÜ][\w()-]+?),\s*'
        r'([¨""\-\w/()]+)\s*'
        r'(?:\(.*?\))?\s*(?:→.*)?$',
        line
    )
    if m:
        result['article'] = m.group(1)
        result['word'] = m.group(2).strip()
        result['plural'] = m.group(3).strip()
        result['wordType'] = 'noun'
        return result

    # Pattern 4: Simple word entries (adjective, adverb, preposition, etc.)
    # Single word or hyphenated, all lowercase, short
    if re.match(r'^[a-zäöüß][\w-]*$', line) and len(line) < 30:
        result['word'] = line
        # Guess word type
        if line.endswith(('lich', 'ig', 'isch', 'bar', 'los', 'sam', 'haft', 'voll')):
            result['wordType'] = 'adj'
        return result

    # Pattern 5: Entry with cross-reference only
    # "das Abitur (D)→A, CH: Matura"
    m = re.match(
        r'^(der|die|das)\s+([A-ZÄÖÜ][\w-]+)\s*(?:\(.*?\))?\s*→',
        line
    )
    if m:
        result['article'] = m.group(1)
        result['word'] = m.group(2).strip()
        result['wordType'] = 'noun'
        return result

    # Pattern 6: Multi-word entries like "Bescheid sagen" or "Rad fahren"
    m = re.match(r'^([A-ZÄÖÜ][\wäöüß]+\s+[\wäöüß]+)\s*$', line)
    if m and len(line) < 30:
        result['word'] = m.group(1)
        return result

    return None


def is_sentence(line: str) -> bool:
    """Check if a line looks like an example sentence."""
    if re.match(r'^\d+\.\s', line):
        return True
    if len(line) > 30 and line[0].isupper() and line[-1] in '.!?':
        return True
    return False


def extract_all_entries(lines: list[str]) -> list[dict]:
    """Extract word entries from the alphabetical section."""
    # Find start of alphabetical section
    start = 0
    for i, line in enumerate(lines):
        if re.match(r'^2\s+Alphabetischer Wortschatz', line) or line == 'A':
            # Look for the actual start (letter A heading)
            for j in range(max(0, i-2), min(len(lines), i+5)):
                if lines[j].strip() == 'A':
                    start = j
                    break
            if start:
                break

    if not start:
        # Fallback: find first "ab" entry
        for i, line in enumerate(lines):
            if line.strip() == 'ab' and i > 100:
                start = i
                break

    entries = []
    current_entry = None
    sentences_for_current = []

    for i in range(start, len(lines)):
        line = lines[i]

        parsed = is_entry_line(line)
        if parsed and parsed['word']:
            # Save previous entry
            if current_entry:
                current_entry['exampleSentence'] = pick_best_sentence(sentences_for_current)
                entries.append(current_entry)

            current_entry = parsed
            sentences_for_current = []
        elif is_sentence(line):
            # Collect sentence
            sentence = re.sub(r'^\d+\.\s*', '', line).strip()
            if sentence:
                sentences_for_current.append(sentence)
        elif current_entry and line[0].isupper() and line[-1] in '.!?' and len(line) > 20:
            # Likely a sentence without number prefix
            sentences_for_current.append(line)

    # Last entry
    if current_entry:
        current_entry['exampleSentence'] = pick_best_sentence(sentences_for_current)
        entries.append(current_entry)

    return entries


def pick_best_sentence(sentences: list[str]) -> str:
    """Pick the first/best example sentence from collected sentences."""
    if not sentences:
        return ''
    # Return first sentence (most likely to be the primary example)
    # Limit length
    s = sentences[0]
    if len(s) > 200:
        s = s[:200]
    return s


def load_existing_csvs() -> dict[str, dict]:
    """Load all existing alphabetical CSVs into a lookup by word."""
    existing = {}
    alpha_dir = ROOT / "csv" / "alphabetisch"
    if alpha_dir.exists():
        for csv_file in sorted(alpha_dir.iterdir()):
            if csv_file.suffix == '.csv':
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        word = row.get('Word', '').strip()
                        if word:
                            existing[word.lower()] = row
    return existing


def merge_entries(new_entries: list[dict], existing: dict[str, dict]) -> list[dict]:
    """
    Merge new parsed entries with existing CSV data.
    Existing entries keep their English/Bangla translations.
    New entries fill gaps in the word list.
    """
    merged = {}

    # Start with existing entries (they have translations)
    for word_lower, row in existing.items():
        merged[word_lower] = {
            'word': row.get('Word', ''),
            'article': row.get('Article', ''),
            'plural': row.get('Plural', ''),
            'wordType': row.get('WordType', ''),
            'english': row.get('English', ''),
            'bangla': row.get('Bangla', ''),
            'partizipII': row.get('Partizip_II', ''),
            'auxiliary': row.get('Auxiliary', ''),
            'exampleSentence': row.get('Example_Sentence', ''),
            'synonyms': row.get('Synonyms', ''),
            'antonyms': row.get('Antonyms', ''),
        }

    # Add/update from new entries
    for entry in new_entries:
        word = entry.get('word', '').strip()
        if not word:
            continue
        if not is_valid_word(word):
            continue
        key = word.lower()

        if key in merged:
            # Update only missing fields
            for field in ['article', 'plural', 'wordType', 'partizipII', 'auxiliary', 'exampleSentence']:
                if entry.get(field) and not merged[key].get(field):
                    merged[key][field] = entry[field]
        else:
            # New entry
            merged[key] = {
                'word': word,
                'article': entry.get('article', ''),
                'plural': entry.get('plural', ''),
                'wordType': entry.get('wordType', ''),
                'english': '',
                'bangla': '',
                'partizipII': entry.get('partizipII', ''),
                'auxiliary': entry.get('auxiliary', ''),
                'exampleSentence': entry.get('exampleSentence', ''),
                'synonyms': '',
                'antonyms': '',
            }

    # Filter out invalid entries
    return [e for e in merged.values() if is_valid_word(e.get('word', ''))]


def is_valid_word(word: str) -> bool:
    """Filter out junk entries that aren't real dictionary words."""
    if not word or len(word) < 2:
        return False
    # Skip pure past participles (ge- prefix without being a real word entry)
    if word.startswith('ge') and word.endswith(('t', 'en')) and len(word) < 12:
        # Allow known "ge-" words
        known_ge = {'gehen', 'geben', 'gehören', 'gelingen', 'genießen', 'geraten',
                    'geschehen', 'gewinnen', 'gewöhnen', 'gelten', 'genügen', 'gefallen',
                    'gebrauchen', 'geduldig', 'gefährlich', 'gehorsam', 'gelb', 'gemein',
                    'gemischt', 'gemütlich', 'genau', 'gering', 'gern', 'gesamt', 'gesund',
                    'gewiss', 'geheim'}
        if word.lower() not in known_ge:
            return False
    # Skip fragments (very short words that aren't real German words)
    if len(word) <= 2 and word.lower() not in {'ab', 'an', 'um', 'ob'}:
        return False
    # Skip obvious fragments from hyphenated words split across lines
    if re.match(r'^[a-z]{2,6}$', word) and not word[-1].isalpha():
        return False
    # Skip entries that look like word fragments (no vowels, too short consonant clusters)
    vowels = set('aeiouäöü')
    if len(word) < 5 and not any(c in vowels for c in word.lower()):
        return False
    return True


def write_csv(entries: list[dict], output_path: Path):
    fieldnames = ['Word', 'Article', 'Plural', 'WordType', 'English', 'Bangla',
                  'Partizip_II', 'Auxiliary', 'Example_Sentence', 'Synonyms', 'Antonyms']

    entries.sort(key=lambda e: e.get('word', '').lower())

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for entry in entries:
            writer.writerow({
                'Word': entry.get('word', ''),
                'Article': entry.get('article', ''),
                'Plural': entry.get('plural', ''),
                'WordType': entry.get('wordType', ''),
                'English': entry.get('english', ''),
                'Bangla': entry.get('bangla', ''),
                'Partizip_II': entry.get('partizipII', ''),
                'Auxiliary': entry.get('auxiliary', ''),
                'Example_Sentence': entry.get('exampleSentence', ''),
                'Synonyms': entry.get('synonyms', ''),
                'Antonyms': entry.get('antonyms', ''),
            })


def main():
    print(f"Reading: {INPUT_FILE}")
    text = INPUT_FILE.read_text(encoding='utf-8')
    lines = clean_lines(text)
    print(f"Clean lines: {len(lines)}")

    new_entries = extract_all_entries(lines)
    print(f"Entries parsed from text: {len(new_entries)}")

    existing = load_existing_csvs()
    print(f"Existing entries in CSVs: {len(existing)}")

    merged = merge_entries(new_entries, existing)
    print(f"Merged total: {len(merged)}")

    write_csv(merged, OUTPUT_FILE)
    print(f"\nWritten to: {OUTPUT_FILE}")

    # Stats
    new_only = [e for e in merged if e.get('word', '').lower() not in existing]
    with_english = sum(1 for e in merged if e.get('english'))
    with_sentences = sum(1 for e in merged if e.get('exampleSentence'))
    nouns = sum(1 for e in merged if e.get('wordType') == 'noun')
    verbs = sum(1 for e in merged if e.get('wordType') == 'verb')

    print(f"\nNew words added: {len(new_only)}")
    print(f"With English translation: {with_english}")
    print(f"With example sentence: {with_sentences}")
    print(f"Nouns: {nouns}, Verbs: {verbs}")

    # Also update the per-letter CSV files with new words
    # Group by first letter
    # Map umlauts to base letters for file organization
    UMLAUT_MAP = {'Ä': 'A', 'Ö': 'O', 'Ü': 'U'}
    by_letter: dict[str, list[dict]] = {}
    for entry in merged:
        word = entry.get('word', '')
        if not word:
            continue
        letter = word[0].upper()
        if letter == '(':
            # Handle "(sich) verb" -> use second word
            parts = word.split()
            if len(parts) > 1:
                letter = parts[1][0].upper()
        if not letter.isalpha():
            continue
        letter = UMLAUT_MAP.get(letter, letter)
        by_letter.setdefault(letter, []).append(entry)

    # Write per-letter CSVs
    alpha_dir = ROOT / "csv" / "alphabetisch"
    alpha_dir.mkdir(parents=True, exist_ok=True)
    for letter, letter_entries in sorted(by_letter.items()):
        letter_file = alpha_dir / f"{letter}.csv"
        write_csv(letter_entries, letter_file)

    print(f"\nUpdated per-letter CSVs in {alpha_dir}")
    print(f"Letters: {', '.join(sorted(by_letter.keys()))}")
    for letter in sorted(by_letter.keys()):
        print(f"  {letter}: {len(by_letter[letter])} words")


if __name__ == '__main__':
    main()
