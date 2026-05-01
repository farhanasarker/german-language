"""
Convert CSV vocabulary files to JSON bundles for the flash card app.
Generates:
  - public/data/index.json (deck metadata)
  - public/data/<deck-id>.json (card arrays)
"""
import csv
import json
import os
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
CSV_DIR = ROOT / "csv"
OUT_DIR = ROOT / "public" / "data"

# Map each Wortgruppen section to appropriate tags
SECTION_TAGS = {
    "1.1_Abkuerzungen": "Funktion",
    "1.2_Anglizismen": "Medien",
    "1.3_Anweisungssprache": "Bildung",
    "1.4_Bildungseinrichtungen": "Bildung",
    "1.5_Schulfaecher": "Bildung",
    "1.6_Schulnoten": "Bildung",
    "1.7_Farben": "Natur",
    "1.8_Himmelsrichtungen": "Reisen,Natur",
    "1.9_Laender_Kontinente": "Reisen,Gesellschaft",
    "1.10_Politische_Begriffe": "Gesellschaft",
    "1.11_Tiere": "Natur",
    "1.12_Waehrungen_Masse_Gewichte": "Einkaufen",
    "1.13_Zahlen_Bruchzahlen": "Funktion",
    "1.14_Zeit": "Zeit",
}

# All valid tags for filtering
ALL_TAGS = [
    "Familie", "Essen", "Wohnen", "Arbeit", "Bildung",
    "Freizeit", "Reisen", "Gesundheit", "Einkaufen", "Medien",
    "Natur", "Gesellschaft", "Zeit", "Gefuehle", "Funktion",
]


def normalize_row(row: dict) -> dict:
    """Convert CSV row keys to lowercase and ensure all fields are strings."""
    key_map = {
        "ID": "id",
        "Word": "word",
        "Article": "article",
        "Plural": "plural",
        "WordType": "wordType",
        "English": "english",
        "Bangla": "bangla",
        "Partizip_II": "partizipII",
        "Auxiliary": "auxiliary",
        "Example_Sentence": "exampleSentence",
        "Synonyms": "synonyms",
        "Antonyms": "antonyms",
        "Tags": "tags",
    }
    normalized = {}
    for old_key, new_key in key_map.items():
        val = row.get(old_key, "")
        normalized[new_key] = (val or "").strip()
    return normalized


def read_csv(filepath: str) -> list[dict]:
    """Read a CSV file and return list of row dicts with normalized keys."""
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Skip empty rows
            if not r.get("Word", "").strip():
                continue
            rows.append(normalize_row(r))
    return rows


def generate_id(prefix: str, index: int) -> str:
    return f"{prefix}-{index:04d}"


def build_decks() -> dict:
    """Build all decks. Returns {deck_id: [cards], ...}"""
    decks: dict[str, list[dict]] = defaultdict(list)

    # Process Wortgruppen CSVs
    wortgruppen_dir = CSV_DIR / "wortgruppen"
    if wortgruppen_dir.exists():
        for csv_file in sorted(wortgruppen_dir.iterdir()):
            if not csv_file.suffix == ".csv":
                continue
            section_name = csv_file.stem  # e.g., "1.1_Abkuerzungen"
            rows = read_csv(str(csv_file))
            default_tags = SECTION_TAGS.get(section_name, "")

            for i, row in enumerate(rows):
                # Add ID if missing
                if not row.get("id", "").strip():
                    row["id"] = generate_id(section_name[:4], i)

                # Add tags if missing
                if not row.get("tags", "").strip():
                    row["tags"] = default_tags

                # Add to per-section deck
                deck_id = f"wg-{section_name.split('_', 1)[0].replace('.', '-')}"
                decks[deck_id].append(row)

                # Add to tag decks
                tags = [t.strip() for t in row["tags"].split(",") if t.strip()]
                for tag in tags:
                    decks[f"tag-{tag.lower()}"].append(row)

                # Add to word-type decks
                wt = row.get("wordType", "").strip().lower()
                if wt in ("noun", "verb", "adj", "adverb", "preposition", "numeral"):
                    decks[f"type-{wt}"].append(row)

                # Add to full deck
                decks["all"].append(row)

    # Process Alphabetical CSVs (if any exist)
    alpha_dir = CSV_DIR / "alphabetisch"
    if alpha_dir.exists():
        for csv_file in sorted(alpha_dir.iterdir()):
            if not csv_file.suffix == ".csv":
                continue
            letter = csv_file.stem  # e.g., "A", "B"
            rows = read_csv(str(csv_file))

            for i, row in enumerate(rows):
                if not row.get("id", "").strip():
                    row["id"] = generate_id(letter, i)

                # Add to per-letter deck
                decks[f"letter-{letter.lower()}"].append(row)

                # Add to tag decks
                tags = [t.strip() for t in row.get("tags", "").split(",") if t.strip()]
                for tag in tags:
                    decks[f"tag-{tag.lower()}"].append(row)

                # Add to word-type decks
                wt = row.get("wordType", "").strip().lower()
                if wt in ("noun", "verb", "adj", "adverb", "preposition", "numeral"):
                    decks[f"type-{wt}"].append(row)

                decks["all"].append(row)

    return decks


def write_output(decks: dict[str, list[dict]]):
    """Write all deck JSON files and index.json."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index_decks = []
    deck_ids = sorted(decks.keys())

    for deck_id in deck_ids:
        cards = decks[deck_id]
        filepath = OUT_DIR / f"{deck_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)

        # Build human-readable name
        name = deck_id_to_name(deck_id, cards)
        category = deck_id.split("-")[0]

        index_decks.append({
            "id": deck_id,
            "name": name,
            "description": "",
            "cardCount": len(cards),
            "category": category,
        })

    # Write index
    index = {
        "decks": index_decks,
        "generatedAt": "",
    }
    with open(OUT_DIR / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    total_cards = sum(len(decks[deck_id]) for deck_id in deck_ids)
    print(f"Generated {len(deck_ids)} decks with {total_cards} total cards")
    print(f"Output: {OUT_DIR}")


def deck_id_to_name(deck_id: str, cards: list[dict]) -> str:
    prefix = deck_id.split("-")[0]
    suffix = "-".join(deck_id.split("-")[1:])

    if prefix == "wg":
        return f"Wortgruppe: {suffix}"
    elif prefix == "letter":
        return f"Letter: {suffix.upper()}"
    elif prefix == "tag":
        return f"Topic: {suffix.capitalize()}"
    elif prefix == "type":
        return f"Type: {suffix.capitalize()}"
    elif deck_id == "all":
        return "All Words"
    return deck_id


def main():
    decks = build_decks()
    write_output(decks)


if __name__ == "__main__":
    main()
