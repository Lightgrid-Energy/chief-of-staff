const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, HeadingLevel } = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' };
const borders = { top: border, bottom: border, left: border, right: border };
const cm = { top: 80, bottom: 80, left: 120, right: 120 };

function hCell(text, w) {
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA }, shading: { fill: '1F3864', type: ShadingType.CLEAR }, margins: cm, children: [new Paragraph({ children: [new TextRun({ text, bold: true, color: 'FFFFFF', size: 18, font: 'Arial' })] })] });
}
function urgencyColor(u) { return u === 'High' ? 'FFE0E0' : u === 'Medium' ? 'FFF8DC' : u === 'Low' ? 'E8F5E9' : 'FFFFFF'; }
function statusColor(s) { return s === 'Draft ready' ? 'E8F5E9' : s === 'On hold' ? 'FFE0E0' : s === 'Need name' ? 'FFF3CD' : s === 'To research' ? 'F0F0F0' : 'FFFFFF'; }

function cell(text, w, i) {
  let fill = 'FFFFFF';
  if (i === 5) fill = urgencyColor(text);
  if (i === 6) fill = statusColor(text);
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA }, shading: { fill, type: ShadingType.CLEAR }, margins: cm, children: [new Paragraph({ children: [new TextRun({ text, size: 18, font: 'Arial' })] })] });
}

const w = [400, 1200, 1400, 900, 3300, 800, 900];
const cols = ['#', 'Name', 'Company', 'Channel', 'Message Focus', 'Urgency', 'Status'];

function makeTable(rows) {
  return new Table({
    width: { size: w.reduce((a,b)=>a+b,0), type: WidthType.DXA },
    columnWidths: w,
    rows: [
      new TableRow({ tableHeader: true, children: cols.map((h,i) => hCell(h, w[i])) }),
      ...rows.map(r => new TableRow({ children: r.map((v,i) => cell(v, w[i], i)) }))
    ]
  });
}

function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text, font: 'Arial', bold: true, color: '2E5F9C', size: 26 })] });
}
function gap() { return new Paragraph({ children: [new TextRun('')] }); }

const montreal = [
  ['1','Tyler Hamilton','MaRS','LinkedIn','DC flexibility contacts; ask him to ping Kathleen re: lab','Medium','Draft ready'],
  ['2','Kathleen Cuth','Mantle Climate','LinkedIn','Intro — flexibility software for DCs, lab projects across Ontario','Medium','Draft ready'],
  ['3','Nicholas Parker','Clean AI ecosystem','LinkedIn','Investor in Emerald AI? Interested in our angel round? Market contacts?','Medium','Draft ready'],
  ['4','Brian Watson','Grants/Funding programs','LinkedIn','Help fund 3 projects: Sarnia ~$300K, Ottawa $1-3M, NB flagship','High','Draft ready'],
  ['5','Lynn Clutter','Family office (AB/NL)','LinkedIn','CSP judge; preseed raising $500K — thesis fit?','High','Draft ready'],
  ['6','Matt','Complete Energy Ventures','LinkedIn','DC flexibility + VPP alignment; $500K angel round','High','Draft ready'],
  ['7','[Name TBD]','Atura Power','LinkedIn','Innovative utility; DC optimization pilot opportunity','Medium','Need name'],
  ['8','Nathanland/Finland','Compute for Humanity','LinkedIn','NeoCloud optimization; 90-day pilot interest','Medium','Draft ready'],
  ['9','Phil de Luna','Mangrove','LinkedIn','NSERC/federal champion — who can open doors?','Medium','Draft ready'],
  ['10','[Partner TBD]','Galvanize Capital','LinkedIn','Does our project fit your infrastructure thesis?','Medium','Need name'],
  ['11','[Partner TBD]','Compass BC','LinkedIn','Same message as Galvanize (duplicate/adapt)','Medium','Need name'],
  ['12','[Contact TBD]','PSP Investments','LinkedIn','Similar thesis on stage; lets connect','Low','Draft ready'],
  ['—','Grantham Institute','—','—','RESEARCH ONLY — no outreach yet','—','To research'],
  ['—','Alex Hermuz','—','—','RESEARCH ONLY — unclear context','—','To research'],
  ['—','David Grimes','—','—','RESEARCH ONLY — interesting study, details TBD','—','To research'],
  ['—','Dawns View Innovation Hub','Toronto','—','RESEARCH ONLY — greenhouse/DC thesis, find presenter','—','To research'],
];

