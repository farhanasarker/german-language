"""
Smart multi-line parser for extracted Goethe B1 PDF text.
Groups related lines into entries using entry-boundary detection.
"""
import re, csv, os, sys

CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv", "alphabetisch")

# ── Translations ──────────────────────────────────────────────────────
TR = {}

def t(word, english, bangla, wtype=None):
    TR[word] = (english, bangla, wtype)

# D words
t("Detail", "detail", "বিস্তারিত")
t("deutlich", "clear / distinct", "স্পষ্ট")
t("Diät", "diet", "ডায়েট / খাদ্য নিয়ন্ত্রণ")
t("Dialekt", "dialect", "উপভাষা / আঞ্চলিক ভাষা")
t("Dialog", "dialogue", "সংলাপ / কথোপকথন")
t("dicht", "tight / sealed / dense", "ঘন / নিবিড় / আঁট")
t("dick", "thick / fat", "মোটা / স্থূল")
t("Dieb", "thief", "চোর")
t("dienen", "to serve", "সেবা করা / কাজে লাগা")
t("Dienst", "service / duty / shift", "সেবা / ডিউটি / শিফট")
t("dies-", "this / these", "এই / এগুলি")
t("diesmal", "this time", "এবার")
t("digital", "digital", "ডিজিটাল")
t("Ding", "thing", "জিনিস / বস্তু")
t("Diplom", "diploma / degree", "ডিপ্লোমা / সনদ")
t("direkt", "direct / directly", "সরাসরি / প্রত্যক্ষ")
t("Direktor", "director / principal (male)", "পরিচালক (পুরুষ)")
t("Direktorin", "director / principal (female)", "পরিচালক (মহিলা)")
t("Diskothek", "discotheque / nightclub", "ডিস্কো / নাইটক্লাব")
t("diskutieren", "to discuss", "আলোচনা করা / বিতর্ক করা")
t("Diskussion", "discussion", "আলোচনা / বিতর্ক")
t("Distanz", "distance", "দূরত্ব")
t("doch", "yes (contradicting) / but / after all", "হ্যাঁ (বিরোধে) / কিন্তু / অবশ্যই")
t("Doktor", "doctor (male)", "ডাক্তার (পুরুষ)")
t("Doktorin", "doctor (female)", "ডাক্তার (মহিলা)")
t("Dokument", "document", "নথি / দলিল")
t("donnern", "to thunder / roar", "বজ্রপাত হওয়া / গর্জন করা")
t("Donner", "thunder", "বজ্রধ্বনি")
t("doppelt", "double", "দ্বিগুণ / ডাবল")
t("Doppel-", "double- / twin-", "দ্বি- / যমজ-")
t("Dorf", "village", "গ্রাম")
t("dort", "there", "সেখানে")
t("dorthin", "to there / thither", "সেদিকে / সেইখানে")
t("Dose", "can / tin", "কৌটা / টিন")
t("draußen", "outside", "বাইরে")
t("Dreck", "dirt / filth", "ময়লা / মাটি")
t("drehen", "to turn / rotate", "ঘোরানো / মোড় নেওয়া")
t("dringend", "urgent / urgently", "জরুরি / জরুরিভাবে")
t("drin", "inside / in there", "ভিতরে")
t("drinnen", "inside / indoors", "ভিতরে / ঘরের ভিতরে")
t("Droge", "drug", "মাদক / ড্রাগ")
t("Drogerie", "drugstore", "ড্রাগস্টোর / প্রসাধনী দোকান")
t("drüben", "over there", "ওপারে / ওদিকে")
t("drucken", "to print", "মুদ্রণ করা / প্রিন্ট করা")
t("Drucker", "printer", "প্রিন্টার")
t("drücken", "to press / push", "চাপ দেওয়া / টিপা")
t("Druck", "pressure / print", "চাপ / মুদ্রণ")
t("dumm", "stupid / silly", "বোকা / মূর্খ")
t("dunkel", "dark", "অন্ধকার / গাঢ়")
t("dünn", "thin", "পাতলা / সরু")
t("durch", "through / by", "মধ্য দিয়ে / দ্বারা")
t("durcheinander", "mixed up / confused / messy", "বিশৃঙ্খল / গোলমেলে")
t("Durchsage", "announcement (loudspeaker)", "ঘোষণা (লাউডস্পিকার)")
t("Durchschnitt", "average", "গড়")
t("durchschnittlich", "on average / average (adj)", "গড়ে / গড়পড়তা")
t("dürfen", "to be allowed to / may", "অনুমতি থাকা / পারা")
t("Durst", "thirst", "তৃষ্ণা / পিপাসা")
t("durstig", "thirsty", "তৃষ্ণার্ত")
t("sich duschen", "to shower (oneself)", "গোসল করা (শাওয়ার)")
t("duschen", "to shower", "গোসল করা (শাওয়ার)")
t("Dusche", "shower (fixture)", "শাওয়ার")
t("duzen", "to address with 'du' (informal you)", "তুমি বলে সম্বোধন করা")

