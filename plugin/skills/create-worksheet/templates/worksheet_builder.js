// worksheet_builder.js — reusable renderers for Ambar's CBSE Class III worksheets.
//
// Usage:
//   const B = require('<path>/worksheet_builder.js');
//   const { Packer } = require('docx');
//   const children = [];
//   children.push(...B.titleBlock("EVS", "Practice Sheet 7", "Plants Around Us", 30));
//   children.push(B.infoRow());
//   children.push(B.sectionHeader(1, "Fill in the blanks", 10));
//   fillUps.forEach((it, i) => children.push(B.fillItem(i + 1, it.parts)));
//   Packer.toBuffer(B.buildDoc(children)).then(buf => fs.writeFileSync(out, buf));

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, PageBreak,
  Table, TableRow, TableCell, WidthType, BorderStyle, ImageRun
} = require('docx');

// ---------- Style constants (locked) ----------
const COLORS_COLOR = {
  titleDark:  "1F5B2E",  // dark green
  accent:     "2E7D32",  // lighter green accent
  text:       "000000",
  muted:      "555555",
  faint:      "888888",
  headerFill: "E8F1E8",  // pale green
  chartFill:  "C8E6C9",  // medium pale green
  line:       "AAAAAA"
};
const COLORS_BW = {
  titleDark:  "333333",
  accent:     "555555",
  text:       "000000",
  muted:      "555555",
  faint:      "888888",
  headerFill: "EEEEEE",
  chartFill:  "DDDDDD",
  line:       "AAAAAA"
};
// Mutable COLORS pointer — set by setBWMode or buildDoc({bwMode: true})
let COLORS = COLORS_COLOR;
function setBWMode(on) { COLORS = on ? COLORS_BW : COLORS_COLOR; }
const FONT = "Calibri";
// A4 page: 11906 x 16838 DXA (210mm x 297mm).
// With 720 DXA (0.5") margins on each side -> content width = 10466 DXA.
const PAGE = { width: 11906, height: 16838 };
const MARGIN = 720;
const CONTENT_W = PAGE.width - 2 * MARGIN;  // 10466
const BLANK = "  _______________  ";

const NO_BORDER = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER };
const thinBorder = (color = COLORS.faint) => {
  const b = { style: BorderStyle.SINGLE, size: 4, color };
  return { top: b, bottom: b, left: b, right: b };
};

// ---------- Title + info ----------
// variant: "Practice Sheet" (default) | "Revision Sheet" | "Weekly Test"
// timeMins (optional): adds a "Time: 30 min" caption under title for Weekly Test
function titleBlock(subject, sheetLabel, chapter, totalMarks, opts = {}) {
  const variant = opts.variant || "Practice Sheet";
  const lines = [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 40 },
      children: [new TextRun({
        text: `${subject} ${variant} \u2014 ${chapter}`,
        bold: true, size: 36, color: COLORS.titleDark
      })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: opts.timeMins ? 40 : 160 },
      children: [new TextRun({
        text: `Class III  \u2022  ${sheetLabel}  \u2022  Total ${totalMarks} marks`,
        italics: true, size: 22, color: COLORS.muted
      })]
    })
  ];
  if (opts.timeMins) {
    lines.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 160 },
      children: [new TextRun({
        text: `Time: ${opts.timeMins} minutes`,
        italics: true, size: 22, color: COLORS.muted
      })]
    }));
  }
  return lines;
}

function infoRow() {
  const w = Math.floor(CONTENT_W / 4);
  const cell = (label) => new TableCell({
    borders: {
      top: NO_BORDER,
      bottom: { style: BorderStyle.SINGLE, size: 6, color: "444444" },
      left: NO_BORDER, right: NO_BORDER
    },
    width: { size: w, type: WidthType.DXA },
    margins: { top: 40, bottom: 40, left: 40, right: 40 },
    children: [new Paragraph({ spacing: { after: 0 },
      children: [new TextRun({ text: label, bold: true, size: 22 })] })]
  });
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [w, w, w, CONTENT_W - 3 * w],
    rows: [new TableRow({
      children: [cell("Name: "), cell("Roll No: "), cell("Section: "), cell("Date: ")]
    })]
  });
}

function sectionHeader(qno, title, marks) {
  return new Paragraph({
    spacing: { before: 120, after: 40 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLORS.accent, space: 1 } },
    children: [
      new TextRun({ text: `Q${qno}) `, bold: true, size: 24, color: COLORS.titleDark }),
      new TextRun({ text: title + "   ", bold: true, size: 24, color: COLORS.titleDark }),
      new TextRun({ text: `(${marks} marks)`, italics: true, size: 20, color: COLORS.muted })
    ]
  });
}

