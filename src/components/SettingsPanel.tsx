import { useState, useEffect } from "preact/hooks";
import type { CardSettings, CardSideConfig } from "../cards";
import { ALL_FIELDS, PRESETS } from "../cards";
import { getCardSettings, saveCardSettings } from "../storage";

interface Props {
  onClose: () => void;
}

export function SettingsPanel({ onClose }: Props) {
  const [settings, setSettings] = useState<CardSettings | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    getCardSettings().then(setSettings);
  }, []);

  if (!settings) {
    return (
      <div style={{ textAlign: "center", padding: 40 }}>
        <p>Loading settings…</p>
      </div>
    );
  }

  const toggleField = (sideIdx: number, fieldKey: string) => {
    const updated = { ...settings };
    const side = { ...updated.sides[sideIdx] };
    const fields = [...side.fields];
    const idx = fields.indexOf(fieldKey as any);
    if (idx >= 0) {
      fields.splice(idx, 1);
    } else {
      fields.push(fieldKey as any);
    }
    side.fields = fields;
    updated.sides = [...updated.sides];
    updated.sides[sideIdx] = side;
    setSettings(updated);
  };

  const addSide = () => {
    if (settings.sides.length >= 5) return;
    const updated = { ...settings, name: "Custom" };
    updated.sides = [...settings.sides, { label: `Side ${settings.sides.length + 1}`, fields: [] }];
    setSettings(updated);
  };

  const removeSide = (idx: number) => {
    if (settings.sides.length <= 1) return;
    const updated = { ...settings, name: "Custom" };
    updated.sides = settings.sides.filter((_, i) => i !== idx);
    setSettings(updated);
  };

  const updateSideLabel = (idx: number, label: string) => {
    const updated = { ...settings, name: "Custom" };
    updated.sides = [...updated.sides];
    updated.sides[idx] = { ...updated.sides[idx], label };
    setSettings(updated);
  };

  const loadPreset = (key: string) => {
    const preset = PRESETS[key];
    if (preset) setSettings({ ...preset });
  };

  const handleSave = async () => {
    await saveCardSettings(settings);
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <h2 style={{ fontSize: "1.2rem" }}>Card Settings</h2>
        <button class="secondary" onClick={onClose} style={{ padding: "6px 14px", fontSize: "0.85rem" }}>
          Back
        </button>
      </div>

      {/* Presets */}
      <div style={{ marginBottom: 20 }}>
        <p style={{ fontSize: "0.8rem", color: "#6b7280", marginBottom: 8 }}>Presets</p>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {Object.entries(PRESETS).map(([key, preset]) => (
            <button
              key={key}
              class="secondary"
              onClick={() => loadPreset(key)}
              style={{
                padding: "6px 14px",
                fontSize: "0.8rem",
                background: settings.name === preset.name ? "#2563eb" : "#e5e7eb",
                color: settings.name === preset.name ? "#fff" : "#374151",
              }}
            >
              {preset.name}
            </button>
          ))}
        </div>
      </div>

      {/* Sides configuration */}
      <p style={{ fontSize: "0.8rem", color: "#6b7280", marginBottom: 12 }}>
        Configure each side — check which fields to show on that side.
      </p>

      {settings.sides.map((side, si) => (
        <div
          key={si}
          style={{
            marginBottom: 16,
            padding: 16,
            background: "#fff",
            borderRadius: 12,
            border: "1px solid #e5e7eb",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
            <span
              style={{
                width: 28,
                height: 28,
                borderRadius: "50%",
                background: "#2563eb",
                color: "#fff",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "0.8rem",
                fontWeight: 700,
              }}
            >
              {si + 1}
            </span>
            <input
              type="text"
              value={side.label}
              onInput={(e) => updateSideLabel(si, (e.target as HTMLInputElement).value)}
              style={{
                flex: 1,
                padding: "4px 10px",
                borderRadius: 6,
                border: "1px solid #e5e7eb",
                fontSize: "0.9rem",
                fontFamily: "inherit",
              }}
            />
            {settings.sides.length > 1 && (
              <button
                onClick={() => removeSide(si)}
                style={{
                  background: "#fef2f2",
                  color: "#dc2626",
                  border: "none",
                  padding: "4px 10px",
                  borderRadius: 6,
                  fontSize: "0.75rem",
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                ✕
              </button>
            )}
          </div>

          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {ALL_FIELDS.map((field) => {
              const checked = side.fields.includes(field.key);
              return (
                <button
                  key={field.key}
                  onClick={() => toggleField(si, field.key)}
                  style={{
                    padding: "4px 10px",
                    borderRadius: 16,
                    fontSize: "0.75rem",
                    fontWeight: 500,
                    background: checked ? "#dbeafe" : "#f3f4f6",
                    color: checked ? "#1d4ed8" : "#6b7280",
                    border: checked ? "1px solid #93c5fd" : "1px solid #e5e7eb",
                    cursor: "pointer",
                  }}
                >
                  {checked ? "✓ " : "+ "}
                  {field.label}
                </button>
              );
            })}
          </div>
        </div>
      ))}

      {/* Add side button */}
      {settings.sides.length < 5 && (
        <button
          onClick={addSide}
          class="secondary"
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: 16,
            border: "2px dashed #d1d5db",
            background: "transparent",
            color: "#6b7280",
            fontSize: "0.9rem",
          }}
        >
          + Add Side ({settings.sides.length}/5)
        </button>
      )}

      {/* Save */}
      <div style={{ display: "flex", gap: 10 }}>
        <button class="primary" onClick={handleSave} style={{ flex: 1 }}>
          {saved ? "Saved!" : "Save Settings"}
        </button>
      </div>
    </div>
  );
}
