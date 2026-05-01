"""
Parse extracted PDF text into CSV entries.
Uses the text output from extract_pdf.py (left/right column reconstruction).
Processes all remaining pages and generates per-letter CSV files.
"""
import re, csv, os, sys

CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv", "alphabetisch")

# ── Translation database ──────────────────────────────────────────────
# (english, bangla) for each headword
TR = {}

def add(word, english, bangla):
    TR[word] = (english, bangla)

# ── D ──
add("Detail", "detail", "বিস্তারিত")
add("deutlich", "clear / distinct", "স্পষ্ট")
add("Diät", "diet", "খাদ্য নিয়ন্ত্রণ")
add("Dialekt", "dialect", "উপভাষা")
add("Dialog", "dialogue", "সংলাপ")
add("dicht", "tight / sealed", "ঘন / আঁটসাঁট")
add("dick", "thick / fat", "মোটা / স্থূল")
add("Dieb", "thief", "চোর")
add("dienen", "to serve", "সেবা করা")
add("Dienst", "service / duty / shift", "সেবা / ডিউটি")
add("dies-", "this / these", "এই / এগুলি")
add("diesmal", "this time", "এবার")
add("digital", "digital", "ডিজিটাল")
add("Ding", "thing", "জিনিস / বস্তু")
add("Diplom", "diploma / degree", "ডিপ্লোমা / সনদ")
add("direkt", "direct / directly", "সরাসরি")
add("Direktor", "director (male)", "পরিচালক (পুরুষ)")
add("Direktorin", "director (female)", "পরিচালক (মহিলা)")
add("Diskothek", "discotheque / club", "ডিস্কো / নাইটক্লাব")
add("diskutieren", "to discuss", "আলোচনা করা")
add("Diskussion", "discussion", "আলোচনা / বিতর্ক")
add("Distanz", "distance", "দূরত্ব")
add("doch", "yes / but / after all", "হ্যাঁ (বিরোধে) / কিন্তু")
add("Doktor", "doctor (male)", "ডাক্তার (পুরুষ)")
add("Doktorin", "doctor (female)", "ডাক্তার (মহিলা)")
add("Dokument", "document", "নথি / দলিল")
add("donnern", "to thunder / roar", "বজ্রপাত হওয়া")
add("Donner", "thunder", "বজ্রধ্বনি")
add("doppelt", "double", "দ্বিগুণ / ডাবল")
add("Doppel-", "double- / twin-", "দ্বি- / যমজ-")
add("Dorf", "village", "গ্রাম")
add("dort", "there", "সেখানে")
add("dorthin", "to there / thither", "সেদিকে")
add("Dose", "can / tin", "কৌটা / টিন")
add("draußen", "outside", "বাইরে")
add("Dreck", "dirt / filth", "ময়লা")
add("drehen", "to turn / rotate", "ঘোরানো")
add("dringend", "urgent / urgently", "জরুরি")
add("drin", "inside / in there", "ভিতরে")
add("drinnen", "inside / indoors", "ভিতরে / ঘরের ভিতরে")
add("Droge", "drug", "মাদক / ড্রাগ")
add("Drogerie", "drugstore", "প্রসাধনী দোকান")
add("drüben", "over there", "ওপারে / ওদিকে")
add("drucken", "to print", "প্রিন্ট করা")
add("Drucker", "printer", "প্রিন্টার")
add("drücken", "to press / push", "চাপ দেওয়া")
add("Druck", "pressure / print", "চাপ / মুদ্রণ")
add("dumm", "stupid / silly", "বোকা")
add("dunkel", "dark", "অন্ধকার / গাঢ়")
add("dünn", "thin", "পাতলা")
add("durch", "through / by", "মধ্য দিয়ে / দ্বারা")
add("durcheinander", "mixed up / confused", "বিশৃঙ্খল / গোলমেলে")
add("Durchsage", "announcement (loudspeaker)", "লাউডস্পিকার ঘোষণা")
add("Durchschnitt", "average", "গড়")
add("durchschnittlich", "on average / average (adj)", "গড়ে / গড়পড়তা")
add("dürfen", "to be allowed to / may", "অনুমতি থাকা")
add("Durst", "thirst", "তৃষ্ণা / পিপাসা")
add("durstig", "thirsty", "তৃষ্ণার্ত")
add("sich duschen", "to shower (oneself)", "গোসল করা (শাওয়ার)")
add("duschen", "to shower", "গোসল করা (শাওয়ার)")
add("Dusche", "shower (fixture)", "শাওয়ার")
add("duzen", "to address with 'du'", "তুমি বলে ডাকা")

