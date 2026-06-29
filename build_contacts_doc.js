
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        WidthType, BorderStyle, ShadingType, HeadingLevel } = require('docx');
const fs = require('fs');

const contacts = JSON.parse(fs.readFileSync(
  'C:/Users/mujta/OneDrive/Documents/Crypto/Robot Work/chief-of-staff/pst-extract/contacts_clean.json',
  'utf8'
));

const border = { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' };
const borders = { top: border, bottom: border, left: border, right: border };
const cm = { top: 80, bottom: 80, left: 120, right: 120 };

function hCell(text, w) {
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA },
    shading: { fill: '1F3864', type: ShadingType.CLEAR }, margins: cm,
    children: [new Paragraph({ children: [new TextRun({ text, bold: true, color: 'FFFFFF', size: 18, font: 'Arial' })] })] });
}

function catColor(cat) {
  const map = {
    'Investor': 'EAF4FB',
    'Academic / Research': 'EAF7EA',
    'Government': 'FFF8DC',
    'Accelerator / Ecosystem': 'F3E8FF',
    'Legal': 'FFE8E8',
    'Finance / Banking': 'F0F0F0',
    'Industry / Other': 'FFFFFF',
  };
  return map[cat] || 'FFFFFF';
}

function row(c) {
  const fill = catColor(c.category);
  const cols = [c.name, c.email, c.category, String(c.count), (c.subjects||[]).slice(0,2).join(' / ')];
  const ws = [1800, 2400, 1400, 500, 3200];
  return new TableRow({ children: cols.map((v, i) =>
    new TableCell({ borders, width: { size: ws[i], type: WidthType.DXA },
      shading: { fill, type: ShadingType.CLEAR }, margins: cm,
      children: [new Paragraph({ children: [new TextRun({ text: v||'', size: 18, font: 'Arial' })] })] })
  )});
}

const headers = ['Name', 'Email', 'Category', 'Emails', 'Sample Subjects'];
const ws = [1800, 2400, 1400, 500, 3200];

const doc = new Document({
  styles: {
    default: { document: { run: { font: 'Arial', size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 40, bold: true, font: 'Arial', color: '1F3864' },
        paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, font: 'Arial', color: '2E5F9C' },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: {
      page: { size: { width: 15840, height: 12240 }, margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } }
    },
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: 'PST Contacts — Real Humans', font: 'Arial', bold: true, color: '1F3864', size: 40 })] }),
      new Paragraph({ children: [new TextRun({ text: `Extracted from mujtaba@lightgrid.energy.pst  |  ${contacts.length} contacts  |  Newsletters and automated emails removed`, font: 'Arial', size: 20, color: '555555', italics: true })] }),
      new Paragraph({ children: [new TextRun('')] }),
      new Table({
        width: { size: ws.reduce((a,b)=>a+b,0), type: WidthType.DXA },
        columnWidths: ws,
        rows: [
          new TableRow({ tableHeader: true, children: headers.map((h,i) => hCell(h, ws[i])) }),
          ...contacts.map(c => row(c))
        ]
      }),
      new Paragraph({ children: [new TextRun('')] }),
      new Paragraph({ children: [new TextRun({ text: 'Color key: Blue = Investor  |  Green = Academic/Research  |  Yellow = Government  |  Purple = Accelerator/Ecosystem  |  Red = Legal  |  Grey = Finance  |  White = Industry/Other', font: 'Arial', size: 16, italics: true, color: '888888' })] }),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('C:/Users/mujta/OneDrive/Documents/Crypto/Robot Work/chief-of-staff/pst-contacts.docx', buf);
  console.log('Done');
}).catch(e => { console.error(e.message); process.exit(1); });
