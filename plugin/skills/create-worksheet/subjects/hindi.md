# Hindi — Subject Guide (हिंदी)

CBSE Class III Hindi — वर्णमाला, मात्राएँ, व्याकरण, और गद्यांश केंद्रित।

## Current syllabus topics (from existing work)

From the Hindi folder, these topics are already in the student's curriculum:

| Topic | File(s) |
|---|---|
| संयुक्त व्यंजन (conjunct consonants — क्ष, त्र, ज्ञ, श्र) | `Topic_1_Sanyukt_Vyanjan.docx` |
| संयुक्ताक्षर और द्वित्व व्यंजन (conjunct vs double consonants) | `Topic_2_Sanyuktakshar_Dvitva.docx` |
| ऋ की मात्रा (the ऋ vowel-sign) | `Topic_3_Ri_ki_Matra.docx` |
| र में उ / ऊ की मात्रा (rephā/रेफ forms of र + उ, ऊ) | `Topic_4_Ra_mein_U_Oo_ki_Matra.docx` |
| अनुस्वार / अनुनासिक (ं and ँ) | `Topic_5_Anusvar_Anunasik.docx` |
| गिनती १ से १० (counting) | `Topic_6_Ginti_1_to_10.docx` |
| वर्णमाला (alphabet) | `Varnmala_Practice_15_Questions.docx` |
| गद्यांश — सीखे हुए मान (comprehension) | `Unseen_Comprehension_1–5_*.docx` |

## Hindi-specific question types

Beyond the standard types in `question_catalog.md`, Hindi practice sheets lean heavily on:

### 1. गद्यांश (unseen comprehension passage)
A 4–6 line passage followed by:
- 3–4 MCQs about the passage
- 1–2 open-ended questions (requires thinking)
- विलोम शब्द (opposites) to pick from the passage

This is **the biggest-marks section** in a Hindi practice sheet (often 8–10 marks).

### 2. मात्रा लगाइए (add the matra)
Student is given a word without matra, must add the correct matra. Uses `fillItem` with clue text:

```javascript
B.fillItem(1, ["क) कषि → ", ""]);  // student writes कृषि
B.fillItem(2, ["ख) पथ्वी → ", ""]);  // student writes पृथ्वी
```

For ऋ-matra, र + उ/ऊ combinations, ं/ँ, etc.

### 3. संयुक्त व्यंजन / संयुक्ताक्षर classification
A word list with space to sort into two groups (use `sortChart` with 2 columns).

```javascript
B.sortChart(["संयुक्ताक्षर", "द्वित्व व्यंजन"], 4);
```

Word bank: सत्य, दिल्ली, अच्छा, छुट्टी, पत्ता, प्यारा

### 4. विलोम शब्द / पर्यायवाची शब्द (opposites / synonyms)
Usually `matchTable` style, or fill-in-blanks:

```javascript
B.matchTable(
  [ { n: 1, text: "शहर" }, { n: 2, text: "पुराना" } ],
  [ { letter: "a", text: "नया" }, { letter: "b", text: "गाँव" } ]
);
```

### 5. T/F with check marks (✓ / ✗)
Standard T/F but use ✓ / ✗ notation in the statement box instead of T/F:

```javascript
new Paragraph({
  children: [
    new TextRun({ text: "1. ", bold: true }),
    new TextRun({ text: "हिंदी वर्णमाला में 11 स्वर होते हैं। " }),
    new TextRun({ text: "( )", bold: true })
  ]
});
// Or use B.tfItem — the rendered box "(  )" works for ✓/✗ too
```

## Default question mix (Hindi full practice sheet)

Based on the school's actual `Full_Practice_Sheet_1.docx` format:

| Q# | Type | Marks |
|---|---|---|
| Q1 | गद्यांश (passage + MCQs + short Q + vilom) | 6–8 |
| Q2 | T/F (✓/✗) on grammar concepts | 4 |
| Q3 | संयुक्त व्यंजन se shabd banaiye (fill-ups) | 4 |
| Q4 | संयुक्ताक्षर vs द्वित्व व्यंजन (sortChart, 2 cols) | 6 |
| Q5 | ऋ की मात्रा (fill matra) | 4 |
| Q6 | र + उ/ऊ matra (fill matra) | 4 |
| Q7 | अनुस्वार / अनुनासिक (identify/apply) | 2–4 |

**Total: ~30–35 marks** fitting a single practice sheet.

## Devanagari font support

All Hindi text must render in Devanagari. Calibri supports basic Devanagari but **Mangal** or **Nirmala UI** render better on Windows. For cross-platform compatibility, **Noto Sans Devanagari** is the safe choice.

When building a Hindi worksheet, override the default font in the doc styles:

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Mangal", size: 22 } } }
  },
  sections: [...]
});
```

If Mangal is not available, fall back to `Nirmala UI` then `Noto Sans Devanagari`:

```javascript
run: { font: { name: "Mangal", eastAsia: "Nirmala UI", cs: "Noto Sans Devanagari" }, size: 22 }
```

**Test the output**: after generating, convert to PDF to verify the script renders (LibreOffice `soffice` with default fonts usually works fine).

## School header style (for Hindi)

The school's Hindi practice sheets have a top banner. Optional — can include if you want it to look exactly like what Ambar gets in class:

```
दिल्ली पब्लिक स्कूल, पूर्वी कैलाश / वसंत विहार
जूनियर शाखा, दिल्ली पब्लिक स्कूल, रामकृष्ण पुरम, नई दिल्ली
कक्षा — तीसरी हिंदी आवधिक पत्र-1 हेतु पूर्ण अभ्यास पत्र — N   सत्र — 2026-27
```

Then निर्देश — सभी प्रश्न अनिवार्य हैं |

Use at user's request only. The default green "EVS Practice Sheet" style works too.

## Folder conventions

```
Hindi/
├── Topic_N_<Name>.docx          # Per-topic practice sheets (already present)
├── Full_Practice_Sheet_N.docx   # Multi-topic paper (already present)
├── Unseen_Comprehension_N_*.docx
└── Chapter - <New Chapter>/     # If we do chapter-wise folders in future
    └── Worksheet 1 - <Title>.docx
```

For consistency going forward, put new full-practice worksheets at the top level of `Hindi/` (as the existing ones are). For deep topic-work, create a subfolder.
