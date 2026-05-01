"""
Comprehensive PDF-to-CSV extractor for Goethe B1 Wortliste.
Processes all remaining alphabetical pages (31-102) directly from PDF.
"""
import pdfplumber
import csv
import os
import re
from collections import defaultdict

PDF_PATH = "Goethe-Zertifikat_B1_Wortliste.pdf"
CSV_DIR = "csv/alphabetisch"

# ── Translation database ─────────────────────────────────────────────
# (german_word → (english, bangla, wordtype_override))
# wordtype_override is optional - used when auto-detection is wrong
TR = {}

def t(word, english, bangla, wtype=None):
    TR[word] = (english, bangla, wtype)

# ── D ────────────────────────────────────────────────────────────────
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
t("sich duschen", "to shower (oneself)", "গোসল করা (নিজে)")
t("Dusche", "shower", "শাওয়ার")
t("duzen", "to address with 'du' (informal 'you')", "তুমি বলে সম্বোধন করা")

# ── E ────────────────────────────────────────────────────────────────
t("eben", "just / exactly / flat", "এইমাত্র / ঠিক / সমতল")
t("ebenfalls", "likewise / also", "একইভাবে / আরও")
t("ebenso", "just as / likewise", "ঠিক তেমনই / একইরকম")
t("e-card", "e-card (health insurance card, Austria)", "ই-কার্ড (স্বাস্থ্য বীমা কার্ড, অস্ট্রিয়া)")
t("echt", "real / genuine / really", "আসল / খাঁটি / সত্যিই")
t("ec-Karte", "EC card / debit card", "ইসি কার্ড / ডেবিট কার্ড")
t("EC-Karte", "EC card / debit card", "ইসি কার্ড / ডেবিট কার্ড")
t("Ecke", "corner", "কোণ / কোনা")
t("Eck", "corner (Austria)", "কোণ (অস্ট্রিয়া)")
t("eckig", "angular / square / cornered", "কৌণিক / চারকোণা")
t("egal", "all the same / doesn't matter", "একই কথা / কিছু যায় আসে না")
t("Ehe", "marriage", "বিবাহ / দাম্পত্য")
t("Ehefrau", "wife", "স্ত্রী")
t("Ehemann", "husband", "স্বামী")
t("Ehepaar", "married couple", "বিবাহিত দম্পতি")
t("eher", "earlier / rather / sooner", "আগে / বরং / শীঘ্র")
t("ehrlich", "honest / honestly", "সৎ / সততার সাথে")
t("Ei", "egg", "ডিম")
t("eigen-", "own", "নিজস্ব / নিজের")
t("eigentlich", "actually / really", "আসলে / প্রকৃতপক্ষে")
t("sich eignen", "to be suitable / suited", "উপযুক্ত হওয়া")
t("eilen", "to hurry / rush", "তাড়াতাড়ি করা")
t("Eile", "hurry / haste", "তাড়াতাড়ি / ত্বরা")
t("eilig", "hurried / in a hurry", "তাড়াহুড়ো / ব্যস্ত")
t("ein-", "one / a / an", "এক / একটি")
t("Einbahnstraße", "one-way street", "একমুখী রাস্তা")
t("einbrechen", "to break in / burgle", "সিঁধ কাটা / চুরি করা")
t("Einbrecher", "burglar (male)", "চোর / সিঁধেল চোর (পুরুষ)")
t("Einbrecherin", "burglar (female)", "চোর / সিঁধেল চোর (মহিলা)")
t("Einbruch", "break-in / burglary", "সিঁধেল চুরি / ডাকাতি")
t("eindeutig", "clear / unambiguous / definite", "সুস্পষ্ট / দ্ব্যর্থহীন")
t("Eindruck", "impression", "প্রভাব / ছাপ")
t("einerseits", "on the one hand", "একদিকে / একপক্ষে")
t("einfach", "simple / easy / just", "সহজ / সরল / শুধু")
t("Einfahrt", "driveway / entrance", "প্রবেশ পথ / ড্রাইভওয়ে")
t("einfallen", "to occur / come to mind", "মনে পড়া / হঠাৎ মনে আসা")
t("Einfall", "idea / sudden thought", "আইডিয়া / হঠাৎ চিন্তা")
t("Einfluss", "influence", "প্রভাব")
t("beeinflussen", "to influence", "প্রভাবিত করা")
t("einfügen", "to insert / paste", "সন্নিবেশ করা / পেস্ট করা")
t("einführen", "to introduce / import", "প্রবর্তন করা / আমদানি করা")
t("Einführung", "introduction", "ভূমিকা / প্রবর্তন")
t("Eingang", "entrance", "প্রবেশদ্বার")
t("einheitlich", "uniform / standardized", "একই ধরনের / অভিন্ন")
t("einig-", "some / a few / agreed", "কিছু / কয়েকটি / একমত")
t("sich einigen", "to agree / come to an agreement", "একমত হওয়া / সমঝোতায় আসা")
t("einkaufen", "to shop / go shopping", "কেনাকাটা করা")
t("Einkauf", "purchase / shopping", "কেনাকাটা / ক্রয়")
t("Einkommen", "income", "আয় / ইনকাম")
t("einladen", "to invite", "আমন্ত্রণ জানানো / দাওয়াত দেওয়া")
t("Einladung", "invitation", "আমন্ত্রণ / দাওয়াত")
t("einmal", "once / one time / sometime", "একবার / কখনো")
t("einnehmen", "to take (medicine) / earn", "গ্রহণ করা (ঔষধ) / আয় করা")
t("Einnahme", "revenue / income / taking", "রাজস্ব / আয়")
t("einpacken", "to pack / wrap up", "প্যাক করা / মোড়ানো")
t("einrichten", "to furnish / set up / arrange", "সাজানো / স্থাপন করা / ব্যবস্থা করা")
t("Einrichtung", "furnishings / facility / institution", "আসবাবপত্র / প্রতিষ্ঠান")
t("einsam", "lonely / solitary", "একাকী / নিঃসঙ্গ")
t("einschalten", "to switch on / turn on", "চালু করা / অন করা")
t("einschließlich", "including / inclusive", "সহ / সমেত")
t("Einschreiben", "registered mail", "রেজিস্টার্ড ডাক")
t("einsetzen", "to insert / appoint / employ", "নিয়োগ করা / ব্যবহার করা")
t("einsteigen", "to get in / board", "উঠা / চড়া (গাড়িতে)")
t("einstellen", "to hire / adjust / set", "নিয়োগ করা / সমন্বয় করা")
t("eintragen", "to enter / register / fill in", "লিখে রাখা / নিবন্ধন করা")
t("eintreten", "to enter / join", "প্রবেশ করা / যোগদান করা")
t("Eintritt", "admission / entry", "প্রবেশ / প্রবেশ মূল্য")
t("einverstanden", "agreed / okay", "একমত / সম্মত")
t("Einwohner", "inhabitant / resident (male)", "বাসিন্দা (পুরুষ)")
t("Einwohnerin", "inhabitant / resident (female)", "বাসিন্দা (মহিলা)")
t("einzahlen", "to deposit (money)", "জমা করা (টাকা)")
t("Einzahlung", "deposit / payment", "জমা / পরিশোধ")
t("einzeln", "single / individual / one by one", "একক / আলাদা / একে একে")
t("Einzel-", "single / individual", "একক / এক-")
t("Einzelheit", "detail", "বিস্তারিত / খুঁটিনাটি")
t("einzig-", "only / sole / unique", "একমাত্র / অনন্য")
t("einziehen", "to move in / collect", "স্থানান্তরিত হওয়া / সংগ্রহ করা")
t("Eis", "ice / ice cream", "বরফ / আইসক্রিম")
t("Eisenbahn", "railway / train", "রেলপথ / ট্রেন")
t("elegant", "elegant", "অভিজাত / মার্জিত")
t("elektrisch", "electric / electrical", "বৈদ্যুতিক / ইলেকট্রিক")
t("Elektro-", "electro- / electric", "ইলেকট্রো- / বৈদ্যুতিক")
t("elektronisch", "electronic", "ইলেকট্রনিক")
t("Eltern", "parents", "পিতামাতা / মা-বাবা")
t("empfangen", "to receive", "গ্রহণ করা / পাওয়া")
t("Empfang", "reception / receipt", "অভ্যর্থনা / প্রাপ্তি")
t("Empfänger", "recipient / receiver", "প্রাপক / গ্রাহক")
t("empfehlen", "to recommend", "সুপারিশ করা")
t("Empfehlung", "recommendation", "সুপারিশ")
t("enden", "to end / finish", "শেষ হওয়া / সমাপ্ত হওয়া")
t("Ende", "end", "শেষ / সমাপ্তি")
t("endgültig", "final / definitive", "চূড়ান্ত / চুড়ান্ত")
t("endlich", "finally / at last", "অবশেষে / শেষ পর্যন্ত")
t("Energie", "energy", "শক্তি / এনার্জি")
t("eng", "narrow / tight / close", "সংকীর্ণ / ঘনিষ্ঠ / আঁট")
t("Enkel", "grandson (male)", "নাতি (পুরুষ)")
t("Enkelin", "granddaughter (female)", "নাতনি (মহিলা)")
t("entdecken", "to discover", "আবিষ্কার করা")
t("entfernen", "to remove / delete", "অপসারণ করা / দূর করা")
t("Entfernung", "distance / removal", "দূরত্ব / অপসারণ")
t("entgegenkommen", "to come towards / accommodate", "সামনে আসা / ছাড় দেওয়া")
t("enthalten", "to contain", "ধারণ করা / থাকা")
t("entlang", "along", "বরাবর / ধরে")
t("entlassen", "to dismiss / discharge / fire", "ছেড়ে দেওয়া / বরখাস্ত করা")
t("Entlassung", "dismissal / discharge", "বরখাস্ত / মুক্তি")
t("entscheiden", "to decide", "সিদ্ধান্ত নেওয়া / স্থির করা")
t("Entscheidung", "decision", "সিদ্ধান্ত")
t("unentschieden", "undecided / tied (sports)", "অনিশ্চিত / অমীমাংসিত")
t("sich entschließen", "to decide / resolve", "সিদ্ধান্ত নেওয়া / সংকল্প করা")
t("entschlossen", "determined / resolute", "দৃঢ়প্রতিজ্ঞ / সংকল্পবদ্ধ")
t("entschuldigen", "to excuse / apologize", "ক্ষমা করা / মাফ চাওয়া")
t("Entschuldigung", "apology / excuse / sorry", "ক্ষমা / দুঃখিত")
t("entsorgen", "to dispose of", "নিষ্পত্তি করা / ফেলা")
t("entspannend", "relaxing", "আরামদায়ক / শিথিলকর")
t("entstehen", "to arise / originate / be created", "সৃষ্টি হওয়া / উৎপন্ন হওয়া")
t("enttäuschen", "to disappoint", "হতাশ করা / নিরাশ করা")
t("Enttäuschung", "disappointment", "হতাশা / নিরাশা")
t("entweder ... oder", "either ... or", "হয় ... অথবা")
t("entwickeln", "to develop", "উন্নয়ন করা / বিকাশ করা")
t("Entwicklung", "development", "উন্নয়ন / বিকাশ")
t("Erde", "earth / ground / soil", "পৃথিবী / মাটি")
t("Erdapfel", "potato (Austria)", "আলু (অস্ট্রিয়া)")
t("Erdgeschoss", "ground floor", "নিচতলা / গ্রাউন্ড ফ্লোর")
t("Ergeschoß", "ground floor (Austria)", "নিচতলা (অস্ট্রিয়া)")
t("Ereignis", "event / occurrence", "ঘটনা / ঘটনাবলী")
t("sich ereignen", "to happen / occur", "ঘটা / ঘটে যাওয়া")
t("erfahren", "to learn / find out / experience", "জানা / অভিজ্ঞতা অর্জন করা")
t("Erfahrung", "experience", "অভিজ্ঞতা")
t("erfinden", "to invent", "উদ্ভাবন করা")
t("Erfindung", "invention", "উদ্ভাবন")

