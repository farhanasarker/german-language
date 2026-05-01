"""Tests for build_data.py — CSV parsing and JSON generation."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_data import normalize_row, generate_id, deck_id_to_name


class TestNormalizeRow:
    def test_normalizes_keys_to_lowercase(self):
        row = {
            "Word": "Tisch", "Article": "der", "Plural": "-e",
            "WordType": "noun", "English": "table", "Bangla": "টেবিল",
            "Partizip_II": "", "Auxiliary": "",
            "Example_Sentence": "Der Tisch ist aus Holz.",
            "Synonyms": "", "Antonyms": "", "ID": "", "Tags": "Wohnen",
        }
        result = normalize_row(row)
        assert result["word"] == "Tisch"
        assert result["article"] == "der"
        assert result["english"] == "table"
        assert result["bangla"] == "টেবিল"
        assert result["partizipII"] == ""
        assert result["tags"] == "Wohnen"

    def test_handles_missing_fields(self):
        row = {"Word": "Haus"}
        result = normalize_row(row)
        assert result["word"] == "Haus"
        assert result["article"] == ""

    def test_strips_whitespace(self):
        row = {"Word": "  Tisch  ", "Article": " der "}
        result = normalize_row(row)
        assert result["word"] == "Tisch"
        assert result["article"] == "der"


class TestGenerateId:
    def test_zero_padded(self):
        assert generate_id("WG", 0) == "WG-0000"
        assert generate_id("WG", 42) == "WG-0042"

    def test_long_prefix(self):
        assert generate_id("1.10", 5) == "1.10-0005"


class TestDeckIdToName:
    def test_wortgruppe(self):
        result = deck_id_to_name("wg-1-1", [{}])
        assert "Wortgruppe" in result

    def test_letter(self):
        assert deck_id_to_name("letter-a", [{}]) == "Letter: A"

    def test_tag(self):
        assert deck_id_to_name("tag-essen", [{}]) == "Topic: Essen"

    def test_type(self):
        assert deck_id_to_name("type-noun", [{}]) == "Type: Noun"

    def test_all(self):
        assert deck_id_to_name("all", [{}]) == "All Words"