const alberta = [
  ['1','Rob Lucas','Dell','Email','Upper Bound presentation; founding partner for flexible compute lab','High','Draft ready'],
  ['2','Joseph La Hiro','Dell (exec?)','HOLD','Need to verify identity before outreach','—','On hold'],
  ['3','[Contact TBD]','Firefly','Email','They reached out previously — follow up; $500K early stage check','High','Draft ready'],
  ['4','Parminder','[TBD]','LinkedIn','Already emailed; LinkedIn follow-up — investor framing help','Medium','Draft ready'],
  ['5','Wish/Wishbake','[TBD]','LinkedIn','Accepted friend request; 30-60 min market insights call','Medium','Draft ready'],
  ['6','Westco Contact 1+2','Westco','LinkedIn/Email','800VDC suppliers/vendors; lab design support for Sarnia','High','Draft ready'],
  ['7','Robert Craig','AMI','Email','Vulcan cluster; pilot project; Hosti hire','Medium','Draft ready'],
  ['8','Marla Ornstein','EFL Energy Futures Lab','LinkedIn','Friend of James; need intros in Canadian energy landscape','Medium','Draft ready'],
  ['9','GK / JIKE','Hacks','Email','Follow up on previous email; lab fit, hardware focus','Medium','Draft ready'],
  ['10','[R&D Lady TBD]','Denver','Email','Optimization partnership; pilot opportunity','Medium','Need name'],
  ['11','[BD Guy TBD]','Denver','Email','Partnership scoping (CC R&D lady intro)','Medium','Need name'],
  ['12','Nathan','Data Dip','LinkedIn','Government champion; Ontario contacts; funding program guidance','High','Draft ready'],
  ['13','Lina Podina','University of Waterloo','LinkedIn','PINNs sprint collaboration; short-term paid engagement','Low','Draft ready'],
  ['14','Aidan Meyer','[TBD]','LinkedIn','Continual learning; startup collaboration interest','Low','Draft ready'],
];

const general = [
  ['1','Nitin','Angel/connector (US)','LinkedIn','Met at Deloitte; looking for US fund intros — who should we talk to?','Medium','Draft ready'],
];

const doc = new Document({
  styles: {
    default: { document: { run: { font: 'Arial', size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 40, bold: true, font: 'Arial', color: '1F3864' },
        paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, font: 'Arial', color: '2E5F9C' },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 15840, height: 12240 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
      }
    },
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: 'Outreach Tracker', font: 'Arial', bold: true, color: '1F3864', size: 40 })] }),
      new Paragraph({ children: [new TextRun({ text: 'Climate Solutions Prize (Montreal)  |  Upper Bound (Alberta)  |  General', font: 'Arial', size: 20, color: '555555', italics: true })] }),
      gap(),
      h2('MONTREAL — Climate Solutions Prize'),
      makeTable(montreal),
      gap(),
      h2('ALBERTA — Upper Bound Conference'),
      makeTable(alberta),
      gap(),
      h2('GENERAL'),
      makeTable(general),
      gap(),
      new Paragraph({ children: [new TextRun({ text: 'Note: "Draft ready" = queued for send, pending Mujtaba review. "Need name" or "On hold" = requires research before outreach. "RESEARCH ONLY" = not ready for contact.', font: 'Arial', size: 16, italics: true, color: '888888' })] }),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('C:/Users/mujta/OneDrive/Documents/Crypto/Robot Work/chief-of-staff/outreach-tracker.docx', buf);
  console.log('Done');
}).catch(e => { console.error(e); process.exit(1); });
