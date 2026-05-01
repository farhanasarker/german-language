import { describe, it, expect, vi } from "vitest";
import {
  createNewCard,
  reviewCard,
  getDueCards,
  getNextReviewDescription,
  type SRSCard,
  type Rating,
} from "../srs";

function makeCard(overrides: Partial<SRSCard> = {}): SRSCard {
  return {
    cardId: "test-001",
    easeFactor: 2.5,
    interval: 0,
    repetitions: 0,
    nextReview: Date.now(),
    lastReview: 0,
    lapses: 0,
    ...overrides,
  };
}

describe("createNewCard", () => {
  it("creates a card with default values", () => {
    const card = createNewCard("A-001");
    expect(card.cardId).toBe("A-001");
    expect(card.easeFactor).toBe(2.5);
    expect(card.interval).toBe(0);
    expect(card.repetitions).toBe(0);
    expect(card.lapses).toBe(0);
    expect(card.nextReview).toBeLessThanOrEqual(Date.now());
  });
});

describe("reviewCard", () => {
  describe("correct responses (rating >= 3)", () => {
    it("first correct: interval = 1 day", () => {
      const card = makeCard({ interval: 0, repetitions: 0 });
      const result = reviewCard(card, 4);
      expect(result.interval).toBe(1);
      expect(result.repetitions).toBe(1);
      expect(result.easeFactor).toBeGreaterThan(2.4); // slight adjustment
    });

    it("second correct: interval = 6 days", () => {
      const card = makeCard({ interval: 1, repetitions: 1, easeFactor: 2.5 });
      const result = reviewCard(card, 4);
      expect(result.interval).toBe(6);
      expect(result.repetitions).toBe(2);
    });

    it("third correct: interval = previous * easeFactor", () => {
      const card = makeCard({ interval: 6, repetitions: 2, easeFactor: 2.5 });
      const result = reviewCard(card, 4);
      expect(result.interval).toBe(15); // 6 * 2.5 = 15
      expect(result.repetitions).toBe(3);
    });

    it("increases ease factor with perfect recall", () => {
      const card = makeCard({ easeFactor: 2.5 });
      const result = reviewCard(card, 5);
      expect(result.easeFactor).toBeGreaterThan(2.5);
    });

    it("decreases ease factor with difficult recall", () => {
      const card = makeCard({ easeFactor: 2.5 });
      const result = reviewCard(card, 3);
      expect(result.easeFactor).toBeLessThan(2.5);
    });
  });

  describe("incorrect responses (rating < 3)", () => {
    it("resets interval to 1 day", () => {
      const card = makeCard({ interval: 15, repetitions: 3 });
      const result = reviewCard(card, 1);
      expect(result.interval).toBe(1);
      expect(result.repetitions).toBe(0);
      expect(result.lapses).toBe(1);
    });

    it("increments lapses count", () => {
      const card = makeCard({ lapses: 2 });
      const result = reviewCard(card, 0);
      expect(result.lapses).toBe(3);
    });
  });

  describe("ease factor", () => {
    it("never drops below 1.3", () => {
      const card = makeCard({ easeFactor: 1.3 });
      const result = reviewCard(card, 0); // worst possible rating
      expect(result.easeFactor).toBeGreaterThanOrEqual(1.3);
    });

    it("rating 5 increases ease factor", () => {
      const card = makeCard({ easeFactor: 2.0 });
      const result = reviewCard(card, 5);
      expect(result.easeFactor).toBeGreaterThan(2.0);
    });

    it("rating 3 decreases ease factor", () => {
      const card = makeCard({ easeFactor: 2.5 });
      const result = reviewCard(card, 3);
      expect(result.easeFactor).toBeLessThan(2.5);
    });
  });

  describe("nextReview", () => {
    it("schedules next review in the future", () => {
      const card = makeCard({ interval: 6, repetitions: 2, easeFactor: 2.5 });
      const before = Date.now();
      const result = reviewCard(card, 4);
      // interval = 6 * 2.5 = 15 days
      const expected = before + 15 * 24 * 60 * 60 * 1000;
      expect(result.nextReview).toBeGreaterThanOrEqual(expected - 2000);
      expect(result.nextReview).toBeLessThanOrEqual(expected + 2000);
    });

    it("sets lastReview to current time", () => {
      const before = Date.now();
      const card = makeCard();
      const result = reviewCard(card, 4);
      expect(result.lastReview).toBeGreaterThanOrEqual(before);
    });

    it("does not mutate the original card", () => {
      const card = makeCard({ interval: 6, repetitions: 2 });
      const original = { ...card };
      reviewCard(card, 4);
      expect(card.interval).toBe(original.interval);
      expect(card.repetitions).toBe(original.repetitions);
    });
  });
});

describe("getDueCards", () => {
  it("returns cards with nextReview <= now", () => {
    const now = Date.now();
    const due = makeCard({ cardId: "due", nextReview: now - 1000 });
    const notDue = makeCard({ cardId: "not-due", nextReview: now + 86400000 });
    const result = getDueCards([due, notDue]);
    expect(result).toHaveLength(1);
    expect(result[0].cardId).toBe("due");
  });

  it("sorts by nextReview ascending", () => {
    const now = Date.now();
    const a = makeCard({ cardId: "a", nextReview: now - 5000 });
    const b = makeCard({ cardId: "b", nextReview: now - 10000 });
    const result = getDueCards([a, b]);
    expect(result[0].cardId).toBe("b");
    expect(result[1].cardId).toBe("a");
  });

  it("returns empty array when no cards are due", () => {
    const now = Date.now();
    const cards = [
      makeCard({ nextReview: now + 10000 }),
      makeCard({ nextReview: now + 20000 }),
    ];
    expect(getDueCards(cards)).toHaveLength(0);
  });
});

describe("getNextReviewDescription", () => {
  it('returns "now" for interval 0', () => {
    expect(getNextReviewDescription(0)).toBe("now");
  });
  it('returns "tomorrow" for interval 1', () => {
    expect(getNextReviewDescription(1)).toBe("tomorrow");
  });
  it("returns days for interval < 30", () => {
    expect(getNextReviewDescription(15)).toBe("15 days");
  });
  it("returns months for interval >= 30 and < 365", () => {
    expect(getNextReviewDescription(60)).toBe("2 months");
  });
  it("returns years for interval >= 365", () => {
    expect(getNextReviewDescription(400)).toBe("1 years");
  });
});
