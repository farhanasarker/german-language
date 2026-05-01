"""D entries from pages 31-32 (continuing from existing D.csv)"""
import csv, os

CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv", "alphabetisch")

ENTRIES = [
    # === Page 31 - Left Column ===
    ("Detail", "das", "-s", "noun", "detail", "বিস্তারিত", "", "",
     "Dieses Detail ist unwichtig.", "", ""),
    ("deutlich", "", "", "adj", "clear / distinct", "স্পষ্ট", "", "",
     "Schreiben Sie bitte deutlich!", "", ""),
    ("Diät", "die", "", "noun", "diet", "ডায়েট / খাদ্য নিয়ন্ত্রণ", "", "",
     "Ich möchte abnehmen. Deshalb mache ich eine Diät.", "", ""),
    ("Dialekt", "der", "-e", "noun", "dialect", "উপভাষা / আঞ্চলিক ভাষা", "", "",
     "Ich verstehe dich besser, wenn du nicht Dialekt sprichst.", "", ""),
    ("Dialog", "der", "-e", "noun", "dialogue", "সংলাপ / কথোপকথন", "", "",
     "Sie hören jetzt einen Dialog.", "", ""),
    ("dicht", "", "", "adj", "tight / sealed / dense", "ঘন / নিবিড় / আঁট", "", "",
     "Unsere Fenster sind nicht dicht. Es zieht immer.", "", ""),
    ("dick", "", "", "adj", "thick / fat", "মোটা / স্থূল", "", "",
     "Ich bin zu dick. Ich muss weniger essen.", "", ""),
    ("Dieb", "der", "-e", "noun", "thief", "চোর", "", "",
     "Ein Dieb hat mir auf dem Markt die Tasche gestohlen.", "", ""),
    ("dienen", "", "", "verb", "to serve", "সেবা করা / কাজে লাগা", "gedient", "hat",
     "Er hat der Firma viele Jahre lang gedient.", "", ""),
    ("Dienst", "der", "", "noun", "service / duty / shift", "সেবা / ডিউটি / শিফট", "", "",
     "Morgen habe ich Dienst. Deshalb kann ich nicht kommen.", "", ""),
    ("dies-", "", "", "pronoun", "this / these", "এই / এগুলি", "", "",
     "Wohin fährst du dieses Jahr in Urlaub?", "", ""),
    ("diesmal", "", "", "adv", "this time", "এবার", "", "",
     "Diesmal haben wir zum Glück gewonnen.", "", ""),
    ("digital", "", "", "adj", "digital", "ডিজিটাল", "", "",
     "Ich habe eine Digitaluhr gekauft.", "", ""),
    ("Ding", "das", "-e", "noun", "thing", "জিনিস / বস্তু", "", "",
     "Gib mir bitte mal das Ding da drüben.", "", ""),
    ("Diplom", "das", "-e", "noun", "diploma / degree", "ডিপ্লোমা / সনদ", "", "",
     "Wo kann ich mein Diplom abholen?", "", ""),
    ("direkt", "", "", "adj", "direct / directly", "সরাসরি / প্রত্যক্ষ", "", "",
     "Wir liefern Ihnen die Waren direkt ins Haus.", "", ""),
    ("Direktor", "der", "-en", "noun", "director / principal (male)", "পরিচালক (পুরুষ)", "", "",
     "Ich möchte gern mit dem Direktor sprechen.", "", ""),
    ("Direktorin", "die", "-nen", "noun", "director / principal (female)", "পরিচালক (মহিলা)", "", "",
     "Ich möchte gern mit der Direktorin sprechen.", "", ""),
    ("Diskothek", "die", "-en", "noun", "discotheque / nightclub", "ডিস্কো / নাইটক্লাব", "", "",
     "Wir gehen heute Abend in die Disko(thek).", "", ""),

    # === Page 31 - Right Column ===
    ("diskutieren", "", "", "verb", "to discuss", "আলোচনা করা / বিতর্ক করা", "diskutiert", "hat",
     "Wir haben lange diskutiert, wie wir das Büro einrichten sollen.", "", ""),
    ("Diskussion", "die", "-en", "noun", "discussion", "আলোচনা / বিতর্ক", "", "",
     "Im Fernsehen gab es eine Diskussion zum Thema \"Kinderbetreuung\".", "", ""),
    ("Distanz", "die", "-en", "noun", "distance", "দূরত্ব", "", "",
     "Diese Firma transportiert Waren auch über große Distanzen.", "", ""),
    ("doch", "", "", "particle", "yes (contradicting) / but / after all", "হ্যাঁ (বিরোধে) / কিন্তু / অবশ্যই", "", "",
     "Isst du kein Fleisch? – Doch, manchmal schon.", "", ""),
    ("Doktor", "der", "-en", "noun", "doctor (male)", "ডাক্তার (পুরুষ)", "", "",
     "Ist Frau Dr. Müller da?", "", ""),
    ("Doktorin", "die", "-nen", "noun", "doctor (female)", "ডাক্তার (মহিলা)", "", "",
     "Meine Tochter ist krank. Wir gehen zur Doktorin.", "", ""),
    ("Dokument", "das", "-e", "noun", "document", "নথি / দলিল", "", "",
     "Hast du alle Dokumente für die Anmeldung dabei?", "", ""),
    ("donnern", "", "", "verb", "to thunder / roar", "বজ্রপাত হওয়া / গর্জন করা", "gedonnert", "hat",
     "Hörst du es donnern? Das Gewitter kommt näher.", "", ""),
    ("Donner", "der", "-", "noun", "thunder", "বজ্রধ্বনি", "", "",
     "Der Donner kam erst lange nach dem Blitz.", "", ""),
    ("doppelt", "", "", "adj", "double", "দ্বিগুণ / ডাবল", "", "",
     "Das Buch habe ich doppelt.", "", ""),
    ("Doppel-", "", "", "prefix", "double- / twin-", "দ্বি- / যমজ-", "", "",
     "Wir hätten gern ein Doppelbett.", "", ""),
    ("Dorf", "das", "¨-er", "noun", "village", "গ্রাম", "", "",
     "Unser Dorf liegt direkt an der Autobahn.", "", ""),
    ("dort", "", "", "adv", "there", "সেখানে", "", "",
     "Dort drüben ist der Bahnhof.", "", ""),
    ("dorthin", "", "", "adv", "to there / thither", "সেদিকে / সেইখানে", "", "",
     "Deine Tasche kannst du dorthin stellen.", "", ""),
    ("Dose", "die", "-n", "noun", "can / tin", "কৌটা / টিন", "", "",
     "Ich habe noch eine Dose Bohnen.", "D/CH: Büchse", ""),
    ("draußen", "", "", "adv", "outside", "বাইরে", "", "",
     "Es ist kalt draußen.", "", ""),
    ("Dreck", "der", "", "noun", "dirt / filth", "ময়লা / মাটি", "", "",
     "Iss den Apfel nicht! Der lag im Dreck.", "", ""),

    # === Page 32 - Left Column ===
    ("drehen", "", "", "verb", "to turn / rotate", "ঘোরানো / মোড় নেওয়া", "gedreht", "hat",
     "Drehen Sie zum Einschalten den Schalter nach rechts.", "", ""),
    ("dringend", "", "", "adj", "urgent / urgently", "জরুরি / জরুরিভাবে", "", "",
     "Ich muss dich dringend sprechen.", "", ""),
    ("drin", "", "", "adv", "inside / in there", "ভিতরে", "", "",
     "In der Packung ist nichts mehr drin.", "", ""),
    ("drinnen", "", "", "adv", "inside / indoors", "ভিতরে / ঘরের ভিতরে", "", "",
     "Bei der Hitze ist es drinnen viel angenehmer.", "", ""),
    ("Droge", "die", "-n", "noun", "drug", "মাদক / ড্রাগ", "", "",
     "Nimmst du etwa Drogen?", "", ""),
    ("Drogerie", "die", "-n", "noun", "drugstore", "ড্রাগস্টোর / প্রসাধনী দোকান", "", "",
     "Waschmittel bekommst du in der Drogerie.", "", ""),
    ("drüben", "", "", "adv", "over there", "ওপারে / ওদিকে", "", "",
     "Dort drüben ist die Haltestelle.", "", ""),
    ("drucken", "", "", "verb", "to print", "মুদ্রণ করা / প্রিন্ট করা", "gedruckt", "hat",
     "Warum hast du den Brief noch nicht ausgedruckt?", "", ""),
    ("Drucker", "der", "-", "noun", "printer", "প্রিন্টার", "", "",
     "Ich brauche einen neuen Drucker für meinen Computer.", "", ""),
    ("drücken", "", "", "verb", "to press / push", "চাপ দেওয়া / টিপা", "gedrückt", "hat",
     "Sie brauchen nur auf den Knopf zu drücken.", "", ""),
    ("Druck", "der", "", "noun", "pressure / print", "চাপ / মুদ্রণ", "", "",
     "Mit einem Knopfdruck schaltet man das Gerät ein.", "", ""),
    ("dumm", "", "", "adj", "stupid / silly", "বোকা / মূর্খ", "", "",
     "Entschuldigung, das war dumm von mir.", "", ""),
    ("dunkel", "", "", "adj", "dark", "অন্ধকার / গাঢ়", "", "",
     "Um sechs Uhr ist es schon dunkel.", "", ""),
    ("dünn", "", "", "adj", "thin", "পাতলা / সরু", "", "",
     "Mein Sohn ist sehr dünn. Er isst zu wenig.", "", ""),
    ("durch", "", "", "preposition", "through / by", "মধ্য দিয়ে / দ্বারা", "", "",
     "Wir sind mit dem Fahrrad durch den Wald gefahren.", "", ""),

    # === Page 32 - Right Column ===
    ("durcheinander", "", "", "adj", "mixed up / confused / messy", "বিশৃঙ্খল / গোলমেলে", "", "",
     "Alle meine Sachen sind durcheinander. Ich finde nichts mehr.", "", ""),
    ("Durchsage", "die", "-n", "noun", "announcement (loudspeaker)", "ঘোষণা (লাউডস্পিকার)", "", "",
     "Achtung, Achtung, eine wichtige Durchsage!", "", ""),
    ("Durchschnitt", "der", "-e", "noun", "average", "গড়", "", "",
     "Im Durchschnitt brauchen wir täglich 20 Minuten zur Arbeit.", "", ""),
    ("durchschnittlich", "", "", "adj", "on average / average", "গড়ে / গড়পড়তা", "", "",
     "Die Preise sind im letzten Jahr um durchschnittlich 6 % gestiegen.", "", ""),
    ("dürfen", "", "", "verb", "to be allowed to / may", "অনুমতি থাকা / পারা", "gedurft", "hat",
     "Dürfen wir heute länger fernsehen?", "", ""),
    ("Durst", "der", "", "noun", "thirst", "তৃষ্ণা / পিপাসা", "", "",
     "Sie haben sicher Durst.", "", ""),
    ("durstig", "", "", "adj", "thirsty", "তৃষ্ণার্ত", "", "",
     "Du bist sicher durstig. Was möchtest du trinken?", "", ""),
    ("sich duschen", "", "", "verb", "to shower (oneself)", "গোসল করা (শাওয়ার)", "geduscht", "hat",
     "Wenn Sie sich duschen wollen: Das Badezimmer ist dort hinten links.", "", ""),
    ("Dusche", "die", "-n", "noun", "shower (fixture)", "শাওয়ার", "", "",
     "Wir haben leider nur noch ein Zimmer mit Dusche.", "", ""),
    ("duzen", "", "", "verb", "to address with 'du' (informal you)", "তুমি বলে সম্বোধন করা", "geduzt", "hat",
     "Wollen wir Du zueinander sagen? Ja, wir können uns gern duzen.", "", ""),
]

if __name__ == "__main__":
    filepath = os.path.join(CSV_DIR, "D.csv")
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
        for e in ENTRIES:
            if e[0] not in existing_words:
                writer.writerow(e)
                new_count += 1

    print(f"D.csv: {len(existing)} existing + {new_count} new = {len(existing) + new_count} total")