# E words
t("eben", "just / exactly / flat", "এইমাত্র / ঠিক")
t("ebenfalls", "likewise / also", "একইভাবে")
t("ebenso", "just as / likewise", "ঠিক তেমনই")
t("e-card", "e-card (health insurance, Austria)", "ই-কার্ড (অস্ট্রিয়া)")
t("echt", "real / genuine / really", "আসল / খাঁটি")
t("ec-Karte", "EC card / debit card", "ইসি কার্ড")
t("EC-Karte", "EC card / debit card", "ইসি কার্ড")
t("Ecke", "corner (Germany/Switzerland)", "কোণ")
t("Eck", "corner (Austria)", "কোণ (অস্ট্রিয়া)")
t("eckig", "angular / square", "কৌণিক / চারকোণা")
t("egal", "all the same / doesn't matter", "কিছু যায় আসে না")
t("Ehe", "marriage", "বিবাহ")
t("Ehefrau", "wife", "স্ত্রী")
t("Ehemann", "husband", "স্বামী")
t("Ehepaar", "married couple", "বিবাহিত দম্পতি")
t("eher", "earlier / rather / sooner", "বরং / আগে")
t("ehrlich", "honest / honestly", "সৎ")
t("Ei", "egg", "ডিম")
t("eigen-", "own", "নিজস্ব")
t("eigentlich", "actually / really", "আসলে")
t("sich eignen", "to be suitable / suited", "উপযুক্ত হওয়া")
t("eilen", "to hurry / rush", "তাড়াতাড়ি করা")
t("Eile", "hurry / haste", "তাড়াতাড়ি / ত্বরা")
t("eilig", "hurried / in a hurry", "তাড়াহুড়ো")
t("ein-", "one / a / an", "এক / একটি")
t("Einbahnstraße", "one-way street", "একমুখী রাস্তা")
t("einbrechen", "to break in / burgle", "সিঁধ কাটা")
t("Einbrecher", "burglar (male)", "চোর (পুরুষ)")
t("Einbrecherin", "burglar (female)", "চোর (মহিলা)")
t("Einbruch", "break-in / burglary", "সিঁধেল চুরি")
t("eindeutig", "clear / unambiguous", "সুস্পষ্ট")
t("Eindruck", "impression", "প্রভাব / ছাপ")
t("einerseits", "on the one hand", "একদিকে")
t("einfach", "simple / easy / just", "সহজ / সরল")
t("Einfahrt", "driveway / entrance", "প্রবেশ পথ")
t("einfallen", "to occur / come to mind", "মনে পড়া")
t("Einfall", "idea / sudden thought", "মাথায় আসা চিন্তা")
t("Einfluss", "influence", "প্রভাব")
t("beeinflussen", "to influence", "প্রভাবিত করা")
t("einfügen", "to insert / paste", "সন্নিবেশ করা")
t("einführen", "to introduce / import", "প্রবর্তন / আমদানি করা")
t("Einführung", "introduction", "ভূমিকা / প্রবর্তন")
t("Eingang", "entrance", "প্রবেশদ্বার")
t("einheitlich", "uniform / standardized", "অভিন্ন / একই ধরনের")
t("einig-", "some / a few / agreed", "কিছু / একমত")
t("sich einigen", "to agree / reach agreement", "একমত হওয়া")
t("einkaufen", "to shop / go shopping", "কেনাকাটা করা")
t("Einkauf", "purchase / shopping", "কেনাকাটা")
t("Einkommen", "income", "আয়")
t("einladen", "to invite", "আমন্ত্রণ জানানো")
t("Einladung", "invitation", "আমন্ত্রণ")
t("einmal", "once / one time", "একবার")
t("einnehmen", "to take (medicine) / earn", "গ্রহণ করা (ঔষধ) / আয় করা")
t("Einnahme", "revenue / income", "রাজস্ব / আয়")
t("einpacken", "to pack / wrap up", "প্যাক করা / মোড়ানো")
t("einrichten", "to furnish / set up", "সাজানো / স্থাপন করা")
t("Einrichtung", "furnishings / facility", "আসবাবপত্র / প্রতিষ্ঠান")
t("einsam", "lonely / solitary", "একাকী / নিঃসঙ্গ")
t("einschalten", "to switch on / turn on", "চালু করা / অন করা")
t("einschließlich", "including / inclusive", "সহ / সমেত")
t("Einschreiben", "registered mail", "রেজিস্টার্ড ডাক")
t("einsetzen", "to insert / appoint / employ", "নিয়োগ করা / ব্যবহার করা")
t("einsteigen", "to get in / board", "উঠা / চড়া (গাড়িতে)")
t("einstellen", "to hire / adjust / set", "নিয়োগ / সমন্বয় করা")
t("eintragen", "to enter / register", "লিখে রাখা / নিবন্ধন করা")
t("eintreten", "to enter / join", "প্রবেশ করা / যোগদান")
t("Eintritt", "admission / entry", "প্রবেশ / প্রবেশ মূল্য")
t("einverstanden", "agreed / okay", "একমত / সম্মত")
t("Einwohner", "inhabitant / resident (male)", "বাসিন্দা (পুরুষ)")
t("Einwohnerin", "inhabitant / resident (female)", "বাসিন্দা (মহিলা)")
t("einzahlen", "to deposit (money)", "জমা করা (টাকা)")
t("Einzahlung", "deposit / payment", "জমা / পরিশোধ")
t("einzeln", "single / individual / one by one", "একক / আলাদা / একে একে")
t("Einzel-", "single / individual", "একক")
t("Einzelheit", "detail", "বিস্তারিত")
t("einzig-", "only / sole / unique", "একমাত্র / অনন্য")
t("einziehen", "to move in / collect", "স্থানান্তরিত হওয়া / সংগ্রহ করা")
t("Eis", "ice / ice cream", "বরফ / আইসক্রিম")
t("Eisenbahn", "railway / train", "রেলপথ / ট্রেন")
t("elegant", "elegant", "অভিজাত / মার্জিত")
t("elektrisch", "electric / electrical", "বৈদ্যুতিক")
t("Elektro-", "electro- / electric", "ইলেকট্রো-")
t("elektronisch", "electronic", "ইলেকট্রনিক")
t("Eltern", "parents (pl.)", "মা-বাবা")
t("empfangen", "to receive", "গ্রহণ করা")
t("Empfang", "reception / receipt", "অভ্যর্থনা / প্রাপ্তি")
t("Empfänger", "recipient / receiver", "প্রাপক")
t("empfehlen", "to recommend", "সুপারিশ করা")
t("Empfehlung", "recommendation", "সুপারিশ")
t("enden", "to end / finish", "শেষ হওয়া")
t("Ende", "end", "শেষ / সমাপ্তি")
t("endgültig", "final / definitive", "চূড়ান্ত")
t("endlich", "finally / at last", "অবশেষে")
t("Energie", "energy", "শক্তি / এনার্জি")
t("eng", "narrow / tight / close", "সংকীর্ণ / ঘনিষ্ঠ")
t("Enkel", "grandson (male)", "নাতি (পুরুষ)")
t("Enkelin", "granddaughter (female)", "নাতনি (মহিলা)")
t("entdecken", "to discover", "আবিষ্কার করা")
t("entfernen", "to remove / delete", "অপসারণ করা")
t("Entfernung", "distance / removal", "দূরত্ব")
t("entgegenkommen", "to come towards / accommodate", "ছাড় দেওয়া / সাহায্য করা")
t("enthalten", "to contain", "ধারণ করা")
t("entlang", "along", "বরাবর / ধরে")
t("entlassen", "to dismiss / discharge / fire", "বরখাস্ত করা / ছেড়ে দেওয়া")
t("Entlassung", "dismissal / discharge", "বরখাস্ত")
t("entscheiden", "to decide", "সিদ্ধান্ত নেওয়া")
t("Entscheidung", "decision", "সিদ্ধান্ত")
t("unentschieden", "undecided / tied (sports)", "অনিশ্চিত / অমীমাংসিত")
t("sich entschließen", "to decide / resolve", "সিদ্ধান্ত নেওয়া / সংকল্প করা")
t("entschlossen", "determined / resolute", "দৃঢ়প্রতিজ্ঞ")
t("entschuldigen", "to excuse / apologize", "ক্ষমা করা / মাফ চাওয়া")
t("Entschuldigung", "apology / excuse me", "ক্ষমা / দুঃখিত")
t("entsorgen", "to dispose of", "নিষ্পত্তি করা")
t("entspannend", "relaxing", "আরামদায়ক")
t("entstehen", "to arise / originate / be created", "সৃষ্টি হওয়া")
t("enttäuschen", "to disappoint", "হতাশ করা")
t("Enttäuschung", "disappointment", "হতাশা")
t("entweder ... oder", "either ... or", "হয় ... অথবা")
t("entwickeln", "to develop", "উন্নয়ন করা")
t("Entwicklung", "development", "উন্নয়ন")
t("Erde", "earth / ground / soil", "পৃথিবী / মাটি")
t("Erdapfel", "potato (Austria)", "আলু (অস্ট্রিয়া)")
t("Erdgeschoss", "ground floor", "নিচতলা")
t("Ergeschoß", "ground floor (Austria)", "নিচতলা (অস্ট্রিয়া)")
t("Ereignis", "event / occurrence", "ঘটনা")
t("sich ereignen", "to happen / occur", "ঘটা")
t("erfahren", "to learn / find out / experience", "জানা / অভিজ্ঞতা অর্জন")
t("Erfahrung", "experience", "অভিজ্ঞতা")
t("erfinden", "to invent", "উদ্ভাবন করা")
t("Erfindung", "invention", "উদ্ভাবন")
t("Erfolg", "success", "সাফল্য")

