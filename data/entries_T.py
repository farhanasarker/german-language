"""T entries from pages 85-87"""
import csv, os

CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv", "alphabetisch")

ENTRIES = [
    # (word, article, plural, wordType, english, bangla, partizipII, auxiliary, exampleSentence, synonyms, antonyms)
    ("Tabelle", "die", "-n", "noun", "table/chart", "টেবিল / তালিকা", "", "", "Tragen Sie die richtige Information in die Tabelle ein.", "", ""),
    ("Tablette", "die", "-n", "noun", "tablet/pill", "ট্যাবলেট / ওষুধের বিড়া", "", "", "Nehmen Sie dreimal taeglich eine Tablette.", "", ""),
    ("Tafel", "die", "-n", "noun", "board/blackboard / bar (chocolate)", "বোর্ড / চকোলেটের বার", "", "", "Der Lehrer schreibt das neue Wort an die Tafel.", "", ""),
    ("Tagesablauf", "der", "¨-e", "noun", "daily routine", "দৈনন্দিন রুটিন", "", "", "Wie ist Ihr Tagesablauf?", "", ""),
    ("Tal", "das", "¨-er", "noun", "valley", "উপত্যকা", "", "", "Unser Dorf liegt in einem Tal.", "", ""),
    ("Talent", "das", "-e", "noun", "talent", "প্রতিভা", "", "", "Sie hat grosses Talent fuer Musik.", "", ""),
    ("tanken", "", "", "verb", "to refuel / fill up", "তেল/পেট্রোল ভরা", "getankt", "hat", "Wir muessen unbedingt tanken. Wir haben fast kein Benzin mehr.", "", ""),
    ("Tankstelle", "die", "-n", "noun", "gas station / petrol station", "পেট্রোল পাম্প", "", "", "Wo ist die naechste Tankstelle?", "", ""),
    ("Tante", "die", "-n", "noun", "aunt", "খালা / ফুফু / চাচী / মামী", "", "", "Die Familie meiner Mutter ist sehr gross, daher habe ich viele Tanten.", "", ""),
    ("tanzen", "", "", "verb", "to dance", "নাচা", "getanzt", "hat", "Auf der Hochzeit haben wir viel getanzt.", "", ""),
    ("Tanz", "der", "¨-e", "noun", "dance", "নাচ", "", "", "Diese modernen Taenze kann ich nicht.", "", ""),
    ("Tasche", "die", "-n", "noun", "bag / pocket", "ব্যাগ / পকেট", "", "", "Ich habe nicht viel Gepaeck, nur eine Tasche.", "", ""),
    ("Taschengeld", "das", "-er", "noun", "pocket money", "হাতখরচ", "", "", "Wie viel Taschengeld bekommst du im Monat?", "", ""),
    ("Taschentuch", "das", "¨-er", "noun", "tissue / handkerchief", "টিস্যু / রুমাল", "", "", "Hast du ein Taschentuch fuer mich?", "", ""),
    ("Tasse", "die", "-n", "noun", "cup", "কাপ", "", "", "Die Tassen sind von meiner Grossmutter.", "", ""),
    ("Tastatur", "die", "-en", "noun", "keyboard", "কিবোর্ড", "", "", "Die Tastatur an meinem Computer ist ganz neu.", "", ""),
    ("Taste", "die", "-n", "noun", "key / button", "বোতাম / কি", "", "", "An der Fernbedienung ist eine Taste kaputt.", "", ""),
    ("Tat", "die", "-en", "noun", "deed / act", "কাজ / কৃতিত্ব", "", "", "Dieser Mensch hat mit vielen guten Taten geholfen.", "", ""),
    ("Taeter", "der", "-", "noun", "perpetrator / offender", "অপরাধী", "", "", "Die Polizei hat den Taeter endlich gefasst.", "", ""),
    ("Taetigkeit", "die", "-en", "noun", "activity / occupation", "কাজ / পেশা", "", "", "Welche Taetigkeit wuerde Ihnen Spass machen?", "", ""),
    ("Tatsache", "die", "-n", "noun", "fact", "তথ্য / সত্য", "", "", "Das widerspricht den Tatsachen.", "", ""),
    ("tatsaechlich", "", "", "adv", "actually / indeed", "আসলে / প্রকৃতপক্ষে", "", "", "Die Hose ist tatsaechlich zu klein, obwohl sie so gross aussieht.", "", ""),
    ("taub", "", "", "adj", "deaf / numb", "বধির", "", "", "Sie hoert schlecht, sie ist schon fast taub.", "", ""),
    ("tauchen", "", "", "verb", "to dive", "ডুব দেওয়া", "getaucht", "ist/hat", "Ich moechte im Urlaub wieder tauchen gehen.", "", ""),
    ("tauschen", "", "", "verb", "to exchange / swap", "বিনিময় করা", "getauscht", "hat", "Ich wuerde meinen Kuchen gegen dein Brot tauschen.", "", ""),
    ("Technik", "die", "-en", "noun", "technology / technique", "প্রযুক্তি / কৌশল", "", "", "Ich verstehe nicht viel von Technik.", "", ""),
    ("technisch", "", "", "adj", "technical", "প্রযুক্তিগত", "", "", "Es gab ein technisches Problem.", "", ""),
    ("Technologie", "die", "-n", "noun", "technology", "প্রযুক্তি", "", "", "Grosse Fortschritte gab es in der Technologie.", "", ""),
    ("Tee", "der", "", "noun", "tea", "চা", "", "", "Bitte einen Tee mit Zitrone.", "", ""),
    ("teilen", "", "", "verb", "to share / divide", "ভাগ করা", "geteilt", "hat", "Mein Mann und ich teilen uns die Arbeit.", "", ""),
    ("Teil", "das", "-e", "noun", "part / piece", "অংশ / টুকরো", "", "", "Dieses Teil muessen wir erst bestellen.", "", ""),
    ("Teil", "der", "-e", "noun", "part / portion", "অংশ", "", "", "Was steht in dem Brief? Ich habe den ersten Teil nicht verstanden.", "", ""),
    ("Teilzeit", "die", "", "noun", "part-time", "পার্ট-টাইম", "", "", "Ich arbeite im Moment nur Teilzeit.", "", ""),
    ("teilnehmen", "", "", "verb", "to participate / take part", "অংশগ্রহণ করা", "teilgenommen", "hat", "Leider konnte ich an dem Kurs nicht regelmaessig teilnehmen.", "", ""),
    ("Teilnahme", "die", "-n", "noun", "participation", "অংশগ্রহণ", "", "", "Die Teilnahme am Gewinnspiel ist kostenlos.", "", ""),
    ("Teilnehmer", "der", "-", "noun", "participant", "অংশগ্রহণকারী", "", "", "Die Teilnehmerinnen aus unserem Kurs kommen aus verschiedenen Laendern.", "", ""),
    ("telefonieren", "", "", "verb", "to telephone / call", "ফোন করা", "telefoniert", "hat", "Ich muss kurz telefonieren.", "", ""),
    ("Telefon", "das", "-e", "noun", "telephone", "টেলিফোন", "", "", "Darf ich bitte Ihr Telefon benutzen?", "", ""),
    ("Teller", "der", "-", "noun", "plate", "প্লেট / থালা", "", "", "Stell bitte schon mal die Teller auf den Tisch!", "", ""),
    ("Temperatur", "die", "-en", "noun", "temperature", "তাপমাত্রা", "", "", "Die Temperaturen steigen heute um 10 Grad.", "", ""),
    ("Tempo", "das", "", "noun", "speed / pace", "গতি", "", "", "Hier darfst du nur Tempo 30 fahren.", "", ""),
    ("Tennis", "das", "", "noun", "tennis", "টেনিস", "", "", "Ich spiele gern Tennis.", "", ""),
    ("Teppich", "der", "-e", "noun", "carpet / rug", "কার্পেট", "", "", "Ich habe mir einen neuen Teppich gekauft.", "", ""),
    ("Termin", "der", "-e", "noun", "appointment / date", "অ্যাপয়েন্টমেন্ট / তারিখ", "", "", "Als Termin schlage ich den 3. Mai vor.", "", ""),
    ("Terminkalender", "der", "-", "noun", "appointment calendar / diary", "অ্যাপয়েন্টমেন্ট ক্যালেন্ডার", "", "", "Hast du unser Treffen schon in deinen Terminkalender eingetragen?", "", ""),
    ("Terrasse", "die", "-n", "noun", "terrace", "টেরেস / ছাদ", "", "", "Setzen wir uns auf die Terrasse!", "", ""),
    ("testen", "", "", "verb", "to test", "পরীক্ষা করা", "getestet", "hat", "Testen Sie unsere Angebote kostenlos.", "", ""),
    ("Test", "der", "-s", "noun", "test", "পরীক্ষা", "", "", "Ich bin ganz sicher: Du wirst den Test schaffen.", "", ""),
    ("teuer", "", "", "adj", "expensive", "দামি / ব্যয়বহুল", "", "", "Ich finde das Geschaeft nicht teuer.", "", ""),
    ("Text", "der", "-e", "noun", "text", "টেক্সট / লেখা", "", "", "Lesen Sie den Text.", "", ""),
    ("Theater", "das", "-", "noun", "theater", "থিয়েটার", "", "", "Wir gehen naechste Woche ins Theater.", "", ""),
    ("Thema", "das", "Themen", "noun", "topic / theme", "বিষয়", "", "", "Wir haben im Kurs viel ueber das Thema Umwelt gesprochen.", "", ""),
    ("theoretisch", "", "", "adj", "theoretical", "তাত্ত্বিক", "", "", "Ich habe die theoretische Pruefung bestanden. Nach der praktischen habe ich den Fuehrerschein.", "", ""),
    ("Theorie", "die", "-n", "noun", "theory", "তত্ত্ব", "", "", "Das ist die Theorie. In der Praxis ist vieles ganz anders.", "", ""),
    ("Therapie", "die", "-n", "noun", "therapy", "থেরাপি / চিকিৎসা", "", "", "Die Therapie hat geholfen. Es geht mir schon viel besser.", "", ""),
    ("Ticket", "das", "-s", "noun", "ticket", "টিকিট", "", "", "Wir muessen die Tickets fuer unseren Flug ausdrucken.", "", ""),
    ("tief", "", "", "adj", "deep", "গভীর", "", "", "Vorsicht, Kinder! Das Wasser ist hier sehr tief.", "", ""),
    ("Tier", "das", "-e", "noun", "animal", "প্রাণী / পশু", "", "", "Er mag Tiere sehr und geht darum oft in den Zoo.", "", ""),
    ("Haustier", "das", "-e", "noun", "pet", "পালিত প্রাণী", "", "", "Hat deine Familie ein Haustier? Ja, wir haben einen Hund.", "", ""),
    ("Tierpark", "der", "-s", "noun", "zoo / animal park", "চিড়িয়াখানা", "", "", "Wollen wir am Samstag mit den Kindern in den Tierpark gehen?", "", ""),
    ("Tipp", "der", "-s", "noun", "tip / hint", "টিপ / পরামর্শ", "", "", "Kannst du mir einen Tipp geben? Wo finde ich billige Moebel?", "", ""),
    ("tippen", "", "", "verb", "to type", "টাইপ করা", "getippt", "hat", "Wie schnell kannst du tippen?", "", ""),
    ("Tisch", "der", "-e", "noun", "table", "টেবিল", "", "", "Das Essen steht schon auf dem Tisch.", "", ""),
    ("Titel", "der", "-", "noun", "title", "শিরোনাম / উপাধি", "", "", "Wie heisst der Film? Ich weiss den Titel nicht mehr.", "", ""),
    ("Tochter", "die", "¨-", "noun", "daughter", "মেয়ে / কন্যা", "", "", "Das ist meine Tochter Katharina.", "", ""),
    ("Tod", "der", "", "noun", "death", "মৃত্যু", "", "", "Ich habe ihn vor seinem Tod noch einmal gesehen.", "", ""),
    ("toedlich", "", "", "adj", "deadly / fatal", "মারণাত্মক", "", "", "Dieses Gift kann fuer den Menschen toedlich sein.", "", ""),
    ("Toilette", "die", "-n", "noun", "toilet / restroom", "টয়লেট / শৌচালয়", "", "", "Wo ist die Toilette, bitte?", "", ""),
    ("tolerant", "", "", "adj", "tolerant", "সহনশীল", "", "", "Die Nachbarn hoeren oft laut Musik. Wir muessen sehr tolerant sein.", "", ""),
    ("toll", "", "", "adj", "great / fantastic", "দারুণ / অসাধারণ", "", "", "Ich habe mir ein tolles Kleid gekauft.", "", ""),
    ("Tomate", "die", "-n", "noun", "tomato", "টমেটো", "", "", "Kauf bitte noch Tomaten auf dem Markt.", "", ""),
    ("Topf", "der", "¨-e", "noun", "pot", "পাত্র / হাঁড়ি", "", "", "Hast du keinen groesseren Topf? Ich moechte Kartoffeln kochen.", "", ""),
    ("Tor", "das", "-e", "noun", "gate / goal", "গেট / গোল", "", "", "Hinter dem Tor geht es zur Fabrik.", "", ""),
    ("Torte", "die", "-n", "noun", "cake / torte", "টর্ট / কেক", "", "", "Zum Geburtstag backe ich dir eine Torte.", "", ""),
    ("tot", "", "", "adj", "dead", "মৃত", "", "", "Meine Grosseltern sind schon lange tot.", "", ""),
    ("Tote", "der", "-n", "noun", "dead person", "মৃত ব্যক্তি", "", "", "Bei dem Unfall gab es zwei Tote.", "", ""),
    ("total", "", "", "adj", "totally / completely", "সম্পূর্ণভাবে", "", "", "Der Film war total langweilig.", "", ""),
    ("Tourismus", "der", "", "noun", "tourism", "পর্যটন", "", "", "In dieser Gegend gibt es viel Tourismus.", "", ""),
    ("Tourist", "der", "-en", "noun", "tourist", "পর্যটক", "", "", "Es kommen immer mehr Touristen in unsere Stadt.", "", ""),
    ("Tradition", "die", "-en", "noun", "tradition", "ঐতিহ্য", "", "", "Eine grosse Hochzeit mit vielen Leuten ist bei uns Tradition.", "", ""),
    ("traditionell", "", "", "adj", "traditional", "ঐতিহ্যগত", "", "", "Ich mag die traditionelle Kueche.", "", ""),
    ("tragen", "", "", "verb", "to carry / wear / bear", "বহন করা / পরা", "getragen", "hat", "Lass mich den Koffer tragen. Der ist zu schwer fuer dich.", "", ""),
    ("trainieren", "", "", "verb", "to train / practice", "প্রশিক্ষণ দেওয়া / অনুশীলন করা", "trainiert", "hat", "Wir trainieren einmal pro Woche im Sportverein.", "", ""),
    ("Trainer", "der", "-", "noun", "coach / trainer", "প্রশিক্ষক", "", "", "Ich finde unseren Trainer sehr nett.", "", ""),
    ("Training", "das", "-s", "noun", "training", "প্রশিক্ষণ", "", "", "Jeden Dienstag ist Training.", "", ""),
    ("Tram", "das", "-s", "noun", "tram", "ট্রাম", "", "", "Fahren wir mit dem Tram oder dem Bus?", "", ""),
    ("Traene", "die", "-n", "noun", "tear", "অশ্রু / চোখের জল", "", "", "Sie trocknet dem Kind die Traenen.", "", ""),
    ("transportieren", "", "", "verb", "to transport", "পরিবহন করা", "transportiert", "hat", "Wie willst du die Moebel denn transportieren?", "", ""),
    ("Transport", "der", "-e", "noun", "transport / transportation", "পরিবহন", "", "", "Was kostet der Transport?", "", ""),
    ("traeumen", "", "", "verb", "to dream", "স্বপ্ন দেখা", "getraeumt", "hat", "Ich habe schlecht getraeumt.", "", ""),
    ("Traum", "der", "¨-e", "noun", "dream", "স্বপ্ন", "", "", "Mein Traum ist ein eigenes Geschaeft.", "", ""),
    ("Traum-", "", "", "prefix", "dream-", "স্বপ্নের-", "", "", "Mein Traumberuf ist Feuerwehrmann.", "", ""),
    ("traurig", "", "", "adj", "sad", "দুঃখিত / বিষণ্ণ", "", "", "Ich bin traurig. Ich darf nicht mitfahren.", "", ""),
    ("treffen", "", "", "verb", "to meet / hit", "দেখা করা / মিলিত হওয়া", "getroffen", "hat", "Wir treffen uns immer freitags.", "", ""),
    ("Treffpunkt", "der", "-e", "noun", "meeting point", "মিলনস্থল", "", "", "Unser Treffpunkt ist um 17 Uhr am Hauptbahnhof.", "", ""),
    ("treiben", "", "", "verb", "to do (sports) / drive", "করা (খেলাধুলা)", "getrieben", "hat", "Welchen Sport treibst du?", "", ""),
    ("trennen", "", "", "verb", "to separate / split up", "আলাদা করা / বিচ্ছেদ হওয়া", "getrennt", "hat", "Wir leben getrennt.", "", ""),
    ("Trennung", "die", "-en", "noun", "separation", "বিচ্ছেদ / পৃথকীকরণ", "", "", "Die Trennung von der Familie war schwierig.", "", ""),
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
    write_entries("T.csv", ENTRIES)
