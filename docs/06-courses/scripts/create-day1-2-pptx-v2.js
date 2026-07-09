const pptxgen = require("pptxgenjs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Carey Hugo";
pres.title = "愿力探索 · Day 1-2 (高端版 v2)";

// Premium color palette
const NAVY = "0A1628";
const DEEP_TEAL = "0D2137";
const GOLD = "C9A24C";
const LIGHT_GOLD = "E8D5A3";
const WHITE = "FFFFFF";
const CREAM = "F5F0E8";
const TEXT_BODY = "C8CDD5";
const TEXT_SUBTLE = "8892A0";
const CARD_BG = "FFFFFF";

const BG_DARK = path.resolve(__dirname, "..", "01-lead-course", "bg-premium-dark.png");

// Helper: add gold bottom accent line
function addGoldLine(slide, y) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.8, y: y, w: 1.5, h: 0.03,
    fill: { color: GOLD }
  });
}

// ===================== SAMPLE SLIDES =====================

// Slide 1: Cover Day 1 (premium)
let s1 = pres.addSlide();
s1.background = { path: BG_DARK };

// Glass effect overlay
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: NAVY, transparency: 30 }
});

// Left vertical gold accent bar
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 0.8, w: 0.04, h: 3.5,
  fill: { color: GOLD }
});

// "愿力探索" label
s1.addText("愿力探索", {
  x: 0.9, y: 1.0, w: 5, h: 0.5,
  fontSize: 16, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true,
  charSpacing: 4, margin: 0
});

// Main title
s1.addText("四个词\n你分得清吗？", {
  x: 0.9, y: 1.6, w: 5.5, h: 1.8,
  fontSize: 38, color: WHITE, fontFace: "WenQuanYi Zen Hei", bold: true,
  lineSpacingMultiple: 1.3, margin: 0
});

// Gold accent line under title
addGoldLine(s1, 3.5);

// Day & author
s1.addText("Day 1", {
  x: 0.9, y: 3.7, w: 2, h: 0.4,
  fontSize: 14, color: GOLD, fontFace: "Arial", bold: true, charSpacing: 2, margin: 0
});
s1.addText("主讲：胡哥", {
  x: 0.9, y: 4.1, w: 3, h: 0.3,
  fontSize: 12, color: TEXT_BODY, fontFace: "WenQuanYi Zen Hei", margin: 0
});

// Bottom-right decorative gold circle
s1.addShape(pres.shapes.OVAL, {
  x: 7.8, y: 3.8, w: 1.8, h: 1.8,
  fill: { color: GOLD, transparency: 92 },
  line: { color: GOLD, width: 0.5, transparency: 80 }
});

// Slide 2: Pain Point (glass card style)
let s2 = pres.addSlide();
s2.background = { color: DEEP_TEAL };

// Subtle gradient overlay
s2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: NAVY, transparency: 50 }
});

// Small label
s2.addText("痛点开场", {
  x: 0.8, y: 0.5, w: 3, h: 0.4,
  fontSize: 11, color: GOLD, fontFace: "Arial", bold: true, charSpacing: 3, margin: 0
});

// Glass card
s2.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.1, w: 8.4, h: 3.8,
  fill: { color: WHITE, transparency: 95 },
  line: { color: WHITE, width: 0.5, transparency: 85 }
});

s2.addText("过去三年，你有没有——", {
  x: 1.2, y: 1.4, w: 7, h: 0.4,
  fontSize: 13, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});

s2.addText(`"终于找到了\n真正想做的事"`, {
  x: 1.2, y: 1.9, w: 7, h: 1.3,
  fontSize: 34, color: WHITE, fontFace: "WenQuanYi Zen Hei", bold: true,
  lineSpacingMultiple: 1.2, margin: 0
});

s2.addText("三个月后又在找新方向？", {
  x: 1.2, y: 3.4, w: 7, h: 0.4,
  fontSize: 16, color: TEXT_SUBTLE, fontFace: "WenQuanYi Zen Hei", margin: 0
});