print(f"Translations loaded: {len(TR)} entries")

# ── Parse extracted text ─────────────────────────────────────────────

def is_new_entry_start(line):
    """Check if a line starts a new word entry."""
    line = line.strip()
    if not line or len(line) < 2:
        return False
    # Skip known non-entry patterns
    skip = ['WORTLISTE', 'ZERTIFIKAT B1', '30_SV', '---', '===']
    if any(line.startswith(s) for s in skip):
        return False
    if re.match(r'^\d{1,3}$', line):
        return False
    # Entry starts:
    # 1. Article + word: "der/die/das Word..."
    if re.match(r'^(der|die|das)\s+\S', line):
        return True
    # 2. Verb: "word, 3sg, ..." or "sich word, ..."
    if re.match(r'^(sich\s+)?[a-zäöüß]+(en|n),\s', line):
        return True
    # 3. Single word (adj/adv/prep): starts with lowercase letter, no comma
    if re.match(r'^[a-zäöüß][a-zäöüß-]+(?:\s|$)', line) and ',' not in line[:30]:
        return True
    # 4. Capitalized word (special terms, prefixes)
    if re.match(r'^[A-ZÄÖÜ][a-zäöüß-]+\s', line):
        return True
    return False

def parse_entry_lines(lines):
    """Parse a group of lines into a structured entry."""
    if not lines:
        return None

    first = lines[0].strip()
    rest_lines = [l.strip() for l in lines[1:] if l.strip()]
    all_text = ' '.join(lines)

    entry = {
        "word": "", "article": "", "plural": "",
        "wordType": "unknown", "english": "", "bangla": "",
        "partizipII": "", "auxiliary": "",
        "exampleSentence": "", "synonyms": "", "antonyms": ""
    }

    # ── Noun detection ──
    noun_match = re.match(r'^(der|die|das)\s+(\S+?)(?:,\s*(.+?))?(?:\s+\d+\.|\s*$)', first)
    if noun_match:
        entry["article"] = noun_match.group(1)
        entry["word"] = noun_match.group(2).rstrip(',')
        entry["wordType"] = "noun"
        rest = noun_match.group(3) or ""

        # Parse plural from rest
        if rest:
            # Check if rest starts with plural form
            plural_match = re.match(r'^([\-–¨\w\s/()]+?)(?:\s+\d+\.|\s*$)', rest)
            if plural_match and len(plural_match.group(1)) < 20:
                entry["plural"] = plural_match.group(1).strip()
            # Extract sentence if present
            sent_match = re.search(r'(\d+\..+)', rest)
            if sent_match:
                entry["exampleSentence"] = sent_match.group(1).strip()

        # Check rest_lines for sentence
        if not entry["exampleSentence"]:
            for rl in rest_lines:
                sent_match = re.match(r'(\d+\..+)', rl)
                if sent_match:
                    entry["exampleSentence"] = sent_match.group(1).strip()
                    break

        # Build sentence from all text if not found
        if not entry["exampleSentence"]:
            # Take everything after the headword
            sent_text = all_text
            headword_end = first.find(entry["word"]) + len(entry["word"])
            if entry["plural"]:
                headword_end = first.find(entry["plural"]) + len(entry["plural"])
            remaining = first[headword_end:].strip().lstrip(',').strip()
            if remaining and not remaining[0].isdigit():
                remaining = ' '.join([remaining] + rest_lines)
            if remaining:
                entry["exampleSentence"] = remaining[:300].strip()

        return entry

    # ── Verb detection ──
    verb_match = re.match(r'^((?:sich\s+)?[a-zäöüß]+(?:en|n)),\s*(.+)$', first)
    if verb_match:
        entry["word"] = verb_match.group(1)
        entry["wordType"] = "verb"

        # Look for Partizip II in rest_lines
        for rl in rest_lines:
            pp_match = re.match(r'(hat|ist)\s+([a-zäöüß]*(?:ge)?[a-zäöüß]+(?:en|t))\b', rl)
            if pp_match:
                entry["auxiliary"] = pp_match.group(1)
                entry["partizipII"] = pp_match.group(2)
                break

        # Look for example sentence
        for rl in rest_lines:
            sent_match = re.match(r'(\d+\..+)', rl)
            if sent_match:
                entry["exampleSentence"] = sent_match.group(1).strip()
                break

        # If no sentence found, use text after grammar forms
        if not entry["exampleSentence"]:
            remaining = first[first.find(','):].strip().lstrip(',').strip()
            remaining = ' '.join([remaining] + rest_lines)
            entry["exampleSentence"] = remaining[:300].strip()

        return entry

    # ── Adjective / Adverb / Other ──
    word_match = re.match(r'^([A-ZÄÖÜa-zäöüß][-a-zäöüß]*(?:\s*\.\.\.\s*\w+)?)', first)
    if word_match:
        entry["word"] = word_match.group(1).strip().rstrip(',')

        # Determine WordType
        w = entry["word"]
        if w[0].isupper() and not w.endswith('-') and not w.startswith('z.'):
            entry["wordType"] = "noun"  # Might be overridden
        elif w.endswith(('lich', 'ig', 'los', 'bar', 'sam', 'haft', 'isch')):
            entry["wordType"] = "adj"
        elif w.endswith(('weise', 'hin', 'her', 'mals', 'wärts', 'seits')):
            entry["wordType"] = "adv"
        elif w.endswith('-') or w.endswith('…'):
            entry["wordType"] = "prefix"

        # Check rest_lines for sentence
        for rl in rest_lines:
            sent_match = re.match(r'(\d+\..+)', rl)
            if sent_match:
                entry["exampleSentence"] = sent_match.group(1).strip()
                break

        # Get sentence from remaining text
        if not entry["exampleSentence"]:
            remaining = first[len(entry["word"]):].strip().lstrip(',').strip()
            remaining = ' '.join([remaining] + rest_lines)
            if remaining:
                entry["exampleSentence"] = remaining[:300].strip()

        return entry

    return None


