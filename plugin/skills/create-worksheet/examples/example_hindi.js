// Example: Hindi practice sheet using the shared builder.
// Demonstrates matra fill-ups, conjunct sorting, true/false, vilom match.

const fs = require('fs');
const path = require('path');
const B = require('../templates/worksheet_builder.js');
const { Packer, Document, Paragraph, TextRun, AlignmentType } = require('docx');

const children = [];

// Title + info
children.push(...B.titleBlock("Hindi", "\u0905\u092D\u094D\u092F\u093E\u0938 \u092A\u0924\u094D\u0930 \u2014 1", "\u0935\u094D\u092F\u093E\u0915\u0930\u0923 \u0914\u0930 \u092E\u093E\u0924\u094D\u0930\u093E", 26));
children.push(B.infoRow());
children.push(B.spacer(60));

// Q1 — Fill the matra (ऋ की मात्रा)
children.push(B.sectionHeader(1, "\u0909\u091A\u093F\u0924 \u092E\u093E\u0924\u094D\u0930\u093E \u0932\u0917\u093E\u0907\u090F \u2014 \u090B \u0915\u0940 \u092E\u093E\u0924\u094D\u0930\u093E", 4));
[
  ["\u0915) \u0915\u0937\u093F \u2192 ", ""],        // कृषि
  ["\u0916) \u092A\u0925\u094D\u0935\u0940 \u2192 ", ""],  // पृथ्वी
  ["\u0917) \u092E\u0917 \u2192 ", ""],               // मृग
  ["\u0918) \u0935\u0915\u094D\u0937 \u2192 ", ""]    // वृक्ष
].forEach((parts, i) => children.push(B.fillItem(i + 1, parts)));

// Q2 — True/False using ✓/✗
children.push(B.sectionHeader(2, "\u0938\u0939\u0940 (\u2713) \u092F\u093E \u0917\u0932\u0924 (\u2717) \u0932\u093F\u0916\u093F\u090F", 4));
[
  "\u0939\u093F\u0902\u0926\u0940 \u0935\u0930\u094D\u0923\u092E\u093E\u0932\u093E \u092E\u0947\u0902 11 \u0938\u094D\u0935\u0930 \u0939\u094B\u0924\u0947 \u0939\u0948\u0902\u0964",   // हिंदी वर्णमाला में 11 स्वर होते हैं।
  "\u0935\u094D\u092F\u0902\u091C\u0928\u094B\u0902 \u0915\u0940 \u0938\u0902\u0916\u094D\u092F\u093E 25 \u0939\u094B\u0924\u0940 \u0939\u0948\u0964",                              // व्यंजनों की संख्या 25 होती है।
  "'\u0905\u0902' \u0915\u094B \u0905\u0928\u0941\u0928\u093E\u0938\u093F\u0915 \u0915\u0939\u0924\u0947 \u0939\u0948\u0902\u0964",                                                  // 'अं' को अनुनासिक कहते हैं।
  "\u0938\u0902\u092F\u0941\u0915\u094D\u0924 \u0935\u094D\u092F\u0902\u091C\u0928 \u092E\u0947\u0902 \u0915\u094D\u0937, \u0924\u094D\u0930, \u091C\u094D\u091E \u0914\u0930 \u0936\u094D\u0930 \u0906\u0924\u0947 \u0939\u0948\u0902\u0964" // संयुक्त व्यंजन में क्ष, त्र, ज्ञ और श्र आते हैं।
].forEach((s, i) => children.push(B.tfItem(i + 1, s)));