s2.addText("然后开始怀疑自己不够坚持？", {
  x: 1.2, y: 3.9, w: 7, h: 0.4,
  fontSize: 16, color: TEXT_SUBTLE, fontFace: "WenQuanYi Zen Hei", margin: 0
});

// Slide 3: Core Insight (full-bleed dramatic)
let s3 = pres.addSlide();
s3.background = { path: BG_DARK };

s3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: NAVY, transparency: 35 }
});

// Large quote-style
s3.addText("你可能只是——", {
  x: 0.8, y: 0.8, w: 8, h: 0.4,
  fontSize: 14, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true,
  charSpacing: 3, margin: 0
});

s3.addText("用错了词！", {
  x: 0.8, y: 1.4, w: 8, h: 1.0,
  fontSize: 48, color: WHITE, fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});

addGoldLine(s3, 2.6);

s3.addText("大部分人追的是「愿望」", {
  x: 0.8, y: 3.0, w: 8, h: 0.5,
  fontSize: 20, color: TEXT_BODY, fontFace: "WenQuanYi Zen Hei", margin: 0
});

s3.addText("从没触到过「愿力」", {
  x: 0.8, y: 3.6, w: 8, h: 0.6,
  fontSize: 24, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});

// Decorative gold line
s3.addShape(pres.shapes.RECTANGLE, {
  x: 4, y: 4.5, w: 2, h: 0.02,
  fill: { color: GOLD, transparency: 50 }
});

// Slide 4: Pyramid (with glass cards for each layer)
let s4 = pres.addSlide();
s4.background = { color: DEEP_TEAL };
s4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: NAVY, transparency: 50 }
});

s4.addText("四层金字塔", {
  x: 0.8, y: 0.4, w: 4, h: 0.5,
  fontSize: 18, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, charSpacing: 3, margin: 0
});

// Pyramid layers with glassmorphism
const layers = [
  { label: "愿力", sub: "「我愿意」", color: GOLD, y: 0.9 },
  { label: "使命", sub: "「我应该」", color: "5A7D60", y: 2.0 },
  { label: "梦想", sub: "「我想到」", color: "5A7D95", y: 3.1 },
  { label: "愿望", sub: "「我想要」", color: "8B7B65", y: 4.2 }
];

layers.forEach((l, i) => {
  const width = 6.5 - i * 0.4;
  const x = (10 - width) / 2;
  
  // Glass card background
  s4.addShape(pres.shapes.RECTANGLE, {
    x, y: l.y, w: width, h: 0.85,
    fill: { color: WHITE, transparency: 93 },
    line: { color: l.color, width: 0.5, transparency: 60 }
  });
  
  // Left accent bar
  s4.addShape(pres.shapes.RECTANGLE, {
    x, y: l.y, w: 0.04, h: 0.85,
    fill: { color: l.color }
  });
  
  s4.addText(l.label, {
    x: x + 0.2, y: l.y + 0.08, w: 3, h: 0.45,
    fontSize: 20, color: l.color, bold: true, fontFace: "WenQuanYi Zen Hei", margin: 0
  });
  s4.addText(l.sub, {
    x: x + 0.2, y: l.y + 0.48, w: 4, h: 0.3,
    fontSize: 12, color: TEXT_SUBTLE, fontFace: "WenQuanYi Zen Hei", margin: 0
  });
});

// Slide 5: Wish vs Willpower (side by side glass cards)
let s5 = pres.addSlide();
s5.background = { color: DEEP_TEAL };
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: NAVY, transparency: 50 }
});

s5.addText("愿望 vs 愿力", {
  x: 0.8, y: 0.4, w: 5, h: 0.5,
  fontSize: 18, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, charSpacing: 3, margin: 0
});