def process_extracted_file(filepath):
    """Read the extracted text file and parse all entries."""
    with open(filepath, 'r') as f:
        content = f.read()

    all_entries = []
    current_page = 0
    current_column = ""
    in_column = False
    entry_lines = []

    for line in content.split('\n'):
        line = line.rstrip()

        # Track page
        page_match = re.match(r'^PAGE\s+(\d+)', line)
        if page_match:
            # Process pending entry
            if entry_lines:
                entry = parse_entry_lines(entry_lines)
                if entry:
                    entry['page'] = current_page
                    entry['column'] = current_column
                    all_entries.append(entry)
                entry_lines = []
            current_page = int(page_match.group(1))
            in_column = False
            continue

        # Track column
        if line.startswith('--- LEFT COLUMN ---'):
            if entry_lines:
                entry = parse_entry_lines(entry_lines)
                if entry:
                    entry['page'] = current_page
                    entry['column'] = current_column
                    all_entries.append(entry)
                entry_lines = []
            current_column = 'left'
            in_column = True
            continue
        elif line.startswith('--- RIGHT COLUMN ---'):
            if entry_lines:
                entry = parse_entry_lines(entry_lines)
                if entry:
                    entry['page'] = current_page
                    entry['column'] = current_column
                    all_entries.append(entry)
                entry_lines = []
            current_column = 'right'
            in_column = True
            continue

        if not in_column:
            continue

        line = line.strip()
        if not line:
            continue

        # Check if this line starts a new entry
        if is_new_entry_start(line):
            if entry_lines:
                entry = parse_entry_lines(entry_lines)
                if entry:
                    entry['page'] = current_page
                    entry['column'] = current_column
                    all_entries.append(entry)
            entry_lines = [line]
        elif entry_lines:
            entry_lines.append(line)

    # Process final entry
    if entry_lines:
        entry = parse_entry_lines(entry_lines)
        if entry:
            entry['page'] = current_page
            entry['column'] = current_column
            all_entries.append(entry)

    return all_entries


