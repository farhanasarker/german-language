"""E and F entries from pages 32-40+"""
import csv, os

CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv", "alphabetisch")

E_ENTRIES = [
    # === Page 32 Right (E start) ===
    ("eben", "", "", "adv", "just / exactly / flat", "এইমাত্র / ঠিক", "", "",
     "Ich bin eben erst angekommen.", "", ""),
    ("ebenfalls", "", "", "adv", "likewise / also", "একইভাবে / আরও", "", "",
     "Ich wünsche Ihnen ein schönes Wochenende. – Danke, ebenfalls.", "", ""),
    ("ebenso", "", "", "adv", "just as / likewise", "ঠিক তেমনই / একইরকম", "", "",
     "Schöne Feiertage. – Danke, ebenso.", "", ""),
    # === Page 33 Left ===
    ("e-card", "die", "", "noun", "e-card (health insurance, Austria)", "ই-কার্ড (স্বাস্থ্য বীমা, অস্ট্রিয়া)", "", "",
     "Haben Sie Ihre e-card dabei?", "A: e-card, D: Versichertenkarte", ""),
    ("echt", "", "", "adj", "real / genuine / really", "আসল / খাঁটি / সত্যিই", "", "",
     "Der Film war echt gut.", "", ""),
    ("ec-Karte", "die", "", "noun", "EC card / debit card", "ইসি কার্ড / ডেবিট কার্ড", "", "",
     "Sie können auch mit der ec-Karte zahlen.", "A: Bankomat-Karte", ""),
    ("Ecke", "die", "-n", "noun", "corner (Germany/Switzerland)", "কোণ (জার্মানি/সুইজারল্যান্ড)", "", "",
     "Das Regal stellen wir hier in die Ecke.", "D/CH: Ecke, A: Eck", ""),
    ("Eck", "das", "-en", "noun", "corner (Austria)", "কোণ (অস্ট্রিয়া)", "", "",
     "Das Regal stellen wir hier ins Eck.", "A: Eck, D/CH: Ecke", ""),
    ("eckig", "", "", "adj", "angular / square / cornered", "কৌণিক / চারকোণা", "", "",
     "Ich möchte einen eckigen Tisch, keinen runden.", "", ""),
    ("egal", "", "", "adj", "all the same / doesn't matter", "কিছু যায় আসে না / সমান", "", "",
     "Es ist mir ganz egal, was die Leute denken.", "", ""),
    ("Ehe", "die", "-n", "noun", "marriage", "বিবাহ / দাম্পত্য", "", "",
     "Sie hat zwei Kinder aus erster Ehe.", "", ""),
    ("Ehefrau", "die", "-en", "noun", "wife", "স্ত্রী", "", "",
     "Wie heißt Ihre Ehefrau mit Vornamen?", "", ""),
    ("Ehemann", "der", "¨-er", "noun", "husband", "স্বামী", "", "",
     "Wie heißt Ihr Ehemann mit Vornamen?", "", ""),
    ("Ehepaar", "das", "-e", "noun", "married couple", "বিবাহিত দম্পতি", "", "",
     "Das Ehepaar unter uns hat zwei Kinder.", "", ""),
    ("eher", "", "", "adv", "earlier / rather / sooner", "বরং / আগে / শীঘ্র", "", "",
     "Michael sieht gerne Serien, ich mag eher Krimis.", "", ""),
    ("ehrlich", "", "", "adj", "honest / honestly", "সৎ / সততার সাথে", "", "",
     "Sie ist ein ehrlicher Mensch.", "", ""),
    ("Ei", "das", "-er", "noun", "egg", "ডিম", "", "",
     "Möchtest du zum Frühstück ein Ei?", "", ""),
    ("eigen-", "", "", "adj", "own", "নিজস্ব / নিজের", "", "",
     "Fast jedes Kind hat ein eigenes Zimmer.", "", ""),
    ("eigentlich", "", "", "adv", "actually / really", "আসলে / প্রকৃতপক্ষে", "", "",
     "Wir wollten eigentlich Freunde besuchen, aber dann sind wir doch zu Hause geblieben.", "", ""),
    ("sich eignen", "", "", "verb", "to be suitable / suited", "উপযুক্ত হওয়া", "geeignet", "hat",
     "Dieses Hotel eignet sich besonders für Familien mit Kindern.", "", ""),
    # === Page 33 Right ===
    ("eilen", "", "", "verb", "to hurry / rush", "তাড়াতাড়ি করা", "geeilt", "hat/ist",
     "Es eilt sehr. Bitte machen Sie schnell.", "", ""),
    ("Eile", "die", "", "noun", "hurry / haste", "তাড়াতাড়ি / ত্বরা", "", "",
     "Ich bin sehr in Eile.", "", ""),
    ("eilig", "", "", "adj", "hurried / in a hurry", "তাড়াহুড়ো / ব্যস্ত", "", "",
     "Hast du es eilig?", "", ""),
    ("ein-", "", "", "numeral", "one / a / an", "এক / একটি", "", "",
     "Ich nehme ein Bier. Willst du auch eins?", "", ""),
    ("Einbahnstraße", "die", "-n", "noun", "one-way street", "একমুখী রাস্তা", "", "",
     "Die Goethestraße ist jetzt eine Einbahnstraße.", "", ""),
    ("einbrechen", "", "", "verb", "to break in / burgle", "সিঁধ কাটা / চুরি করা", "eingebrochen", "ist",
     "Jemand ist in unsere Wohnung eingebrochen.", "", ""),
    ("Einbrecher", "der", "-", "noun", "burglar (male)", "চোর / সিঁধেল চোর (পুরুষ)", "", "",
     "Die Einbrecher haben nichts gestohlen.", "", ""),
    ("Einbrecherin", "die", "-nen", "noun", "burglar (female)", "চোর / সিঁধেল চোর (মহিলা)", "", "",
     "Die Einbrecherin wurde von der Polizei gefasst.", "", ""),
    ("Einbruch", "der", "¨-e", "noun", "break-in / burglary", "সিঁধেল চুরি / ডাকাতি", "", "",
     "In der Urlaubszeit gibt es viele Wohnungseinbrüche.", "", ""),
    ("eindeutig", "", "", "adj", "clear / unambiguous", "সুস্পষ্ট / দ্ব্যর্থহীন", "", "",
     "Das Ergebnis ist eindeutig. Du hast gewonnen.", "", ""),
    ("Eindruck", "der", "¨-e", "noun", "impression", "প্রভাব / ছাপ", "", "",
     "Ich glaube, ich habe bei dem Vorstellungsgespräch einen guten Eindruck gemacht.", "", ""),
    ("einerseits", "", "", "adv", "on the one hand", "একদিকে / একপক্ষে", "", "",
     "Einerseits möchte ich die Reise gern machen, andererseits ist sie zu teuer.", "", ""),
    ("einfach", "", "", "adj", "simple / easy / just", "সহজ / সরল / শুধু", "", "",
     "Hin und zurück? – Nein, bitte nur einfach.", "", ""),
    ("Einfahrt", "die", "-en", "noun", "driveway / entrance", "প্রবেশ পথ / ড্রাইভওয়ে", "", "",
     "Da parkt wieder jemand vor unserer Einfahrt.", "", ""),
    ("einfallen", "", "", "verb", "to occur / come to mind", "মনে পড়া / হঠাৎ মনে আসা", "eingefallen", "ist",
     "Mir ist wieder eingefallen, wie das Buch heißt.", "", ""),
    ("Einfall", "der", "¨-e", "noun", "idea / sudden thought", "আইডিয়া / হঠাৎ চিন্তা", "", "",
     "Frag einfach meine Freundin. Sie hat immer gute Einfälle.", "", ""),
    ("Einfluss", "der", "¨-e", "noun", "influence", "প্রভাব", "", "",
     "Das Wetter hat Einfluss auf die Gesundheit der Menschen.", "", ""),
]

F_ENTRIES = [
    # We'll add F entries shortly - need to read more pages
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
    write_entries("E.csv", E_ENTRIES)
    if F_ENTRIES:
        write_entries("F.csv", F_ENTRIES)
