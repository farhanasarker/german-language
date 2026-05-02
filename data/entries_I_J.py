"""I and J entries from pages 51-54"""
import csv, os

CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv", "alphabetisch")

I_ENTRIES = [
    # === Page 51 Left (I start) ===
    ("ideal", "", "", "adj", "ideal / perfect", "আদর্শ / নিখুঁত", "", "",
     "Eine Wohnung mit Garten wäre für uns ideal.", "", ""),
    ("Idee", "die", "-n", "noun", "idea", "ধারণা / আইডিয়া", "", "",
     "Du willst ein Picknick machen? Ich finde die Idee toll.", "", ""),
    ("illegal", "", "", "adj", "illegal", "অবৈধ", "", "",
     "Ohne Steuerkarte zu arbeiten ist illegal.", "", ""),
    ("Imbiss", "der", "-e", "noun", "snack / snack bar (Germany)", "জলখাবার / স্ন্যাক (জার্মানি)", "", "",
     "Es ist Zeit für einen kleinen Imbiss.", "D: Imbiss, A: Jause, CH: Znüni/Zvieri", ""),
    # === Page 51 Right ===
    ("immer", "", "", "adv", "always", "সবসময়", "", "",
     "Frau Bast kommt immer zu spät.", "", ""),
    ("Import", "der", "-e", "noun", "import", "আমদানি", "", "",
     "Im dritten Stock ist die Firma Schmidt & Co, Import und Export.", "", ""),
    ("in", "", "", "preposition", "in / to / at", "মধ্যে / ভিতরে / তে", "", "",
     "Ich wohne in Frankfurt.", "", ""),
    ("indem", "", "", "conjunction", "by (doing something)", "দ্বারা / করে", "", "",
     "Du kannst die Datei öffnen, indem du hier klickst.", "", ""),
    ("individuell", "", "", "adj", "individual / personalized", "ব্যক্তিগত / স্বতন্ত্র", "", "",
     "Die Lehrerin versucht, jedes Kind individuell zu fördern.", "", ""),
    ("Industrie", "die", "-n", "noun", "industry", "শিল্প", "", "",
     "In dieser Gegend gibt es viel Industrie.", "", ""),
    ("Infektion", "die", "-en", "noun", "infection", "সংক্রমণ / ইনফেকশন", "", "",
     "Sie haben eine Infektion. Sie müssen Tabletten nehmen.", "", ""),
    ("informieren", "", "", "verb", "to inform", "জানানো / তথ্য দেওয়া", "informiert", "hat",
     "Wir informieren Sie rechtzeitig über die neuen Prüfungstermine.", "", ""),
    ("Information", "die", "-en", "noun", "information", "তথ্য", "", "",
     "Bitte lesen Sie diese Informationen genau.", "", ""),
    ("Ingenieur", "der", "-e", "noun", "engineer", "প্রকৌশলী", "", "",
     "Hans will Bauingenieur werden.", "", ""),
    ("Inhalt", "der", "-e", "noun", "content / contents", "বিষয়বস্তু / ভিতরের জিনিস", "", "",
     "Geben Sie den Inhalt der Packung in einen Liter kochendes Wasser.", "", ""),
    ("inklusive", "", "", "preposition", "including / inclusive", "সহ / সমেত", "", "",
     "Der Zimmerpreis ist inklusive Frühstück.", "", ""),
    ("innen", "", "", "adv", "inside", "ভিতরে", "", "",
     "Der Lichtschalter ist innen links.", "", ""),
    ("inner-", "", "", "adj", "inner / internal", "অভ্যন্তরীণ", "", "",
     "Wir müssen Sie untersuchen. Es kann sein, dass Sie innere Verletzungen haben.", "", ""),
    ("innerhalb", "", "", "preposition", "within / inside of", "মধ্যে / ভিতরে", "", "",
     "Diese Fahrkarte gilt nur innerhalb der Stadt.", "", ""),
    # === Page 52 Left ===
    ("Insel", "die", "-n", "noun", "island", "দ্বীপ", "", "",
     "Ich würde dieses Mal gern auf einer Insel Ferien machen.", "", ""),
    ("Inserat", "das", "-e", "noun", "advertisement / ad", "বিজ্ঞাপন", "", "",
     "Was kostet ein Inserat in der Zeitung?", "", ""),
    ("insgesamt", "", "", "adv", "altogether / in total", "সর্বমোট / মোটে", "", "",
     "Insgesamt haben sich 20 Teilnehmer für die Prüfung angemeldet.", "", ""),
    ("installieren", "", "", "verb", "to install", "ইনস্টল করা", "installiert", "hat",
     "Können Sie mir helfen, meinen Computer zu installieren?", "", ""),
    ("Institut", "das", "-e", "noun", "institute", "প্রতিষ্ঠান / ইনস্টিটিউট", "", "",
     "Ich besuche einen Sprachkurs in einem kleinen Sprachinstitut.", "", ""),
    ("Instrument", "das", "-e", "noun", "instrument", "যন্ত্র / বাদ্যযন্ত্র", "", "",
     "Ich spiele Klavier. Spielen Sie auch ein Musikinstrument?", "", ""),
    ("integrieren", "", "", "verb", "to integrate", "একীভূত করা / সংহত করা", "integriert", "hat",
     "Sie ist schon sehr gut im Team integriert.", "", ""),
    ("Integration", "die", "-en", "noun", "integration", "একীভূতকরণ / সংহতি", "", "",
     "Gute Deutschkenntnisse sollen bei der Integration helfen.", "", ""),
    ("intelligent", "", "", "adj", "intelligent", "বুদ্ধিমান / মেধাবী", "", "",
     "Maria ist sehr intelligent. Sie kann sehr gut rechnen.", "", ""),
    ("Intelligenz", "die", "", "noun", "intelligence", "বুদ্ধিমত্তা", "", "",
     "Meine Kinder haben in der Schule einen Intelligenztest gemacht.", "", ""),
    ("intensiv", "", "", "adj", "intensive / intensely", "নিবিড় / গভীরভাবে", "", "",
     "Ich möchte intensiv Deutsch lernen.", "", ""),
    ("Intensivkurs", "der", "-e", "noun", "intensive course", "নিবিড় কোর্স", "", "",
     "Der Intensivkurs findet täglich von 9 bis 12 Uhr statt.", "", ""),
    ("interessieren", "", "", "verb", "to interest", "আগ্রহী করা / আগ্রহ জন্মানো", "interessiert", "hat",
     "Das Thema Kindererziehung interessiert mich sehr.", "", ""),
    ("interessant", "", "", "adj", "interesting", "আকর্ষণীয় / মজার", "", "",
     "Ich habe einen interessanten Bericht gelesen.", "", ""),
    ("Interesse", "das", "-n", "noun", "interest", "আগ্রহ", "", "",
     "Ich habe viele Interessen: Sport, Lesen, Handarbeit, Tanzen.", "", ""),
    ("interessiert", "", "", "adj", "interested", "আগ্রহী", "", "",
     "Mein Nachbar zieht nächsten Monat aus. Sind Sie noch an der Wohnung interessiert?", "", ""),
    ("interkulturell", "", "", "adj", "intercultural", "আন্তঃসাংস্কৃতিক", "", "",
     "Wir haben in der Sprachschule ein interkulturelles Fest gefeiert.", "", ""),
    ("international", "", "", "adj", "international", "আন্তর্জাতিক", "", "",
     "Die Teilnehmenden in unserem Kurs sind ganz international.", "", ""),
    # === Page 52 Right ===
    ("Interview", "das", "-s", "noun", "interview", "সাক্ষাৎকার / ইন্টারভিউ", "", "",
     "Ich habe im Fernsehen ein interessantes Interview mit zwei Schauspielern gesehen.", "", ""),
    ("inzwischen", "", "", "adv", "meanwhile / in the meantime", "ইতিমধ্যে / এর মধ্যে", "", "",
     "Herr Müller kommt gleich zurück. Sie können inzwischen in seinem Büro warten.", "", ""),
    ("irgend-", "", "", "prefix", "some- / any- (prefix)", "কোনো- / যেকোনো- (উপসর্গ)", "", "",
     "Was für einen Saft möchten Sie? – Ganz egal, irgendeinen.", "", ""),
    ("irgendein", "", "", "pronoun", "some / any (at all)", "কোনো একটা / যেকোনো", "", "",
     "Was für einen Saft möchten Sie? – Ganz egal, irgendeinen.", "", ""),
    ("irgendwann", "", "", "adv", "sometime / at some point", "কোনো এক সময়", "", "",
     "Ich habe Sie irgendwann schon mal gesehen.", "", ""),
    ("sich irren", "", "", "verb", "to be mistaken / wrong", "ভুল করা", "geirrt", "hat",
     "Du irrst dich. Das Auto war nicht grün, sondern rot.", "", ""),
]