# ── E ──
add("eben", "just / exactly / flat", "এইমাত্র / ঠিক")
add("ebenfalls", "likewise / also", "একইভাবে")
add("ebenso", "just as / likewise", "ঠিক তেমনই")
add("e-card", "e-card (insurance, Austria)", "ই-কার্ড (অস্ট্রিয়া)")
add("echt", "real / genuine / really", "আসল / খাঁটি")
add("ec-Karte", "EC card / debit card", "ইসি কার্ড")
add("EC-Karte", "EC card / debit card", "ইসি কার্ড")
add("Ecke", "corner (Germany/Switzerland)", "কোণ")
add("Eck", "corner (Austria)", "কোণ (অস্ট্রিয়া)")
add("eckig", "angular / square", "কৌণিক")
add("egal", "all the same / doesn't matter", "কিছু যায় আসে না")
add("Ehe", "marriage", "বিবাহ")
add("Ehefrau", "wife", "স্ত্রী")
add("Ehemann", "husband", "স্বামী")
add("Ehepaar", "married couple", "বিবাহিত দম্পতি")
add("eher", "earlier / rather / sooner", "বরং / আগে")
add("ehrlich", "honest / honestly", "সৎ")
add("Ei", "egg", "ডিম")
add("eigen-", "own", "নিজস্ব")
add("eigentlich", "actually / really", "আসলে")
add("sich eignen", "to be suitable", "উপযুক্ত হওয়া")
add("eilen", "to hurry / rush", "তাড়াতাড়ি করা")
add("Eile", "hurry / haste", "তাড়াতাড়ি / ত্বরা")
add("eilig", "hurried / in a hurry", "তাড়াহুড়ো")
add("ein-", "one / a / an", "এক / একটি")
add("Einbahnstraße", "one-way street", "একমুখী রাস্তা")
add("einbrechen", "to break in / burgle", "সিঁধ কাটা")
add("Einbrecher", "burglar (male)", "চোর (পুরুষ)")
add("Einbrecherin", "burglar (female)", "চোর (মহিলা)")
add("Einbruch", "break-in / burglary", "সিঁধেল চুরি")
add("eindeutig", "clear / unambiguous", "সুস্পষ্ট")
add("Eindruck", "impression", "প্রভাব / ছাপ")
add("einerseits", "on the one hand", "একদিকে")
add("einfach", "simple / easy / just", "সহজ / সরল")
add("Einfahrt", "driveway / entrance", "প্রবেশ পথ")
add("einfallen", "to occur / come to mind", "মনে পড়া")
add("Einfall", "idea / sudden thought", "মাথায় আসা চিন্তা")
add("Einfluss", "influence", "প্রভাব")
add("beeinflussen", "to influence", "প্রভাবিত করা")
add("einfügen", "to insert / paste", "সন্নিবেশ করা")
add("einführen", "to introduce / import", "প্রবর্তন / আমদানি করা")
add("Einführung", "introduction", "ভূমিকা / প্রবর্তন")
add("Eingang", "entrance", "প্রবেশদ্বার")
add("einheitlich", "uniform / standardized", "অভিন্ন")
add("einig-", "some / a few / agreed", "কিছু / একমত")
add("sich einigen", "to agree / reach agreement", "একমত হওয়া")
add("einkaufen", "to shop", "কেনাকাটা করা")
add("Einkauf", "purchase / shopping", "কেনাকাটা")
add("Einkommen", "income", "আয়")
add("einladen", "to invite", "আমন্ত্রণ জানানো")
add("Einladung", "invitation", "আমন্ত্রণ")
add("einmal", "once / one time", "একবার")
add("einnehmen", "to take (medicine) / earn", "গ্রহণ করা / আয় করা")
add("Einnahme", "revenue / income", "রাজস্ব / আয়")
add("einpacken", "to pack / wrap up", "প্যাক করা")
add("einrichten", "to furnish / set up", "সাজানো / স্থাপন করা")
add("Einrichtung", "furnishings / facility", "আসবাবপত্র / প্রতিষ্ঠান")
add("einsam", "lonely / solitary", "একাকী / নিঃসঙ্গ")
add("einschalten", "to switch on / turn on", "চালু করা")
add("einschließlich", "including / inclusive", "সহ / সমেত")
add("Einschreiben", "registered mail", "রেজিস্টার্ড ডাক")
add("einsetzen", "to insert / appoint / employ", "নিয়োগ করা / ব্যবহার করা")
add("einsteigen", "to get in / board", "উঠা (গাড়িতে)")
add("einstellen", "to hire / adjust / set", "নিয়োগ / সমন্বয় করা")
add("eintragen", "to enter / register", "লিখে রাখা / নিবন্ধন")
add("eintreten", "to enter / join", "প্রবেশ করা / যোগদান")
add("Eintritt", "admission / entry", "প্রবেশ / প্রবেশ মূল্য")
add("einverstanden", "agreed / okay", "একমত / সম্মত")
add("Einwohner", "inhabitant (male)", "বাসিন্দা (পুরুষ)")
add("Einwohnerin", "inhabitant (female)", "বাসিন্দা (মহিলা)")
add("einzahlen", "to deposit (money)", "জমা করা")
add("Einzahlung", "deposit / payment", "জমা")
add("einzeln", "single / individual", "একক / আলাদা")
add("Einzel-", "single / individual", "একক")
add("Einzelheit", "detail", "বিস্তারিত")
add("einzig-", "only / sole / unique", "একমাত্র / অনন্য")
add("einziehen", "to move in / collect", "স্থানান্তর / সংগ্রহ")
add("Eis", "ice / ice cream", "বরফ / আইসক্রিম")
add("Eisenbahn", "railway / train", "রেলপথ")
add("elegant", "elegant", "অভিজাত / মার্জিত")
add("elektrisch", "electric / electrical", "বৈদ্যুতিক")
add("Elektro-", "electro- / electric", "ইলেকট্রো-")
add("elektronisch", "electronic", "ইলেকট্রনিক")
add("Eltern", "parents (pl.)", "মা-বাবা")
add("empfangen", "to receive", "গ্রহণ করা")
add("Empfang", "reception / receipt", "অভ্যর্থনা / প্রাপ্তি")
add("Empfänger", "recipient / receiver", "প্রাপক")
add("empfehlen", "to recommend", "সুপারিশ করা")
add("Empfehlung", "recommendation", "সুপারিশ")
add("enden", "to end / finish", "শেষ হওয়া")
add("Ende", "end", "শেষ / সমাপ্তি")
add("endgültig", "final / definitive", "চূড়ান্ত")
add("endlich", "finally / at last", "অবশেষে")
add("Energie", "energy", "শক্তি")
add("eng", "narrow / tight / close", "সংকীর্ণ / ঘনিষ্ঠ")
add("Enkel", "grandson", "নাতি (পুরুষ)")
add("Enkelin", "granddaughter", "নাতনি (মহিলা)")
add("entdecken", "to discover", "আবিষ্কার করা")
add("entfernen", "to remove / delete", "অপসারণ করা")
add("Entfernung", "distance / removal", "দূরত্ব")
add("entgegenkommen", "to come towards / accommodate", "ছাড় দেওয়া")
add("enthalten", "to contain", "ধারণ করা")
add("entlang", "along", "বরাবর / ধরে")
add("entlassen", "to dismiss / discharge", "বরখাস্ত করা")
add("Entlassung", "dismissal / discharge", "বরখাস্ত")
add("entscheiden", "to decide", "সিদ্ধান্ত নেওয়া")
add("Entscheidung", "decision", "সিদ্ধান্ত")
add("unentschieden", "undecided / tied", "অনিশ্চিত")
add("sich entschließen", "to decide / resolve", "সিদ্ধান্ত নেওয়া")
add("entschlossen", "determined / resolute", "দৃঢ়প্রতিজ্ঞ")
add("entschuldigen", "to excuse / apologize", "ক্ষমা করা")
add("Entschuldigung", "apology / excuse me", "ক্ষমা / দুঃখিত")
add("entsorgen", "to dispose of", "নিষ্পত্তি করা")
add("entspannend", "relaxing", "আরামদায়ক")
add("entstehen", "to arise / originate", "সৃষ্টি হওয়া")
add("enttäuschen", "to disappoint", "হতাশ করা")
add("Enttäuschung", "disappointment", "হতাশা")
add("entweder ... oder", "either ... or", "হয় ... অথবা")
add("entwickeln", "to develop", "উন্নয়ন করা")
add("Entwicklung", "development", "উন্নয়ন")
add("Erde", "earth / ground / soil", "পৃথিবী / মাটি")
add("Erdapfel", "potato (Austria)", "আলু (অস্ট্রিয়া)")
add("Erdgeschoss", "ground floor", "নিচতলা")
add("Ergeschoß", "ground floor (Austria)", "নিচতলা (অস্ট্রিয়া)")
add("Ereignis", "event / occurrence", "ঘটনা")
add("sich ereignen", "to happen / occur", "ঘটা")
add("erfahren", "to learn / find out", "জানা / শিখা")
add("Erfahrung", "experience", "অভিজ্ঞতা")
add("erfinden", "to invent", "উদ্ভাবন করা")
add("Erfindung", "invention", "উদ্ভাবন")

