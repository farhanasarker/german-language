"""Fix CSV quality issues: missing English, WordType, and shifted Bangla fields."""
import csv
from pathlib import Path

BASE = Path(__file__).parent.parent / "csv" / "wortgruppen"

# line_number -> (english, wordtype, bangla)
FIXES = {
    "1.1_Abkuerzungen.csv": {
        5:  ("respectively", "abbreviation", "যথাক্রমে"),
        6:  ("approximately", "abbreviation", "আনুমানিক"),
        7:  ("that is / i.e.", "abbreviation", "অর্থাৎ"),
        9:  ("ground floor", "abbreviation", "নিচতলা"),
        10: ("upper floor", "abbreviation", "উপরতলা"),
        11: ("basement", "abbreviation", "বেসমেন্ট"),
        12: ("etc. / and so on", "abbreviation", "ইত্যাদি"),
        13: ("ICE (Inter City Express)", "abbreviation", "আইসিই (হাই-স্পিড ট্রেন)"),
        20: ("etc. / and so on", "abbreviation", "ইত্যাদি"),
        21: ("compare / cf.", "abbreviation", "তুলনা করুন"),
        24: ("for example", "abbreviation", "উদাহরণস্বরূপ"),
    },

    "1.2_Anglizismen.csv": {
        8:  ("to blog", "verb", "ব্লগ করা"),
        10: ("to camp", "verb", "ক্যাম্প করা"),
        14: ("to chat", "verb", "চ্যাট করা"),
        15: ("to check", "verb", "চেক করা"),
        22: ("cool", "adj", "দুর্দান্ত"),
        27: ("to fax", "verb", "ফ্যাক্স করা"),
        29: ("fit", "adj", "ফিট / সুস্থ"),
        31: ("global", "adj", "বৈশ্বিক"),
        32: ("to google", "verb", "গুগল করা"),
        39: ("to work a side job", "verb", "খণ্ডকালীন কাজ করা"),
        40: ("to jog", "verb", "জগিং করা"),
        45: ("live", "adj", "সরাসরি / লাইভ"),
        48: ("to email", "verb", "ইমেইল করা"),
        52: ("okay", "adj", "ঠিক আছে"),
        53: ("online", "adj", "অনলাইন"),
        65: ("to surf", "verb", "সার্ফ করা"),
        73: ("to tweet", "verb", "টুইট করা"),
    },

    "1.3_Anweisungssprache.csv": {
        3:  ("to tick / check off", "verb", "টিক চিহ্ন দেওয়া"),
        12: ("to solve", "verb", "সমাধান করা"),
        21: ("to transfer", "verb", "স্থানান্তর করা"),
        22: ("to assign / match", "verb", "মিল করা / নির্ধারণ করা"),
    },

    "1.6_Schulnoten.csv": {
        2:  ("very good (grade 1)",  "grade",  "খুব ভালো (গ্রেড ১)"),
        3:  ("good (grade 2)",       "grade",  "ভালো (গ্রেড ২)"),
        4:  ("satisfactory (grade 3)", "grade", "সন্তোষজনক (গ্রেড ৩)"),
        5:  ("sufficient (grade 4)", "grade",  "পর্যাপ্ত (গ্রেড ৪)"),
        6:  ("deficient (grade 5)",  "grade",  "অপ্রতুল (গ্রেড ৫)"),
        7:  ("insufficient (grade 6)", "grade", "অপর্যাপ্ত (গ্রেড ৬)"),
        8:  ("sufficient",           "adj",    "পর্যাপ্ত"),
        9:  ("insufficient",         "adj",    "অপর্যাপ্ত"),
        10: ("bad",                  "adj",    "খারাপ"),
        11: ("very bad",             "adj",    "খুব খারাপ"),
    },

    "1.7_Farben.csv": {
        2:  ("blue",   "adj", "নীল"),
        3:  ("brown",  "adj", "বাদামি"),
        4:  ("yellow", "adj", "হলুদ"),
        5:  ("gray",   "adj", "ধূসর"),
        6:  ("green",  "adj", "সবুজ"),
        7:  ("purple", "adj", "বেগুনি"),
        8:  ("orange", "adj", "কমলা"),
        9:  ("pink",   "adj", "গোলাপি"),
        10: ("red",    "adj", "লাল"),
        11: ("black",  "adj", "কালো"),
        12: ("violet", "adj", "ভায়োলেট"),
        13: ("white",  "adj", "সাদা"),
        14: ("light-", "prefix", "হালকা-"),
        15: ("dark-",  "prefix", "গাঢ়-"),
    },

    "1.9_Laender_Kontinente.csv": {
        5:  ("German",              "adj",  "জার্মান"),
        10: ("Austrian",            "adj",  "অস্ট্রীয়"),
        14: ("Swiss",               "adj",  "সুইস"),
        15: ("Swiss (person)",      "noun", "সুইস (ব্যক্তি)"),
        19: ("European",            "adj",  "ইউরোপীয়"),
        23: ("Greek",               "adj",  "গ্রিক"),
        28: ("Turkish",             "adj",  "তুর্কি"),
        33: ("Ukrainian",           "adj",  "ইউক্রেনীয়"),
    },

    "1.12_Waehrungen_Masse_Gewichte.csv": {
        17: ("kilometers per hour", "noun", "কিলোমিটার প্রতি ঘণ্টা"),
        18: ("plus",                "preposition/conjunction", "যোগ"),
        19: ("minus",               "preposition/conjunction", "বিয়োগ"),
        20: ("half",                "adj",  "অর্ধেক"),
    },

    "1.13_Zahlen_Bruchzahlen.csv": {
        2:  ("one",            "numeral", "এক"),
        3:  ("two",            "numeral", "দুই"),
        4:  ("three",          "numeral", "তিন"),
        5:  ("four",           "numeral", "চার"),
        6:  ("five",           "numeral", "পাঁচ"),
        7:  ("six",            "numeral", "ছয়"),
        8:  ("seven",          "numeral", "সাত"),
        9:  ("eight",          "numeral", "আট"),
        10: ("nine",           "numeral", "নয়"),
        11: ("ten",            "numeral", "দশ"),
        12: ("eleven",         "numeral", "এগারো"),
        13: ("twelve",         "numeral", "বারো"),
        14: ("thirteen",       "numeral", "তেরো"),
        15: ("fourteen",       "numeral", "চৌদ্দ"),
        16: ("fifteen",        "numeral", "পনেরো"),
        17: ("sixteen",        "numeral", "ষোল"),
        18: ("seventeen",      "numeral", "সতেরো"),
        19: ("eighteen",       "numeral", "আঠারো"),
        20: ("nineteen",       "numeral", "উনিশ"),
        21: ("twenty",         "numeral", "বিশ"),
        22: ("twenty-one",     "numeral", "একুশ"),
        23: ("thirty",         "numeral", "ত্রিশ"),
        24: ("one hundred",    "numeral", "একশো"),
        25: ("one thousand",   "numeral", "এক হাজার"),
        26: ("one million",    "numeral", "এক মিলিয়ন"),
        27: ("one billion",    "numeral", "এক বিলিয়ন"),
        28: ("first",          "numeral", "প্রথম"),
        29: ("second",         "numeral", "দ্বিতীয়"),
        30: ("third",          "numeral", "তৃতীয়"),
        31: ("fourth",         "numeral", "চতুর্থ"),
        32: ("firstly",        "adverb",  "প্রথমত"),
        33: ("secondly",       "adverb",  "দ্বিতীয়ত"),
        34: ("thirdly",        "adverb",  "তৃতীয়ত"),
        35: ("once",           "adverb",  "একবার"),
        36: ("twice",          "adverb",  "দুইবার"),
        37: ("three times",    "adverb",  "তিনবার"),
        38: ("simple / single", "adj",    "সহজ / একক"),
        39: ("double / twofold", "adj",   "দ্বিগুণ"),
    },
}