function instruction(text) {
  return new Paragraph({
    spacing: { after: 80 },
    children: [new TextRun({ text, italics: true, size: 20, color: COLORS.muted })]
  });
}

function spacer(h = 80) {
  return new Paragraph({ spacing: { after: h }, children: [new TextRun("")] });
}

// ---------- Fill in the blanks ----------
// parts alternate: text, BLANK, text, BLANK, ... (first item always a string, can be "")
// e.g. parts: ["Big, ", " and ", " plants are called ", "."]
function fillItem(idx, parts, opts = {}) {
  const size = opts.size || 22;
  const runs = [new TextRun({ text: `${idx}. `, bold: true, size })];
  parts.forEach((p, i) => {
    if (p) runs.push(new TextRun({ text: p, size }));
    if (i < parts.length - 1) runs.push(new TextRun({ text: BLANK, size }));
  });
  return new Paragraph({
    spacing: { before: 20, after: 20, line: 320 },
    children: runs
  });
}

// ---------- MCQ (2x2 grid of options) ----------
function optionCell(letter, text, width) {
  return new TableCell({
    borders: noBorders,
    width: { size: width, type: WidthType.DXA },
    margins: { top: 10, bottom: 10, left: 60, right: 60 },
    children: [new Paragraph({
      spacing: { after: 0 },
      children: [
        new TextRun({ text: `(${letter}) `, bold: true, size: 20 }),
        new TextRun({ text, size: 20 })
      ]
    })]
  });
}
function mcqBlock(idx, q, opts) {
  const letters = ["a", "b", "c", "d"];
  const half = Math.floor(CONTENT_W / 2);
  const qPara = new Paragraph({
    spacing: { before: 40, after: 10 },
    children: [
      new TextRun({ text: `${idx}. `, bold: true, size: 21 }),
      new TextRun({ text: q, size: 21 })
    ]
  });
  const table = new Table({
    width: { size: CONTENT_W - 200, type: WidthType.DXA },
    columnWidths: [half - 100, (CONTENT_W - 200) - (half - 100)],
    rows: [
      new TableRow({ children: [
        optionCell(letters[0], opts[0], half - 100),
        optionCell(letters[1], opts[1], (CONTENT_W - 200) - (half - 100))
      ]}),
      new TableRow({ children: [
        optionCell(letters[2], opts[2], half - 100),
        optionCell(letters[3], opts[3], (CONTENT_W - 200) - (half - 100))
      ]})
    ]
  });
  return [qPara, table];
}

// ---------- Match the following ----------
// left = [{ n: 1, text: "Tree" }, ...]
// right = [{ letter: "a", text: "Banyan" }, ...]
function matchTable(left, right, columnA = "Column A", columnB = "Column B") {
  const colW = Math.floor(CONTENT_W / 2);
  const rows = [
    new TableRow({ tableHeader: true, children: [
      new TableCell({
        borders: thinBorder("444444"),
        width: { size: colW, type: WidthType.DXA },
        margins: { top: 40, bottom: 40, left: 80, right: 80 },
        shading: { fill: COLORS.headerFill, type: "clear" },
        children: [new Paragraph({
          children: [new TextRun({ text: columnA, bold: true, size: 22, color: COLORS.titleDark })]
        })]
      }),
      new TableCell({
        borders: thinBorder("444444"),
        width: { size: CONTENT_W - colW, type: WidthType.DXA },
        margins: { top: 40, bottom: 40, left: 80, right: 80 },
        shading: { fill: COLORS.headerFill, type: "clear" },
        children: [new Paragraph({
          children: [new TextRun({ text: columnB, bold: true, size: 22, color: COLORS.titleDark })]
        })]
      })
    ]})
  ];
  const n = Math.max(left.length, right.length);
  for (let i = 0; i < n; i++) {
    const L = left[i] || { n: "", text: "" };
    const R = right[i] || { letter: "", text: "" };
    rows.push(new TableRow({ children: [
      new TableCell({
        borders: thinBorder(COLORS.line),
        width: { size: colW, type: WidthType.DXA },
        margins: { top: 30, bottom: 30, left: 80, right: 80 },
        children: [new Paragraph({ children: [
          new TextRun({ text: `${L.n}. `, bold: true, size: 22 }),
          new TextRun({ text: L.text, size: 22 })
        ]})]
      }),
      new TableCell({
        borders: thinBorder(COLORS.line),
        width: { size: CONTENT_W - colW, type: WidthType.DXA },
        margins: { top: 30, bottom: 30, left: 80, right: 80 },
        children: [new Paragraph({ children: [
          new TextRun({ text: `(${R.letter}) `, bold: true, size: 22 }),
          new TextRun({ text: R.text, size: 22 })
        ]})]
      })
    ]}));
  }
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [colW, CONTENT_W - colW],
    rows
  });
}