// Left card - Wish
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.2, w: 4, h: 3.5,
  fill: { color: WHITE, transparency: 96 },
  line: { color: TEXT_SUBTLE, width: 0.3, transparency: 80 }
});
s5.addText("愿望", {
  x: 0.8, y: 1.5, w: 4, h: 0.6,
  fontSize: 26, color: "667788", align: "center", fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});
s5.addText("「我想要」", {
  x: 0.8, y: 2.1, w: 4, h: 0.4,
  fontSize: 14, color: "8899AA", align: "center", fontFace: "WenQuanYi Zen Hei", margin: 0
});
s5.addShape(pres.shapes.RECTANGLE, {
  x: 2.0, y: 2.6, w: 0.8, h: 0.02,
  fill: { color: "667788", transparency: 50 }
});
s5.addText("消费心态 · 被动等待\n许个愿，没了", {
  x: 0.8, y: 2.8, w: 4, h: 0.8,
  fontSize: 13, color: "8899AA", align: "center", fontFace: "WenQuanYi Zen Hei", margin: 0
});

// Right card - Willpower
s5.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4, h: 3.5,
  fill: { color: GOLD, transparency: 94 },
  line: { color: GOLD, width: 0.5, transparency: 70 }
});
s5.addText("愿力", {
  x: 5.2, y: 1.5, w: 4, h: 0.6,
  fontSize: 26, color: GOLD, align: "center", fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});
s5.addText("「我愿意」", {
  x: 5.2, y: 2.1, w: 4, h: 0.4,
  fontSize: 14, color: GOLD, align: "center", fontFace: "WenQuanYi Zen Hei", margin: 0
});
s5.addShape(pres.shapes.RECTANGLE, {
  x: 6.4, y: 2.6, w: 0.8, h: 0.02,
  fill: { color: GOLD, transparency: 40 }
});
s5.addText("创造心态 · 主动选择\n做一辈子", {
  x: 5.2, y: 2.8, w: 4, h: 0.8,
  fontSize: 13, color: GOLD, align: "center", fontFace: "WenQuanYi Zen Hei", margin: 0
});

// Slide 6: Ultimate Question (dramatic)
let s6 = pres.addSlide();
s6.background = { path: BG_DARK };
s6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: NAVY, transparency: 40 }
});

// Subtle gold circle behind text
s6.addShape(pres.shapes.OVAL, {
  x: 3.5, y: 0.5, w: 3, h: 3,
  fill: { color: GOLD, transparency: 95 }
});

s6.addText("有没有一件事——", {
  x: 0.8, y: 0.8, w: 8, h: 0.4,
  fontSize: 14, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});

s6.addText("你愿意做一辈子", {
  x: 0.8, y: 1.5, w: 8, h: 0.8,
  fontSize: 38, color: WHITE, fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});

s6.addText("没人看、没人夸、没人给钱\n也愿意？", {
  x: 0.8, y: 2.5, w: 8, h: 1.0,
  fontSize: 20, color: TEXT_SUBTLE, fontFace: "WenQuanYi Zen Hei", margin: 0
});

addGoldLine(s6, 3.8);

s6.addText("找到它 → 你就是最幸运的 1%", {
  x: 0.8, y: 4.1, w: 8, h: 0.5,
  fontSize: 16, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});

// Slide 7: Homework card
let s7 = pres.addSlide();
s7.background = { color: DEEP_TEAL };
s7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: NAVY, transparency: 50 }
});

s7.addText("📝 今天的功课", {
  x: 0.8, y: 0.4, w: 5, h: 0.5,
  fontSize: 18, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, charSpacing: 3, margin: 0
});

// Larger glass card
s7.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.1, w: 8.4, h: 3.8,
  fill: { color: WHITE, transparency: 95 },
  line: { color: WHITE, width: 0.5, transparency: 85 }
});

s7.addText("写下过去三年换过的三个方向", {
  x: 1.2, y: 1.5, w: 7, h: 0.5,
  fontSize: 18, color: WHITE, fontFace: "WenQuanYi Zen Hei", margin: 0
});

