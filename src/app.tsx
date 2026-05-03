import { useState, useEffect, useCallback } from "preact/hooks";
import { DeckList } from "./components/DeckList";
import { StudySession } from "./components/StudySession";
import { SettingsPanel } from "./components/SettingsPanel";
import { CustomDeck } from "./components/CustomDeck";
import { loadDeckIndex, loadDeck, type DeckIndex, type CardEntry } from "./data";
import { exportAllProgress, importProgress } from "./storage";
import { getCustomDeckId } from "./custom-words";

type Page = "decks" | "study" | "settings" | "custom";

export function App() {
  const [page, setPage] = useState<Page>("decks");
  const [deckIndex, setDeckIndex] = useState<DeckIndex | null>(null);
  const [currentDeckId, setCurrentDeckId] = useState<string | null>(null);
  const [entries, setEntries] = useState<CardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDeckIndex()
      .then(setDeckIndex)
      .catch((e) => setError(`Failed to load decks: ${e.message}`))
      .finally(() => setLoading(false));
  }, []);

  const startStudy = useCallback(async (deckId: string) => {
    try {
      const deckEntries = await loadDeck(deckId);
      setEntries(deckEntries);
      setCurrentDeckId(deckId);
      setPage("study");
    } catch (e: any) {
      setError(`Failed to load deck: ${e.message}`);
    }
  }, []);

  const startCustomStudy = useCallback((customEntries: CardEntry[]) => {
    setEntries(customEntries);
    setCurrentDeckId(getCustomDeckId());
    setPage("study");
  }, []);

  const backToDecks = useCallback(() => {
    setPage("decks");
    setCurrentDeckId(null);
  }, []);

  const handleExport = useCallback(async () => {
    const json = await exportAllProgress();
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `german-flashcards-backup-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }, []);

  const handleImport = useCallback(async () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json";
    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (!file) return;
      const text = await file.text();
      await importProgress(text);
      alert("Progress imported successfully!");
    };
    input.click();
  }, []);

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "80px 20px" }}>
        <h2>Loading decks…</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ textAlign: "center", padding: "80px 20px" }}>
        <h2>Error</h2>
        <p style={{ color: "#dc2626", marginTop: 8 }}>{error}</p>
        <button class="primary" style={{ marginTop: 16 }} onClick={() => location.reload()}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "12px 0",
          borderBottom: "2px solid #e5e7eb",
          marginBottom: 20,
        }}
      >
        <h1 style={{ fontSize: "1.4rem", cursor: "pointer" }} onClick={backToDecks}>
          German B1 Flashcards
        </h1>
        <div style={{ display: "flex", gap: 8 }}>
          <button
            class="secondary"
            style={{ fontSize: "0.8rem", padding: "6px 12px" }}
            onClick={() => setPage(page === "custom" ? "decks" : "custom")}
          >
            {page === "custom" ? "Decks" : "Custom Words"}
          </button>
          <button
            class="secondary"
            style={{ fontSize: "0.8rem", padding: "6px 12px" }}
            onClick={() => setPage(page === "settings" ? "decks" : "settings")}
          >
            {page === "settings" ? "Decks" : "Settings"}
          </button>
          <button class="secondary" style={{ fontSize: "0.8rem", padding: "6px 12px" }} onClick={handleExport}>
            Export
          </button>
          <button class="secondary" style={{ fontSize: "0.8rem", padding: "6px 12px" }} onClick={handleImport}>
            Import
          </button>
        </div>
      </header>

      {page === "decks" && deckIndex && (
        <DeckList
          index={deckIndex}
          onSelectDeck={startStudy}
          onCustomDeck={() => setPage("custom")}
        />
      )}

      {page === "study" && currentDeckId && (
        <StudySession
          deckId={currentDeckId}
          entries={entries}
          onDone={backToDecks}
          forceAll={currentDeckId === getCustomDeckId()}
        />
      )}

      {page === "settings" && (
        <SettingsPanel onClose={() => setPage("decks")} />
      )}

      {page === "custom" && (
        <CustomDeck onStartStudy={startCustomStudy} />
      )}
    </div>
  );
}