print(f"Translation database has {len(TR)} entries")

# Now parse the extracted text for pages 31-104
def parse_line_to_entry(line, next_lines, col_name):
    """Try to parse a line as a word entry. Returns (entry_dict, lines_consumed) or (None, 0)."""
    text = line.strip()
    if not text or len(text) < 2:
        return None, 0

    # Skip header/footer lines
    skip_patterns = ['WORTLISTE', 'ZERTIFIKAT B1', '30_SV', '---']
    if any(text.startswith(s) for s in skip_patterns):
        return None, 0
    if re.match(r'^\d{1,3}\s*$', text):
        return None, 0

    # Noun: starts with der/die/das
    noun_match = re.match(r'^(der|die|das)\s+(\S+?),?\s*(.+)?$', text)
    if noun_match:
        article = noun_match.group(1)
        word = noun_match.group(2).rstrip(',')
        rest = noun_match.group(3) or ""
        plural = ""
        sentence = ""

        # Parse rest - it could be plural or the start of a sentence
        if rest:
            # Check if rest looks like a plural form
            plural_match = re.match(r'^([¨\-\w\s/]+?)(?:\s+\d+\.\s+.+)?$', rest)
            if plural_match:
                plural_candidate = plural_match.group(1).strip().rstrip(',')
                # Only use as plural if short
                if len(plural_candidate) < 20 and not re.match(r'^\d', plural_candidate):
                    plural = plural_candidate
                    sent_match = re.search(r'\d+\.\s+(.+)', rest)
                    if sent_match:
                        sentence = sent_match.group(0)
                else:
                    sentence = rest

        # Check next lines for sentences
        consumed = 1
        if not sentence:
            for j, nl in enumerate(next_lines[:5]):
                nl = nl.strip()
                if re.match(r'^\d+\.', nl):
                    sentence = nl
                    consumed = 1 + j + 1
                    break

        return {
            "word": word, "article": article, "plural": plural,
            "wordType": "noun", "english": "", "bangla": "",
            "partizipII": "", "auxiliary": "",
            "exampleSentence": sentence or "",
            "synonyms": "", "antonyms": ""
        }, consumed

    # Verb: pattern like "word, form, form," or "sich word, form,"
    verb_match = re.match(r'^((?:sich\s+)?[a-zäöüß]+(?:en|n)),\s*(.+)$', text)
    if verb_match:
        word = verb_match.group(1)
        rest = verb_match.group(2)

        # Look in next lines for participle
        partizip = ""
        auxiliary = ""
        sentence = ""
        consumed = 1

        for j, nl in enumerate(next_lines[:5]):
            nl = nl.strip()
            # Check for "hat/ist participle"
            pp_match = re.match(r'(hat|ist)\s+([a-zäöüß]+(?:en|t))', nl)
            if pp_match:
                auxiliary = pp_match.group(1)
                partizip = pp_match.group(2)
                consumed = max(consumed, 1 + j + 1)
            # Check for sentence
            sent_match = re.match(r'^\d+\.\s+(.+)', nl)
            if sent_match:
                sentence = nl
                consumed = max(consumed, 1 + j + 1)

        return {
            "word": word, "article": "", "plural": "",
            "wordType": "verb", "english": "", "bangla": "",
            "partizipII": partizip, "auxiliary": auxiliary,
            "exampleSentence": sentence or "",
            "synonyms": "", "antonyms": ""
        }, consumed

    # Adjective / Adverb / Preposition / etc.
    word_match = re.match(r'^([A-ZÄÖÜa-zäöüß][^\d,]*?)(?:\s+\d+\.|\s*$)', text)
    if word_match:
        word = word_match.group(1).strip().rstrip(',').rstrip(';')
        if len(word) < 2:
            return None, 0

        # Determine type
        wordType = "unknown"
        if word.endswith('lich') or word.endswith('ig') or word.endswith('los') or word.endswith('bar'):
            wordType = "adj"
        elif word.endswith('weise') or word.endswith('hin') or word.endswith('her') or word.endswith('mals'):
            wordType = "adv"

        # Check next lines for sentence
        sentence = ""
        consumed = 1
        for j, nl in enumerate(next_lines[:3]):
            nl = nl.strip()
            if re.match(r'^\d+\.', nl):
                sentence = nl
                consumed = 1 + j + 1
                break

        return {
            "word": word, "article": "", "plural": "",
            "wordType": wordType, "english": "", "bangla": "",
            "partizipII": "", "auxiliary": "",
            "exampleSentence": sentence or "",
            "synonyms": "", "antonyms": ""
        }, consumed

    return None, 0


