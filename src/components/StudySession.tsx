import { useState, useEffect, useCallback, useRef } from "preact/hooks";
import type { CardEntry } from "../data";
import type { Rating } from "../srs";
import { createNewCard, reviewCard, getDueCards, getNextReviewDescription } from "../srs";
import { getCardState, saveCardState, getCardSettings } from "../storage";
import type { CardSettings, CardFaceData } from "../cards";
import { renderSide, DEFAULT_SETTINGS } from "../cards";
import { CardFace, type SwipeDirection } from "./CardFace";
import { RatingButtons } from "./RatingButtons";

interface Props {
  deckId: string;
  entries: CardEntry[];
  onDone: () => void;
  forceAll?: boolean;
}

interface StudyCard {
  srs: ReturnType<typeof createNewCard>;
  entry: CardEntry;
  sides: CardFaceData[];
}

export function StudySession({ entries, onDone, forceAll }: Props) {
  const [settings, setSettings] = useState<CardSettings | null>(null);
  const [cards, setCards] = useState<StudyCard[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [currentSide, setCurrentSide] = useState(0);
  const [loading, setLoading] = useState(true);
  const [done, setDone] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Load settings
  useEffect(() => {
    getCardSettings().then((s) => {
      setSettings(s);
    });
  }, []);

  // Load cards (depends on settings for side generation)
  useEffect(() => {
    if (!settings) return;
    (async () => {
      const studyCards: StudyCard[] = [];
      for (const entry of entries) {
        let srsState = await getCardState(entry.id);
        if (!srsState) {
          srsState = createNewCard(entry.id);
          await saveCardState(srsState);
        }
        // Generate sides from settings
        const sides: CardFaceData[] = settings.sides.map((sideConfig) =>
          renderSide(entry, sideConfig.fields)
        );
        studyCards.push({ srs: srsState, entry, sides });
      }

      const due = forceAll
        ? studyCards.map((c) => c.srs)
        : getDueCards(studyCards.map((c) => c.srs));
      const dueIds = new Set(due.map((d) => d.cardId));
      const dueCards = studyCards.filter((c) => dueIds.has(c.srs.cardId));

      for (let i = dueCards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [dueCards[i], dueCards[j]] = [dueCards[j], dueCards[i]];
      }

      setCards(dueCards);
      setLoading(false);
    })();
  }, [entries, settings]);

  // Focus container
  useEffect(() => {
    containerRef.current?.focus();
  }, [currentIdx, currentSide]);

  const current = cards[currentIdx];
  const totalDue = cards.length;
  if (!current) {
    if (!loading && totalDue === 0) {
      // handled below
    }
  }

  const totalSides = settings?.sides.length ?? DEFAULT_SETTINGS.sides.length;
  const isLastSide = currentSide >= totalSides - 1;

  const advance = useCallback(
    async (rating: Rating) => {
      if (!current) return;
      const updatedSrs = reviewCard(current.srs, rating);
      await saveCardState(updatedSrs);

      if (currentIdx + 1 >= totalDue) {
        setDone(true);
      } else {
        setCurrentIdx((i) => i + 1);
        setCurrentSide(0);
      }
    },
    [current, currentIdx, totalDue]
  );

  const nextSide = useCallback(() => {
    if (isLastSide) return; // Must rate, not advance
    setCurrentSide((s) => Math.min(s + 1, totalSides - 1));
  }, [isLastSide, totalSides]);

  // Swipe on card
  const handleSwipe = useCallback(
    (direction: SwipeDirection) => {
      if (!direction) return;
      if (isLastSide) {
        const ratingMap: Record<string, Rating> = {
          left: 1, right: 4, up: 5, down: 3,
        };
        advance(ratingMap[direction]);
      } else {
        nextSide();
      }
    },
    [isLastSide, advance, nextSide]
  );

  // Keyboard
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (loading || done || !current) return;

      // Space/Enter: next side or rate Good on last
      if (e.key === " " || e.key === "Enter") {
        e.preventDefault();
        if (isLastSide) { advance(4); } else { nextSide(); }
        return;
      }

      // Arrow keys
      if (e.key === "ArrowRight") {
        e.preventDefault();
        if (isLastSide) { advance(4); } else { nextSide(); }
        return;
      }
      if (e.key === "ArrowLeft") { e.preventDefault(); advance(1); return; }
      if (e.key === "ArrowUp") { e.preventDefault(); advance(5); return; }
      if (e.key === "ArrowDown") { e.preventDefault(); advance(3); return; }

      // Number keys: rate from any side
      if (/^[0-5]$/.test(e.key)) {
        e.preventDefault();
        advance(parseInt(e.key) as Rating);
      }
    },
    [isLastSide, advance, nextSide, loading, done, current]
  );

  if (loading || !settings) {
    return (
      <div style={{ textAlign: "center", padding: "60px 20px" }}>
        <p>Preparing cards…</p>
      </div>
    );
  }

  if (done || totalDue === 0) {
    return (
      <div style={{ textAlign: "center", padding: "60px 20px" }}>
        <h2 style={{ marginBottom: 12 }}>
          {totalDue === 0 ? "All caught up!" : "Session complete!"}
        </h2>
        <p style={{ color: "#6b7280", marginBottom: 20 }}>
          {totalDue === 0
            ? "No cards are due for review right now."
            : `You reviewed ${currentIdx + 1} cards.`}
        </p>
        <button class="primary" onClick={onDone}>
          Back to Decks
        </button>
      </div>
    );
  }

  return (
    <div ref={containerRef} tabIndex={0} onKeyDown={handleKeyDown} style={{ outline: "none" }}>
      {/* Progress bar */}
      <div style={{ marginBottom: 16 }}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: 4,
            fontSize: "0.85rem",
            color: "#6b7280",
          }}
        >
          <span>
            Card {currentIdx + 1} of {totalDue}
          </span>
          <span>{settings.name}</span>
        </div>
        <div style={{ height: 4, background: "#e5e7eb", borderRadius: 2 }}>
          <div
            style={{
              height: "100%",
              width: `${((currentIdx + 1) / totalDue) * 100}%`,
              background: "#2563eb",
              borderRadius: 2,
              transition: "width 0.3s",
            }}
          />
        </div>
      </div>

      {/* Card */}
      <CardFace
        sides={current.sides}
        currentSide={currentSide}
        isLastSide={isLastSide}
        onNextSide={nextSide}
        onSwipeRate={handleSwipe}
      />

      {/* Bottom area */}
      {isLastSide ? (
        <RatingButtons onRate={advance} />
      ) : (
        <div style={{ textAlign: "center", marginTop: 16 }}>
          <button
            class="primary"
            style={{ minWidth: 200, fontSize: "1rem" }}
            onClick={nextSide}
          >
            Next Side (Space / →)
          </button>
          <div
            style={{
              marginTop: 12,
              display: "flex",
              gap: 8,
              justifyContent: "center",
              flexWrap: "wrap",
              fontSize: "0.75rem",
              color: "#9ca3af",
            }}
          >
            <span>Tap card or Space / → to advance</span>
            <span>0-5 to rate any time</span>
          </div>
        </div>
      )}

      {/* SRS info on last side */}
      {isLastSide && (
        <div style={{ textAlign: "center", marginTop: 12, fontSize: "0.8rem", color: "#6b7280" }}>
          Next: {getNextReviewDescription(current.srs.interval)} · Reps:{" "}
          {current.srs.repetitions} · Ease: {current.srs.easeFactor.toFixed(1)}
        </div>
      )}
    </div>
  );
}