J_ENTRIES = [
    # === Page 52 Right (J start) ===
    ("ja", "", "", "particle", "yes / indeed / after all", "হ্যাঁ / নিশ্চয়ই", "", "",
     "Sind Sie verheiratet? – Ja.", "", ""),
    ("Jacke", "die", "-n", "noun", "jacket", "জ্যাকেট", "", "",
     "Zieh dir eine Jacke an. Es ist kalt.", "", ""),
    ("Jause", "die", "-n", "noun", "snack (Austria)", "জলখাবার (অস্ট্রিয়া)", "", "",
     "Es ist Zeit für eine kleine Jause.", "A: Jause, D: Imbiss, CH: Znüni/Zvieri", ""),
    ("je", "", "", "adv", "per / each / ever", "প্রতি / প্রতি / কখনও", "", "",
     "Die Pullover kosten je nach Qualität zwischen 40 und 60 Euro.", "", ""),
    ("je...desto...", "", "", "conjunction", "the...the... (comparative)", "যত...তত...", "", "",
     "Je länger ich Deutsch lerne, desto besser kann ich es verstehen.", "", ""),
    ("Jeans", "die", "(Pl.)", "noun", "jeans", "জিনস", "", "",
     "Nicht nur junge Leute tragen Jeans.", "", ""),
    ("jeder/jedes/jede", "", "", "pronoun", "every / each / everyone", "প্রত্যেক / প্রতিটি", "", "",
     "Das Restaurant hat jeden Tag geöffnet.", "", ""),
    # === Page 53 Left ===
    ("jederzeit", "", "", "adv", "at any time / anytime", "যেকোনো সময়", "", "",
     "Sie können mich jederzeit anrufen.", "", ""),
    ("jedes Mal", "", "", "adv", "every time / each time", "প্রতিবার", "", "",
     "Inge erzählt die Geschichte jedes Mal anders.", "", ""),
    ("jedoch", "", "", "conjunction", "however / but", "তবে / কিন্তু", "", "",
     "Sie ruft immer wieder an, jedoch ohne Erfolg.", "", ""),
    ("jemals", "", "", "adv", "ever", "কখনও", "", "",
     "Hast du jemals von dem Problem gehört? – Nein, nie.", "", ""),
    ("jemand", "", "", "pronoun", "someone / somebody", "কেউ / কেউ একজন", "", "",
     "Hat jemand einen Bleistift für mich?", "", ""),
    ("jetzt", "", "", "adv", "now", "এখন", "", "",
     "Ich muss jetzt gehen.", "", ""),
    ("jeweils", "", "", "adv", "respectively / each time", "প্রত্যেকবার / যথাক্রমে", "", "",
     "Der Kurs findet jeweils montags und donnerstags um 18 Uhr statt.", "", ""),
    ("Journalist", "der", "-en", "noun", "journalist (male)", "সাংবাদিক (পুরুষ)", "", "",
     "Meine Tochter möchte Journalistin werden.", "", ""),
    ("Journalistin", "die", "-nen", "noun", "journalist (female)", "সাংবাদিক (মহিলা)", "", "",
     "Meine Tochter möchte Journalistin werden.", "", ""),
    ("Jugend", "die", "", "noun", "youth", "যৌবন / তরুণ বয়স", "", "",
     "In meiner Jugend habe ich mich sehr für Musik interessiert.", "", ""),
    ("Jugendliche", "der/die", "-n", "noun", "adolescent / teenager / youth", "কিশোর / তরুণ", "", "",
     "Die Jugendlichen gehen gerne in die Disko.", "", ""),
    ("Jugendherberge", "die", "-n", "noun", "youth hostel", "যুব হোস্টেল", "", "",
     "Wo habt ihr übernachtet? – In einer Jugendherberge.", "", ""),
    ("jung", "", "", "adj", "young", "তরুণ / যুবক", "", "",
     "Für diesen Film bist du noch zu jung.", "", ""),
    ("Junge", "der", "-n", "noun", "boy (Germany)", "ছেলে (জার্মানি)", "", "",
     "In der Schulklasse sind 15 Jungen und 10 Mädchen.", "D: Junge, A/CH: Bub", ""),
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
    write_entries("I.csv", I_ENTRIES)
    write_entries("J.csv", J_ENTRIES)