def fix_file(filename):
    filepath = BASE / filename
    fixes = FIXES.get(filename, {})
    if not fixes:
        return

    rows = []
    with open(filepath, "r", newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        for i, row in enumerate(reader, start=2):
            if i in fixes:
                english_val, wordtype_val, bangla_val = fixes[i]
                # Pad row to match header length
                while len(row) < len(header):
                    row.append("")
                # Set WordType[3], English[4], Bangla[5]
                if len(row) > 5:
                    row[5] = bangla_val
                if len(row) > 4:
                    row[4] = english_val
                if len(row) > 3:
                    row[3] = wordtype_val
                # Clear Partizip_II[6] if it has Bengali (shifted data)
                if len(row) > 6:
                    p2 = row[6].strip()
                    if p2 and any(0x0980 <= ord(c) <= 0x09FF for c in p2):
                        row[6] = ""
            rows.append(row)

    with open(filepath, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)

    print(f"  Fixed {len(fixes)} rows in {filename}")


def main():
    for filename in sorted(FIXES.keys()):
        filepath = BASE / filename
        if filepath.exists():
            fix_file(filename)
        else:
            print(f"  SKIP {filename} — file not found")

    print("\nDone. Run 'python3 data/build_data.py' to rebuild JSON.")


if __name__ == "__main__":
    main()