// Q3 — Sort संयुक्ताक्षर vs द्वित्व व्यंजन
children.push(B.sectionHeader(3, "\u0936\u092C\u094D\u0926\u094B\u0902 \u0915\u094B \u0938\u0939\u0940 \u0938\u092E\u0942\u0939 \u092E\u0947\u0902 \u0932\u093F\u0916\u093F\u090F", 6));
children.push(new Paragraph({
  spacing: { after: 80 },
  children: [
    new TextRun({ text: "\u0936\u092C\u094D\u0926 \u2014 ", italics: true, size: 22, color: B.COLORS.muted }),
    new TextRun({ text: "\u0938\u0924\u094D\u092F, \u0926\u093F\u0932\u094D\u0932\u0940, \u0905\u091A\u094D\u091B\u093E, \u091B\u0941\u091F\u094D\u091F\u0940, \u092A\u0924\u094D\u0924\u093E, \u092A\u094D\u092F\u093E\u0930\u093E",  // सत्य, दिल्ली, अच्छा, छुट्टी, पत्ता, प्यारा
      bold: true, size: 22, color: B.COLORS.titleDark })
  ]
}));
children.push(B.sortChart(["\u0938\u0902\u092F\u0941\u0915\u094D\u0924\u093E\u0915\u094D\u0937\u0930", "\u0926\u094D\u0935\u093F\u0924\u094D\u0935 \u0935\u094D\u092F\u0902\u091C\u0928"], 4));  // संयुक्ताक्षर, द्वित्व व्यंजन

// Q4 — विलोम match
children.push(B.sectionHeader(4, "\u0935\u093F\u0932\u094B\u092E \u0936\u092C\u094D\u0926 \u092E\u093F\u0932\u093E\u0907\u090F", 6));
children.push(B.matchTable(
  [ { n: 1, text: "\u0936\u0939\u0930" },       // शहर
    { n: 2, text: "\u092A\u0941\u0930\u093E\u0928\u093E" },  // पुराना
    { n: 3, text: "\u0927\u0928\u0940" },         // धनी
    { n: 4, text: "\u091B\u094B\u091F\u093E" },   // छोटा
    { n: 5, text: "\u0926\u093F\u0928" },         // दिन
    { n: 6, text: "\u0938\u091A" } ],             // सच
  [ { letter: "a", text: "\u0928\u092F\u093E" },          // नया
    { letter: "b", text: "\u0917\u093E\u0901\u0935" },    // गाँव
    { letter: "c", text: "\u091D\u0942\u0920" },          // झूठ
    { letter: "d", text: "\u0917\u0930\u0940\u092C" },    // गरीब
    { letter: "e", text: "\u0930\u093E\u0924" },          // रात
    { letter: "f", text: "\u092C\u0921\u093C\u093E" } ]   // बड़ा
));

// Q5 — short Hindi answer
children.push(B.sectionHeader(5, "\u090F\u0915 \u0935\u093E\u0915\u094D\u092F \u092E\u0947\u0902 \u0909\u0924\u094D\u0924\u0930 \u0926\u0940\u091C\u093F\u090F", 6));
[
  "\u0938\u094D\u0935\u0930 \u0915\u093F\u0924\u0928\u0947 \u0939\u094B\u0924\u0947 \u0939\u0948\u0902? \u0909\u0928\u0915\u0947 \u0928\u093E\u092E \u0932\u093F\u0916\u093F\u090F\u0964",  // स्वर कितने होते हैं?
  "\u0905\u0928\u0941\u0938\u094D\u0935\u093E\u0930 \u0914\u0930 \u0905\u0928\u0941\u0928\u093E\u0938\u093F\u0915 \u092E\u0947\u0902 \u0915\u094D\u092F\u093E \u0905\u0902\u0924\u0930 \u0939\u0948?",  // अनुस्वार और अनुनासिक में क्या अंतर है?
  "\u0938\u0902\u092F\u0941\u0915\u094D\u0924 \u0935\u094D\u092F\u0902\u091C\u0928 \u0915\u094C\u0928 \u0938\u0947 \u0939\u094B\u0924\u0947 \u0939\u0948\u0902?"  // संयुक्त व्यंजन कौन से होते हैं?
].forEach((q, i) => {
  children.push(B.shortQuestion(i + 1, q));
  children.push(B.answerLine());
});

// Use Devanagari-friendly font
const doc = new Document({
  styles: {
    default: {
      document: {
        run: {
          font: { name: "Mangal", eastAsia: "Nirmala UI", cs: "Noto Sans Devanagari" },
          size: 22
        }
      }
    }
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 720, right: 720, bottom: 720, left: 720 }
      }
    },
    children
  }]
});

const outputPath = path.join(__dirname, "example_hindi_output.docx");
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outputPath, buf);
  console.log("Wrote:", outputPath);
});