// ---------- True/False ----------
function tfItem(idx, statement) {
  return new Paragraph({
    spacing: { before: 15, after: 15 },
    children: [
      new TextRun({ text: `${idx}. `, bold: true, size: 22 }),
      new TextRun({ text: statement + "   ", size: 22 }),
      new TextRun({ text: "(  )", size: 22, bold: true })
    ]
  });
}

// ---------- Odd one out ----------
function oddOneOut(idx, options) {
  return new Paragraph({
    spacing: { before: 15, after: 15 },
    children: [
      new TextRun({ text: `${idx}. `, bold: true, size: 22 }),
      new TextRun({ text: options.join("   \u2022   "), size: 22 })
    ]
  });
}

// ---------- One-word answer (inline) ----------
function oneWordItem(idx, q) {
  return new Paragraph({
    spacing: { before: 10, after: 10, line: 300 },
    children: [
      new TextRun({ text: `${idx}. `, bold: true, size: 22 }),
      new TextRun({ text: q + "  ", size: 22 }),
      new TextRun({ text: "Ans. ", bold: true, size: 22 }),
      new TextRun({ text: "_______________________________", size: 22, color: COLORS.line })
    ]
  });
}

// ---------- Short answer (question + N lines) ----------
function shortQuestion(idx, q) {
  return new Paragraph({
    spacing: { before: 30, after: 10 },
    children: [
      new TextRun({ text: `${idx}. `, bold: true, size: 22 }),
      new TextRun({ text: q, size: 22 })
    ]
  });
}
function answerLine() {
  return new Paragraph({
    spacing: { after: 20 },
    children: [new TextRun({
      text: "_______________________________________________________________________________________________",
      color: COLORS.line, size: 22
    })]
  });
}

// ---------- Name the part (clue-based fill) ----------
// Same as fillItem — just phrase the prompt as a description.

// ---------- Draw + label (row of labelled boxes) ----------
// boxes = ["Stage 1: Seed", "Stage 2: Seedling", ...]
// heightDxa = spacing.after inside each cell's empty paragraph. Use 900 when sharing a page, 3200 for a dedicated page.
function drawBoxRow(boxes, heightDxa = 3200) {
  const n = boxes.length;
  const w = Math.floor(CONTENT_W / n);
  const cells = boxes.map((label, i) => new TableCell({
    borders: thinBorder("666666"),
    width: { size: i === n - 1 ? CONTENT_W - w * (n - 1) : w, type: WidthType.DXA },
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [
      new Paragraph({
        spacing: { after: heightDxa },
        children: [new TextRun({ text: "", size: 22 })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 20, after: 20 },
        children: [new TextRun({ text: label, bold: true, size: 22, color: COLORS.titleDark })]
      })
    ]
  }));
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: boxes.map((_, i) => i === n - 1 ? CONTENT_W - w * (n - 1) : w),
    rows: [new TableRow({ children: cells })]
  });
}

// ---------- Sort-into-groups chart ----------
// groups = ["Tree", "Shrub", "Herb", "Climber", "Creeper"]
// writingLines = number of guide lines per column (default 6)
function sortChart(groups, writingLines = 6) {
  const colW = Math.floor(CONTENT_W / groups.length);
  const sortHeader = (text) => new TableCell({
    borders: thinBorder("666666"),
    width: { size: colW, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 40, right: 40 },
    shading: { fill: COLORS.chartFill, type: "clear" },
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, bold: true, size: 26, color: COLORS.titleDark })]
    })]
  });
  const sortEmpty = () => {
    const rowBorder = {
      top: NO_BORDER, left: NO_BORDER, right: NO_BORDER,
      bottom: { style: BorderStyle.SINGLE, size: 6, color: COLORS.line }
    };
    const innerRows = [];
    for (let i = 0; i < writingLines; i++) {
      innerRows.push(new TableRow({
        height: { value: 420, rule: "atLeast" },
        children: [new TableCell({
          borders: rowBorder,
          width: { size: colW - 400, type: WidthType.DXA },
          margins: { top: 40, bottom: 40, left: 40, right: 40 },
          children: [new Paragraph({ children: [new TextRun({ text: "", size: 22 })] })]
        })]
      }));
    }
    const innerTable = new Table({
      width: { size: colW - 400, type: WidthType.DXA },
      columnWidths: [colW - 400],
      rows: innerRows
    });
    return new TableCell({
      borders: thinBorder("666666"),
      width: { size: colW, type: WidthType.DXA },
      margins: { top: 80, bottom: 80, left: 160, right: 160 },
      children: [innerTable, new Paragraph({ children: [new TextRun("")] })]
    });
  };
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: groups.map((_, i) =>
      i === groups.length - 1 ? CONTENT_W - colW * (groups.length - 1) : colW),
    rows: [
      new TableRow({ children: groups.map(sortHeader) }),
      new TableRow({ children: groups.map(sortEmpty) })
    ]
  });
}