s7.addText("判断每个驱动你的是：", {
  x: 1.2, y: 2.2, w: 7, h: 0.4,
  fontSize: 14, color: TEXT_SUBTLE, fontFace: "WenQuanYi Zen Hei", margin: 0
});

// Choice tags
const tags = ["愿望", "梦想", "使命", "愿力"];
tags.forEach((tag, i) => {
  const tx = 1.2 + i * 1.9;
  s7.addShape(pres.shapes.RECTANGLE, {
    x: tx, y: 2.8, w: 1.6, h: 0.5,
    fill: { color: GOLD, transparency: 85 },
    line: { color: GOLD, width: 0.3, transparency: 60 }
  });
  s7.addText("□ " + tag, {
    x: tx, y: 2.8, w: 1.6, h: 0.5,
    fontSize: 13, color: GOLD, align: "center", valign: "middle", fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
  });
});

s7.addText("评论区见 👇", {
  x: 1.2, y: 3.8, w: 4, h: 0.3,
  fontSize: 12, color: TEXT_SUBTLE, fontFace: "WenQuanYi Zen Hei", margin: 0
});

// Slide 8: Preview / hook
let s8 = pres.addSlide();
s8.background = { path: BG_DARK };
s8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: NAVY, transparency: 35 }
});

s8.addText("明天见", {
  x: 0.8, y: 1.2, w: 3, h: 0.4,
  fontSize: 14, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});

s8.addText("三个标志", {
  x: 0.8, y: 1.8, w: 8, h: 1.0,
  fontSize: 42, color: WHITE, fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});

s8.addText("测你离愿力还有多远", {
  x: 0.8, y: 2.9, w: 8, h: 0.5,
  fontSize: 18, color: TEXT_SUBTLE, fontFace: "WenQuanYi Zen Hei", margin: 0
});

addGoldLine(s8, 3.7);

s8.addText("🔥 明天见", {
  x: 0.8, y: 4.0, w: 3, h: 0.5,
  fontSize: 18, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, margin: 0
});

// ===== DAY 2 SLIDES (same visual system) =====

// Slide 9: Day 2 Cover
let s9 = pres.addSlide();
s9.background = { path: BG_DARK };
s9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: NAVY, transparency: 30 }
});

// Left vertical gold accent bar
s9.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 0.8, w: 0.04, h: 3.5,
  fill: { color: GOLD }
});

s9.addText("愿力探索", {
  x: 0.9, y: 1.0, w: 5, h: 0.5,
  fontSize: 16, color: GOLD, fontFace: "WenQuanYi Zen Hei", bold: true, charSpacing: 4, margin: 0
});

s9.addText("3个标志\n测你的愿力纯度", {
  x: 0.9, y: 1.6, w: 5.5, h: 1.8,
  fontSize: 36, color: WHITE, fontFace: "WenQuanYi Zen Hei", bold: true,
  lineSpacingMultiple: 1.3, margin: 0
});

addGoldLine(s9, 3.5);

s9.addText("Day 2", {
  x: 0.9, y: 3.7, w: 2, h: 0.4,
  fontSize: 14, color: GOLD, fontFace: "Arial", bold: true, charSpacing: 2, margin: 0
});
s9.addText("主讲：胡哥", {
  x: 0.9, y: 4.1, w: 3, h: 0.3,
  fontSize: 12, color: TEXT_BODY, fontFace: "WenQuanYi Zen Hei", margin: 0
});

// Bottom-right gold circle
s9.addShape(pres.shapes.OVAL, {
  x: 7.8, y: 3.8, w: 1.8, h: 1.8,
  fill: { color: GOLD, transparency: 92 },
  line: { color: GOLD, width: 0.5, transparency: 80 }
});

// Write file
const outPath = path.resolve(__dirname, "Day1-2-课件-v2.pptx");
pres.writeFile({ fileName: outPath })
  .then(() => console.log("OK: " + outPath))
  .catch(err => console.error(err));
