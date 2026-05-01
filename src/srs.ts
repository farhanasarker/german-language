/**
 * SM-2 spaced repetition algorithm (Anki-style).
 * All state is stored externally (IndexedDB), functions are pure.
 */

export interface SRSCard {
  cardId: string;
  easeFactor: number;   // starts 2.5, min 1.3
  interval: number;     // days
  repetitions: number;  // consecutive correct reviews
  nextReview: number;   // timestamp (ms)
  lastReview: number;   // timestamp (ms)
  lapses: number;       // total times forgotten
}

export type Rating = 0 | 1 | 2 | 3 | 4 | 5;
// 0 = complete blackout
// 1 = incorrect, but recognized answer
// 2 = incorrect, but answer felt familiar
// 3 = correct with significant difficulty
// 4 = correct with slight hesitation
// 5 = perfect recall, effortless

export function createNewCard(cardId: string): SRSCard {
  return {
    cardId,
    easeFactor: 2.5,
    interval: 0,
    repetitions: 0,
    nextReview: Date.now(), // due immediately
    lastReview: 0,
    lapses: 0,
  };
}

export function reviewCard(card: SRSCard, rating: Rating): SRSCard {
  const now = Date.now();
  const updated = { ...card, lastReview: now };

  if (rating >= 3) {
    // Correct response
    if (card.repetitions === 0) {
      updated.interval = 1;
    } else if (card.repetitions === 1) {
      updated.interval = 6;
    } else {
      updated.interval = Math.round(card.interval * card.easeFactor);
    }
    updated.repetitions = card.repetitions + 1;
  } else {
    // Forgotten
    updated.interval = 1;
    updated.repetitions = 0;
    updated.lapses = card.lapses + 1;
  }

  // Adjust ease factor
  updated.easeFactor = card.easeFactor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02));
  if (updated.easeFactor < 1.3) updated.easeFactor = 1.3;

  updated.nextReview = now + updated.interval * 24 * 60 * 60 * 1000;
  return updated;
}

export function getDueCards(cards: SRSCard[]): SRSCard[] {
  const now = Date.now();
  return cards
    .filter((c) => c.nextReview <= now)
    .sort((a, b) => a.nextReview - b.nextReview);
}

export function getNextReviewDescription(interval: number): string {
  if (interval === 0) return "now";
  if (interval === 1) return "tomorrow";
  if (interval < 30) return `${interval} days`;
  if (interval < 365) return `${Math.round(interval / 30)} months`;
  return `${Math.round(interval / 365)} years`;
}