def process_extracted_pages(filepath, start_page, end_page):
    """Process pages from the extracted text file."""
    with open(filepath, 'r') as f:
        content = f.read()

    all_entries = []
    lines = content.split('\n')

    # Find the page range
    in_range = False
    current_page = 0
    current_column = None
    column_lines = []

    for line in lines:
        # Detect page boundaries
        page_match = re.match(r'^PAGE\s+(\d+)', line)
        if page_match:
            page_num = int(page_match.group(1))
            if current_column and column_lines and in_range:
                # Process the previous column
                entries = process_column_lines(column_lines, current_column, current_page)
                all_entries.extend(entries)

            current_page = page_num
            in_range = (start_page <= page_num <= end_page)
            current_column = None
            column_lines = []
            continue

        if not in_range:
            continue

        if line.startswith('--- LEFT COLUMN ---'):
            if current_column and column_lines:
                entries = process_column_lines(column_lines, current_column, current_page)
                all_entries.extend(entries)
            current_column = 'left'
            column_lines = []
        elif line.startswith('--- RIGHT COLUMN ---'):
            if current_column and column_lines:
                entries = process_column_lines(column_lines, current_column, current_page)
                all_entries.extend(entries)
            current_column = 'right'
            column_lines = []
        elif current_column and line.strip():
            column_lines.append(line.strip())

    # Process final column
    if current_column and column_lines and in_range:
        entries = process_column_lines(column_lines, current_column, current_page)
        all_entries.extend(entries)

    return all_entries