def get_letter(word):
    w = word.strip()
    if w.startswith("sich "):
        w = w[5:]
    if w.startswith("ein "):
        w = w[4:]
    return w[0].upper()


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "/tmp/pages_31_104.txt"
    print(f"Processing {filepath}...")
    entries = process_extracted_file(filepath)
    print(f"Parsed {len(entries)} entries")

    # Add translations
    translated = 0
    for e in entries:
        w = e['word']
        if w in TR:
            e['english'], e['bangla'], *_ = TR[w]
            translated += 1
            # Override word type if specified
            if len(TR[w]) > 2 and TR[w][2]:
                e['wordType'] = TR[w][2]

    print(f"Translated: {translated}/{len(entries)}")

    # Show untranslated
    missing = [e for e in entries if not e['english']]
    if missing:
        print(f"\nUntranslated ({len(missing)}):")
        for e in missing[:50]:
            print(f"  {e['word']:30s} ({e['wordType']:10s}) page {e['page']} {e['column']}")

    # Group by letter
    groups = {}
    for e in entries:
        letter = get_letter(e['word'])
        groups.setdefault(letter, []).append(e)

    print(f"\nLetters found: {sorted(groups.keys())}")
    for letter in sorted(groups.keys()):
        print(f"  {letter}: {len(groups[letter])} entries")