# I'll continue building this dictionary. Let me also build the parse-and-generate function.
# The key idea: for each page, extract all word entries with grammatical info from the PDF,
# then match against TR for translations.

def extract_word_entries_from_pages(start_page, end_page):
    """Extract structured word entries from PDF pages."""
    entries = []
    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num in range(start_page - 1, end_page):
            if page_num >= len(pdf.pages):
                break
            page = pdf.pages[page_num]
            words = page.extract_words(keep_blank_chars=True, x_tolerance=3)

            # Separate left/right columns
            left_words = []
            right_words = []
            for w in words:
                entry = {"text": w["text"], "x0": round(w["x0"], 1), "top": round(w["top"], 1)}
                if w["x0"] < 300:
                    left_words.append(entry)
                else:
                    right_words.append(entry)

            for col_words, column in [(left_words, "left"), (right_words, "right")]:
                if not col_words:
                    continue
                col_words = sorted(col_words, key=lambda w: (w["top"], w["x0"]))
                lines = []
                current_line = [col_words[0]]
                current_top = col_words[0]["top"]
                for w in col_words[1:]:
                    if abs(w["top"] - current_top) <= 6:
                        current_line.append(w)
                    else:
                        lines.append((current_top, " ".join(w["text"] for w in current_line)))
                        current_line = [w]
                        current_top = w["top"]
                lines.append((current_top, " ".join(w["text"] for w in current_line)))

                # Now parse lines into entries
                # This is the hard part - we need to group related lines
                i = 0
                while i < len(lines):
                    top, text = lines[i]
                    text = text.strip()

                    # Skip headers/footers
                    if text in ("WORTLISTE", "ZERTIFIKAT B1", "30_SV") or text.isdigit():
                        i += 1
                        continue
                    if re.match(r'^\d+\s*WORTLISTE', text):
                        i += 1
                        continue

                    # Detect entry type
                    # Noun: starts with article (der/die/das)
                    noun_match = re.match(r'^(der|die|das)\s+(\S.+?)(?:,\s*(.+?))?\s*$', text)
                    if noun_match:
                        article = noun_match.group(1)
                        rest = noun_match.group(2)
                        plural = noun_match.group(3) or ""
                        word = rest.rstrip(",")

                        # Look ahead for example sentences
                        sentences = []
                        j = i + 1
                        while j < len(lines):
                            nt, ntext = lines[j][1].strip()
                            # Stop if next line looks like a new entry
                            if re.match(r'^(der|die|das)\s', ntext) or re.match(r'^[a-zäöüß]+(en|n)?,?\s+[a-zäöüß]', ntext):
                                break
                            if re.match(r'^\d+\.', ntext) or not re.match(r'^(der|die|das|WORTLISTE|30_SV|\d)', ntext):
                                if ntext and ntext[0].isdigit() and '. ' in ntext[:4]:
                                    sentences.append(ntext)
                                elif sentences:
                                    sentences[-1] += " " + ntext
                                else:
                                    sentences.append(ntext)
                            j += 1

                        sentence = sentences[0] if sentences else ""
                        i = j if sentences else i + 1

                        entries.append({
                            "word": word, "article": article, "plural": plural,
                            "wordType": "noun", "sentence": sentence,
                            "partizipII": "", "auxiliary": "", "column": column,
                            "page": page_num + 1
                        })
                        continue

                    # Verb: pattern like "word, 3sg, past," or "word, 3sg, past, participle"
                    verb_match = re.match(r'^(sich\s+)?([a-zäöüß]+(?:en|n)),\s*([a-zäöüß]+(?:,|\s|$))', text)
                    if verb_match:
                        is_reflexive = verb_match.group(1) is not None
                        word = (verb_match.group(1) or "") + verb_match.group(2)

                        # Look for Partizip II and auxiliary on next line
                        partizip = ""
                        auxiliary = ""
                        sentences = []
                        j = i + 1
                        while j < len(lines) and j < i + 5:
                            nt, ntext = lines[j][1].strip()
                            # Check for participle line
                            pp_match = re.match(r'(hat|ist)\s+([a-zäöüß]+(?:en|t))', ntext)
                            if pp_match:
                                auxiliary = pp_match.group(1)
                                partizip = pp_match.group(2)
                            # Check for example sentences
                            if re.match(r'^\d+\.', ntext):
                                sentences.append(ntext)
                            elif sentences and not re.match(r'^(der|die|das)\s', ntext) and not re.match(r'^[a-zäöüß]+(en|n)?,', ntext):
                                sentences[-1] += " " + ntext
                            else:
                                # Check if this line starts a new entry
                                if re.match(r'^(der|die|das)\s', ntext) or re.match(r'^[a-zäöüß]+(en|n)?,\s*[a-zäöüß]', ntext):
                                    break
                            j += 1

                        sentence = sentences[0] if sentences else ""
                        i = j if (sentences or partizip) else i + 1

                        entries.append({
                            "word": word, "article": "", "plural": "",
                            "wordType": "verb", "sentence": sentence,
                            "partizipII": partizip, "auxiliary": auxiliary,
                            "column": column, "page": page_num + 1
                        })
                        continue

                    # Adjective/adverb/etc
                    if text and not text[0].isdigit():
                        word_match = re.match(r'^([a-zäöüßA-ZÄÖÜ].+?)$', text)
                        if word_match:
                            word = word_match.group(1).rstrip(",")
                            # Skip if it's a continuation
                            if len(word) < 3 and word.lower() not in ('da', 'ei', 'zu'):
                                i += 1
                                continue
                            entries.append({
                                "word": word, "article": "", "plural": "",
                                "wordType": "unknown", "sentence": "",
                                "partizipII": "", "auxiliary": "",
                                "column": column, "page": page_num + 1
                            })

                    i += 1

    return entries

if __name__ == "__main__":
    # Test extraction
    entries = extract_word_entries_from_pages(31, 35)
    print(f"Extracted {len(entries)} entries from pages 31-35")

    # Show sample
    for e in entries[:20]:
        print(f"  {e['article']} {e['word']} ({e['wordType']}) - {e['sentence'][:60]}")

    # Count by type
    from collections import Counter
    types = Counter(e['wordType'] for e in entries)
    print(f"\nTypes: {dict(types)}")