def process_column_lines(lines, column, page):
    """Parse a list of text lines into word entries."""
    entries = []
    i = 0
    while i < len(lines):
        entry, consumed = parse_line_to_entry(lines[i], lines[i+1:i+10], column)
        if entry:
            entry['page'] = page
            entry['column'] = column
            entries.append(entry)
            i += consumed
        else:
            i += 1
    return entries


def get_letter(word):
    w = word.strip()
    if w.startswith("sich "):
        w = w[5:]
    if w.startswith("ein "):
        w = w[4:]
    return w[0].upper()


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "/tmp/pages_31_104.txt"
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 31
    end = int(sys.argv[3]) if len(sys.argv) > 3 else 104

    entries = process_extracted_pages(filepath, start, end)
    print(f"Parsed {len(entries)} entries from pages {start}-{end}")

    # Add translations
    translated = 0
    for e in entries:
        word = e['word']
        if word in TR:
            e['english'], e['bangla'] = TR[word]
            translated += 1
            # Auto-detect word type from translation info
            if e['wordType'] == 'unknown':
                if e['article']:
                    e['wordType'] = 'noun'
                elif e['partizipII']:
                    e['wordType'] = 'verb'

    print(f"Translated: {translated}/{len(entries)}")

    # Group by letter
    groups = {}
    for e in entries:
        letter = get_letter(e['word'])
        groups.setdefault(letter, []).append(e)

    print(f"Letters: {sorted(groups.keys())}")

    # Show sample
    for letter in sorted(groups.keys())[:4]:
        group = groups[letter]
        print(f"\n  {letter}: {len(group)} entries")
        for e in group[:5]:
            print(f"    {e['word']} ({e['wordType']}) - {e['english'][:40] if e['english'] else 'NO TRANS'}")

    # Show untranslated
    missing = [e for e in entries if not e['english']]
    if missing:
        print(f"\n  UNTRANSLATED ({len(missing)}):")
        for e in missing[:30]:
            print(f"    {e['word']} ({e['wordType']}) page {e['page']} {e['column']}")
