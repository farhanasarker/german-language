"""Q entries from page 72"""
import csv, os

CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv", "alphabetisch")

ENTRIES = [
    ("Qualifikation", "die", "-en", "noun", "qualification", "যোগ্যতা", "", "",
     "Für diesen Job braucht man eine gute Qualifikation.", "", ""),
    ("Qualität", "die", "-en", "noun", "quality", "গুণমান/গুণগত মান", "", "",
     "Die Qualität dieses Produkts ist ausgezeichnet.", "", ""),
    ("Quartier", "das", "-e", "noun", "quarter/district (CH)", "পাড়া/জেলা (সুইস)", "", "",
     "In welchem Quartier wohnst du?", "", ""),
    ("quer", "", "", "adj", "crosswise/diagonally", "আড়াআড়ি/তির্যকভাবে", "", "",
     "Wir gehen quer durch den Wald.", "", ""),
    ("Quittung", "die", "-en", "noun", "receipt", "রসিদ/প্রাপ্তি স্বীকার", "", "",
     "Bitte bewahren Sie die Quittung auf.", "", ""),
    ("Quiz", "das", "-", "noun", "quiz", "কুইজ/প্রশ্নোত্তর প্রতিযোগিতা", "", "",
     "Das Quiz im Fernsehen ist sehr beliebt.", "", ""),
]

def write_entries(filename, entries):
    filepath = os.path.join(CSV_DIR, filename)
    existing = []
    existing_words = set()
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                existing.append(row)
                existing_words.add(row[0])
    new_count = 0
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Article", "Plural", "WordType", "English", "Bangla",
                          "Partizip_II", "Auxiliary", "Example_Sentence", "Synonyms", "Antonyms"])
        for row in existing:
            writer.writerow(row)
        for e in entries:
            if e[0] not in existing_words:
                writer.writerow(e)
                new_count += 1
    print(f"{filename}: {len(existing)} existing + {new_count} new = {len(existing) + new_count} total")

if __name__ == "__main__":
    write_entries("Q.csv", ENTRIES)
