import { useState, useEffect } from "preact/hooks";
import { db } from "../storage";
import type { SRSCard } from "../srs";

interface StatsData {
  totalCards: number;
  studiedCards: number;
  masteredCards: number;
  learningCards: number;
  newCards: number;
  dueNow: number;
  todayReviewed: number;
  weekReviewed: number;
  streak: number;
  averageEase: number;
  totalLapses: number;
}

export function Stats({ onClose }: { onClose: () => void }) {
  const [stats, setStats] = useState<StatsData | null>(null);

  useEffect(() => {
    computeStats().then(setStats);
  }, []);

  if (!stats) {
    return (
      <div style={{ textAlign: "center", padding: 40 }}>
        <p>Loading stats...</p>
      </div>
    );
  }

  const studiedPct = stats.totalCards > 0 ? (stats.studiedCards / stats.totalCards) * 100 : 0;
  const masteredPct = stats.totalCards > 0 ? (stats.masteredCards / stats.totalCards) * 100 : 0;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <h2 style={{ fontSize: "1.2rem" }}>Progress</h2>
        <button class="secondary" onClick={onClose} style={{ padding: "6px 14px", fontSize: "0.85rem" }}>
          Back
        </button>
      </div>

      {/* Streak & Today */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10, marginBottom: 20 }}>
        <StatBox label="Streak" value={`${stats.streak}d`} color="#f59e0b" />
        <StatBox label="Today" value={String(stats.todayReviewed)} color="#2563eb" />
        <StatBox label="This Week" value={String(stats.weekReviewed)} color="#8b5cf6" />
      </div>

      {/* Overall progress bar */}
      <div style={{ marginBottom: 20, padding: 16, background: "#fff", borderRadius: 12, border: "1px solid #e5e7eb" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8, fontSize: "0.85rem" }}>
          <span style={{ fontWeight: 600 }}>Overall Progress</span>
          <span style={{ color: "#6b7280" }}>{stats.studiedCards} / {stats.totalCards} words</span>
        </div>
        <div style={{ height: 12, background: "#f3f4f6", borderRadius: 6, overflow: "hidden" }}>
          <div style={{ height: "100%", display: "flex" }}>
            <div style={{ width: `${masteredPct}%`, background: "#16a34a", transition: "width 0.5s" }} />
            <div style={{ width: `${studiedPct - masteredPct}%`, background: "#2563eb", transition: "width 0.5s" }} />
          </div>
        </div>
        <div style={{ display: "flex", gap: 16, marginTop: 8, fontSize: "0.75rem", color: "#6b7280" }}>
          <span><span style={{ display: "inline-block", width: 8, height: 8, borderRadius: "50%", background: "#16a34a", marginRight: 4 }} />Mastered ({stats.masteredCards})</span>
          <span><span style={{ display: "inline-block", width: 8, height: 8, borderRadius: "50%", background: "#2563eb", marginRight: 4 }} />Learning ({stats.learningCards})</span>
          <span><span style={{ display: "inline-block", width: 8, height: 8, borderRadius: "50%", background: "#f3f4f6", marginRight: 4, border: "1px solid #d1d5db" }} />New ({stats.newCards})</span>
        </div>
      </div>

      {/* Detail cards */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <StatBox label="Due Now" value={String(stats.dueNow)} color="#dc2626" />
        <StatBox label="Avg Ease" value={stats.averageEase.toFixed(2)} color="#16a34a" />
        <StatBox label="Total Lapses" value={String(stats.totalLapses)} color="#ea580c" />
        <StatBox label="Mastered" value={`${Math.round(masteredPct)}%`} color="#16a34a" />
      </div>
    </div>
  );
}

function StatBox({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div
      style={{
        padding: "14px 12px",
        background: "#fff",
        borderRadius: 12,
        border: "1px solid #e5e7eb",
        textAlign: "center",
      }}
    >
      <div style={{ fontSize: "1.4rem", fontWeight: 700, color }}>{value}</div>
      <div style={{ fontSize: "0.75rem", color: "#6b7280", marginTop: 2 }}>{label}</div>
    </div>
  );
}

async function computeStats(): Promise<StatsData> {
  const allCards = await db.srsCards.toArray();
  const now = Date.now();
  const todayStart = startOfDay(now);
  const weekStart = todayStart - 6 * 24 * 60 * 60 * 1000;

  const totalCards = allCards.length;
  const studiedCards = allCards.filter((c) => c.repetitions > 0 || c.lastReview > 0).length;
  const masteredCards = allCards.filter((c) => c.interval >= 21).length;
  const learningCards = studiedCards - masteredCards;
  const newCards = totalCards - studiedCards;
  const dueNow = allCards.filter((c) => c.nextReview <= now).length;
  const todayReviewed = allCards.filter((c) => c.lastReview >= todayStart).length;
  const weekReviewed = allCards.filter((c) => c.lastReview >= weekStart).length;
  const totalLapses = allCards.reduce((sum, c) => sum + c.lapses, 0);
  const averageEase = totalCards > 0
    ? allCards.reduce((sum, c) => sum + c.easeFactor, 0) / totalCards
    : 2.5;

  const streak = computeStreak(allCards, todayStart);

  return {
    totalCards,
    studiedCards,
    masteredCards,
    learningCards,
    newCards,
    dueNow,
    todayReviewed,
    weekReviewed,
    streak,
    averageEase,
    totalLapses,
  };
}

function startOfDay(ts: number): number {
  const d = new Date(ts);
  d.setHours(0, 0, 0, 0);
  return d.getTime();
}

function computeStreak(cards: SRSCard[], todayStart: number): number {
  const reviewDays = new Set<number>();
  for (const card of cards) {
    if (card.lastReview > 0) {
      reviewDays.add(startOfDay(card.lastReview));
    }
  }

  let streak = 0;
  let day = todayStart;

  while (reviewDays.has(day)) {
    streak++;
    day -= 24 * 60 * 60 * 1000;
  }

  return streak;
}