// ---------- Label diagram (image with answer line below for identification) ----------
// Used e.g. for "identify the plant type" — image in a cell, answer line beneath.
function imageAnswerCell(imgPath, imgW, imgH, idx, cellWidth) {
  return new TableCell({
    borders: noBorders,
    width: { size: cellWidth, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 40, right: 40 },
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 100 },
        children: [new TextRun({ text: `${idx}.`, bold: true, size: 22, color: COLORS.titleDark })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120 },
        children: [new ImageRun({
          type: imgPath.endsWith(".png") ? "png" : (imgPath.endsWith(".jpg") || imgPath.endsWith(".jpeg") ? "jpg" : "svg"),
          data: fs.readFileSync(imgPath),
          transformation: { width: imgW, height: imgH },
          altText: { title: "image", description: "image", name: "image" }
        })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 0 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: "555555", space: 1 } },
        children: [new TextRun({ text: " ", size: 22 })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 20, after: 0 },
        children: [new TextRun({ text: "(Ans)", italics: true, size: 20, color: COLORS.faint })]
      })
    ]
  });
}
function imageRow(items) {
  // items = [{ imgPath, imgW, imgH }, ...]
  const n = items.length;
  const w = Math.floor(CONTENT_W / n);
  const cells = items.map((it, i) =>
    imageAnswerCell(it.imgPath, it.imgW, it.imgH, i + 1,
      i === n - 1 ? CONTENT_W - w * (n - 1) : w));
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: items.map((_, i) => i === n - 1 ? CONTENT_W - w * (n - 1) : w),
    rows: [new TableRow({ children: cells })]
  });
}

// ---------- Classify list (2-column plant → type list) ----------
// items = [{ name: "Neem", }, ...]  — for student to fill type next to each
function classifyList(items, cols = 2) {
  const colW = Math.floor(CONTENT_W / cols);
  const per = Math.ceil(items.length / cols);
  function makeCell(start, end, width) {
    const paras = [];
    for (let i = start; i < end; i++) {
      paras.push(new Paragraph({
        spacing: { before: 50, after: 50 },
        children: [
          new TextRun({ text: `${i + 1}. `, bold: true, size: 22 }),
          new TextRun({ text: items[i].name + "   \u2014   ", size: 22 }),
          new TextRun({ text: "____________________", size: 22, color: COLORS.muted })
        ]
      }));
    }
    return new TableCell({
      borders: noBorders,
      width: { size: width, type: WidthType.DXA },
      margins: { top: 20, bottom: 20, left: 60, right: 60 },
      children: paras
    });
  }
  const cells = [];
  for (let c = 0; c < cols; c++) {
    const start = c * per;
    const end = Math.min(start + per, items.length);
    cells.push(makeCell(start, end, c === cols - 1 ? CONTENT_W - colW * (cols - 1) : colW));
  }
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: Array(cols).fill(colW).map((v, i) => i === cols - 1 ? CONTENT_W - colW * (cols - 1) : colW),
    rows: [new TableRow({ children: cells })]
  });
}

// ---------- Doc assembly ----------
// opts.bwMode: true -> use greyscale palette
// NOTE: setBWMode must be called BEFORE building the children array,
// because COLORS is read at render time during children construction.
// Workflow:  B.setBWMode(true); [build children]; B.buildDoc(children)
function buildDoc(children, opts = {}) {
  if (opts.bwMode !== undefined) setBWMode(!!opts.bwMode);
  return new Document({
    styles: { default: { document: { run: { font: FONT, size: 22 } } } },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE.width, height: PAGE.height }, // A4
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }
        }
      },
      children
    }]
  });
}

// ---------- Export ----------
module.exports = {
  // constants + mode
  CONTENT_W, PAGE, MARGIN, FONT, BLANK,
  get COLORS() { return COLORS; },   // live getter — reflects current B&W mode
  setBWMode,
  // structural
  titleBlock, infoRow, sectionHeader, instruction, spacer,
  // question renderers
  fillItem,
  mcqBlock, optionCell,
  matchTable,
  tfItem,
  oddOneOut,
  oneWordItem,
  shortQuestion, answerLine,
  drawBoxRow,
  sortChart,
  imageRow, imageAnswerCell,
  classifyList,
  // doc
  buildDoc
};
