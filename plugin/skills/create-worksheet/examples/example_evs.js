// Example: EVS practice sheet on "Plants Around Us" using the shared builder.
// Run with: node example_evs.js
//
// Demonstrates fill-ups, MCQs, match, odd-one-out, and one-word answers.

const fs = require('fs');
const path = require('path');
const B = require('../templates/worksheet_builder.js');
const { Packer } = require('docx');

const children = [];

// Title + info row
children.push(...B.titleBlock("EVS", "Example Sheet", "Plants Around Us", 27));
children.push(B.infoRow());
children.push(B.spacer(60));

// Q1 — Fill in the blanks
children.push(B.sectionHeader(1, "Fill in the blanks", 6));
children.push(B.instruction("Fill each blank with the correct word from the chapter."));
const fillUps = [
  ["The thick main stem of a tree is called the ", "."],
  ["", " is the green pigment found in leaves."],
  ["A plant with a weak stem that grows along the ground is called a ", "."],
  ["A small garden at home where we grow vegetables is called a ", "."],
  ["The process by which a seed grows into a new plant is called ", "."],
  ["", " is the world\u2019s largest flower."]
];
fillUps.forEach((parts, i) => children.push(B.fillItem(i + 1, parts)));

// Q2 — Match the following
children.push(B.sectionHeader(2, "Match the following", 6));
children.push(B.instruction("Write the correct letter from Column B next to each number in Column A."));
children.push(B.matchTable(
  [ { n: 1, text: "Trunk" },       { n: 2, text: "Chlorophyll" },
    { n: 3, text: "Seedling" },    { n: 4, text: "Bark" },
    { n: 5, text: "Stomata" },     { n: 6, text: "Kitchen garden" } ],
  [ { letter: "a", text: "Brown outer covering of a trunk" },
    { letter: "b", text: "Green pigment in leaves" },
    { letter: "c", text: "Garden for growing vegetables at home" },
    { letter: "d", text: "Thick main stem of a tree" },
    { letter: "e", text: "Tiny pores on leaves" },
    { letter: "f", text: "Baby plant grown from a seed" } ]
));

// Q3 — MCQs
children.push(B.sectionHeader(3, "Choose the correct answer", 6));
children.push(B.instruction("Tick (\u2713) the correct option."));
const mcqs = [
  { q: "Which of these is a shrub?", opts: ["Banyan", "Rose", "Grass", "Pumpkin"] },
  { q: "Grass is a:", opts: ["Tree", "Shrub", "Herb", "Creeper"] },
  { q: "Which plant needs support to grow?", opts: ["Tree", "Climber", "Creeper", "Shrub"] },
  { q: "A seed needs _______ to germinate.", opts: ["Only water", "Only sun", "Air, water and warmth", "Only soil"] },
  { q: "Which is NOT a part of a plant?", opts: ["Root", "Stem", "Leaf", "Sun"] },
  { q: "A young baby plant is called a:", opts: ["Seedling", "Fruit", "Flower", "Branch"] }
];
mcqs.forEach((m, i) => {
  const blocks = B.mcqBlock(i + 1, m.q, m.opts);
  blocks.forEach(b => children.push(b));
});

// Q4 — Odd one out
children.push(B.sectionHeader(4, "Circle the odd one out", 4));
[
  ["Rose", "Mint", "Spinach", "Coriander"],
  ["Banyan", "Ashok", "Mango", "Tulsi"],
  ["Watermelon", "Pumpkin", "Grapevine", "Cucumber"],
  ["Water", "Air", "Warmth", "Music"]
].forEach((opts, i) => children.push(B.oddOneOut(i + 1, opts)));

// Q5 — One-word answers
children.push(B.sectionHeader(5, "Answer in one word", 5));
[
  "Which tree is known as the tree of life?",
  "Name the world\u2019s largest flower.",
  "What is the green colour in leaves called?",
  "Name the process by which plants make their own food.",
  "Which flower turns its head to follow the sun?"
].forEach((q, i) => children.push(B.oneWordItem(i + 1, q)));

// Save -> PDF (delivery format)
// Workflow: write docx -> convert to PDF with soffice -> remove the docx.
const { execSync } = require('child_process');
const doc = B.buildDoc(children);
const outputDir = path.resolve(__dirname);
const docxPath = path.join(outputDir, "example_evs_output.docx");
const pdfPath  = path.join(outputDir, "example_evs_output.pdf");

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(docxPath, buf);
  // Convert to PDF (assumes soffice is on PATH; the docx skill provides a wrapper too)
  execSync(`soffice --headless --convert-to pdf "${docxPath}" --outdir "${outputDir}"`,
           { stdio: 'inherit' });
  fs.unlinkSync(docxPath); // PDF is the deliverable; remove the intermediate docx
  console.log("Wrote PDF:", pdfPath);
});
