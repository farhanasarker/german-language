# German B1 Flashcards

An Anki-style spaced repetition flashcard app for learning German B1 vocabulary from the Goethe-Zertifikat B1 Wortliste. Built with Preact, TypeScript, and Vite. Includes English and Bangla translations.

## Features

- **SM-2 Spaced Repetition** — cards are scheduled using the SM-2 algorithm (same as Anki) with ease factors, intervals, and lapse tracking
- **Multiple Card Layouts** — configurable multi-sided cards with presets: Simple (Word → Meaning), Deep (3 sides), Grammar (4 sides), and Minimal (Sentence → Word)
- **Swipe & Keyboard Controls** — swipe cards to rate (→ Good, ← Again, ↑ Easy, ↓ Hard) or use keyboard shortcuts (arrow keys, number keys 0-5, Space/Enter)
- **Organized Decks** — vocabulary organized by letter (A-Z), topic (Familie, Essen, Reisen, etc.), word type (Noun, Verb, Adj), and Wortgruppen sections
- **Custom Word Lists** — paste any words to match against the full dictionary and create a study session
- **Offline-First** — all progress stored locally in IndexedDB via Dexie; no server required
- **Export/Import** — backup and restore your progress as JSON
- **Mobile-Friendly** — responsive design with touch/swipe support

## Tech Stack

- **Frontend:** Preact + TypeScript
- **Build:** Vite
- **Storage:** IndexedDB (Dexie)
- **Data Pipeline:** Python scripts (CSV → JSON)
- **Deployment:** GitHub Pages via GitHub Actions

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.12+ (for data generation)

### Install & Run

```bash
npm install
python3 data/build_data.py   # generate JSON decks from CSVs
npm run dev                  # start dev server
```

### Build for Production

```bash
npm run build
npm run preview   # preview the production build locally
```

## Project Structure

```
csv/
  alphabetisch/       # A-Z vocabulary CSVs (~2900 words)
  wortgruppen/        # Thematic word group CSVs (~370 words)
data/
  build_data.py       # CSV → JSON pipeline (generates public/data/)
  entries_*.py        # PDF extraction helpers
public/data/          # Generated JSON decks (gitignored)
src/
  app.tsx             # Main app with page routing
  srs.ts              # SM-2 spaced repetition algorithm
  storage.ts          # IndexedDB persistence (Dexie)
  cards.ts            # Card layout system & presets
  data.ts             # Deck loading from JSON
  custom-words.ts     # Custom word list matching
  components/
    DeckList.tsx      # Deck selection screen
    StudySession.tsx  # Review session with SRS
    CardFace.tsx      # Swipeable card UI
    RatingButtons.tsx # Rating input buttons
    SettingsPanel.tsx # Card layout configuration
    CustomDeck.tsx    # Custom word input
```

## Data Pipeline

Vocabulary data originates from the Goethe-Zertifikat B1 Wortliste PDF. The pipeline:

1. PDF → extracted text (via `extract_pdf.py` and helper scripts in `data/`)
2. Extracted text → structured CSVs in `csv/`
3. CSVs → JSON deck files via `python3 data/build_data.py`

Each CSV row contains: Word, Article, Plural, WordType, English, Bangla, Partizip_II, Auxiliary, Example_Sentence, Synonyms, Antonyms.

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start Vite dev server |
| `npm run build` | TypeScript check + production build |
| `npm run preview` | Preview production build |
| `npm run build:data` | Regenerate JSON decks from CSVs |
| `npm run test` | Run unit tests (Vitest) |
| `npm run test:data` | Run data pipeline tests (pytest) |

## Deployment

Pushes to `main` trigger the GitHub Actions workflow which:
1. Builds JSON data from CSVs (Python)
2. Builds the Vite app (Node)
3. Deploys to GitHub Pages
