const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Carey Hugo";
pres.title = "愿力探索 · Day 1-2";

// Color palette: deep blue + warm gold
const DEEP_BLUE = "1A2940";
const GOLD = "C9A24C";
const WHITE = "FFFFFF";
const LIGHT_BG = "F5F3EF";
const DARK_TEXT = "1A2940";
const ACCENT_GOLD = "D4AF37";

// ===================== DAY 1 =====================

// Slide 1: Cover Day 1
let s1 = pres.addSlide();
s1.background = { color: DEEP_BLUE };
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 4.2, w: 10, h: 1.425, fill: { color: GOLD, transparency: 85 }
});
s1.addText("🌊", { x: 0.8, y: 0.8, w: 1.5, h: 1.2, fontSize: 48, align: "center" });
s1.addText("愿力探索", {
  x: 0.8, y: 1.6, w: 4, h: 0.6, fontSize: 20, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s1.addText("四个词，你分得清吗？", {
  x: 0.8, y: 2.3, w: 6, h: 1.0, fontSize: 36, color: WHITE, fontFace: "Arial", bold: true, margin: 0
});
s1.addText("Day 1", {
  x: 0.8, y: 3.5, w: 2, h: 0.5, fontSize: 16, color: GOLD, fontFace: "Arial", margin: 0
});
s1.addText("主讲：胡哥", {
  x: 6, y: 4.4, w: 3, h: 0.5, fontSize: 14, color: WHITE, fontFace: "Arial", align: "right", margin: 0
});

// Slide 2: Pain point
let s2 = pres.addSlide();
s2.background = { color: LIGHT_BG };
s2.addText("过去三年，你有没有——", {
  x: 0.8, y: 0.6, w: 8, h: 0.6, fontSize: 14, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s2.addText(`"终于找到了\n真正想做的事"`, {
  x: 0.8, y: 1.3, w: 8, h: 1.5, fontSize: 36, color: DARK_TEXT, fontFace: "Arial", bold: true, margin: 0
});
s2.addText("三个月后又在找新方向？", {
  x: 0.8, y: 2.9, w: 8, h: 0.5, fontSize: 18, color: "666666", fontFace: "Arial", margin: 0
});
s2.addText("然后开始怀疑自己不够坚持？", {
  x: 0.8, y: 3.5, w: 8, h: 0.5, fontSize: 18, color: "666666", fontFace: "Arial", margin: 0
});

// Slide 3: Core insight
let s3 = pres.addSlide();
s3.background = { color: DEEP_BLUE };
s3.addText("你可能只是——", {
  x: 0.8, y: 0.8, w: 8, h: 0.6, fontSize: 16, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s3.addText("用错了词！", {
  x: 0.8, y: 1.5, w: 8, h: 0.8, fontSize: 40, color: WHITE, fontFace: "Arial", bold: true, margin: 0
});
s3.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 2.6, w: 3, h: 0.04, fill: { color: GOLD }
});
s3.addText("大部分人追的是「愿望」", {
  x: 0.8, y: 3.0, w: 8, h: 0.5, fontSize: 20, color: WHITE, fontFace: "Arial", margin: 0
});
s3.addText("从没触到过「愿力」", {
  x: 0.8, y: 3.6, w: 8, h: 0.5, fontSize: 20, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});

// Slide 4: Four-layer pyramid
let s4 = pres.addSlide();
s4.background = { color: LIGHT_BG };
s4.addText("四层金字塔", {
  x: 0.8, y: 0.4, w: 4, h: 0.6, fontSize: 20, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});

// Pyramid layers (bottom to top)
const layers = [
  { label: "愿力", sub: "「我愿意」", color: "D4AF37", y: 0.9 },
  { label: "使命", sub: "「我应该」", color: "4A6741", y: 2.0 },
  { label: "梦想", sub: "「我想到」", color: "5B7F95", y: 3.1 },
  { label: "愿望", sub: "「我想要」", color: "8B7355", y: 4.2 }
];
layers.forEach((l, i) => {
  const width = 6 - i * 0.8;
  const x = (10 - width) / 2;
  s4.addShape(pres.shapes.RECTANGLE, {
    x, y: l.y, w: width, h: 0.85,
    fill: { color: l.color, transparency: 20 }
  });
  s4.addText(l.label, {
    x, y: l.y + 0.05, w: width, h: 0.5,
    fontSize: 22, color: WHITE, bold: true, align: "center", fontFace: "Arial", margin: 0
  });
  s4.addText(l.sub, {
    x, y: l.y + 0.45, w: width, h: 0.35,
    fontSize: 13, color: "DDDDDD", align: "center", fontFace: "Arial", margin: 0
  });
});

// Slide 5: Wish vs Willpower
let s5 = pres.addSlide();
s5.background = { color: DEEP_BLUE };
s5.addText("愿望 vs 愿力", {
  x: 0.8, y: 0.4, w: 5, h: 0.6, fontSize: 22, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});

// Left card
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.3, w: 4, h: 3.2,
  fill: { color: WHITE, transparency: 92 }
});
s5.addText("愿望", {
  x: 0.8, y: 1.5, w: 4, h: 0.6, fontSize: 28, color: "888888", align: "center", fontFace: "Arial", bold: true, margin: 0
});
s5.addText("「我想要」", {
  x: 0.8, y: 2.1, w: 4, h: 0.5, fontSize: 16, color: "AAAAAA", align: "center", fontFace: "Arial", margin: 0
});
s5.addText("消费心态", {
  x: 0.8, y: 2.8, w: 4, h: 0.4, fontSize: 14, color: "888888", align: "center", fontFace: "Arial", margin: 0
});
s5.addText("被动等待", {
  x: 0.8, y: 3.2, w: 4, h: 0.4, fontSize: 14, color: "888888", align: "center", fontFace: "Arial", margin: 0
});
s5.addText("许个愿，没了", {
  x: 0.8, y: 3.6, w: 4, h: 0.4, fontSize: 14, color: "888888", align: "center", fontFace: "Arial", margin: 0
});

// Right card
s5.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.3, w: 4, h: 3.2,
  fill: { color: GOLD, transparency: 90 }
});
s5.addText("愿力", {
  x: 5.2, y: 1.5, w: 4, h: 0.6, fontSize: 28, color: GOLD, align: "center", fontFace: "Arial", bold: true, margin: 0
});
s5.addText("「我愿意」", {
  x: 5.2, y: 2.1, w: 4, h: 0.5, fontSize: 16, color: GOLD, align: "center", fontFace: "Arial", margin: 0
});
s5.addText("创造心态", {
  x: 5.2, y: 2.8, w: 4, h: 0.4, fontSize: 14, color: GOLD, align: "center", fontFace: "Arial", margin: 0
});
s5.addText("主动选择", {
  x: 5.2, y: 3.2, w: 4, h: 0.4, fontSize: 14, color: GOLD, align: "center", fontFace: "Arial", margin: 0
});
s5.addText("做一辈子", {
  x: 5.2, y: 3.6, w: 4, h: 0.4, fontSize: 14, color: GOLD, align: "center", fontFace: "Arial", margin: 0
});

// Slide 6: Ultimate question
let s6 = pres.addSlide();
s6.background = { color: DEEP_BLUE };
s6.addText("有没有一件事——", {
  x: 0.8, y: 0.8, w: 8, h: 0.5, fontSize: 16, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s6.addText("你愿意做一辈子", {
  x: 0.8, y: 1.5, w: 8, h: 0.8, fontSize: 36, color: WHITE, fontFace: "Arial", bold: true, margin: 0
});
s6.addText("没人看、没人夸、没人给钱\n也愿意？", {
  x: 0.8, y: 2.4, w: 8, h: 1.0, fontSize: 20, color: "AAAAAA", fontFace: "Arial", margin: 0
});
s6.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 3.6, w: 3, h: 0.04, fill: { color: GOLD }
});
s6.addText("找到它 → 你就是最幸运的 1%", {
  x: 0.8, y: 4.0, w: 8, h: 0.5, fontSize: 16, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});

// Slide 7: Homework
let s7 = pres.addSlide();
s7.background = { color: LIGHT_BG };
s7.addText("📝 今天的功课", {
  x: 0.8, y: 0.4, w: 4, h: 0.6, fontSize: 22, color: DARK_TEXT, fontFace: "Arial", bold: true, margin: 0
});
s7.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.2, w: 8, h: 3.2,
  fill: { color: WHITE }
});
s7.addText("写下过去三年换过的三个方向", {
  x: 1.2, y: 1.5, w: 7, h: 0.6, fontSize: 18, color: DARK_TEXT, fontFace: "Arial", margin: 0
});
s7.addText("判断每个驱动你的是：", {
  x: 1.2, y: 2.2, w: 7, h: 0.5, fontSize: 16, color: "666666", fontFace: "Arial", margin: 0
});
s7.addText("□ 愿望  □ 梦想  □ 使命  □ 愿力", {
  x: 1.2, y: 2.9, w: 7, h: 0.6, fontSize: 18, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s7.addText("评论区见 👇", {
  x: 1.2, y: 3.7, w: 4, h: 0.4, fontSize: 14, color: "888888", fontFace: "Arial", margin: 0
});

// Slide 8: Preview
let s8 = pres.addSlide();
s8.background = { color: DEEP_BLUE };
s8.addText("明天见", {
  x: 0.8, y: 1.0, w: 8, h: 0.6, fontSize: 16, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s8.addText("三个标志", {
  x: 0.8, y: 1.7, w: 8, h: 1.0, fontSize: 40, color: WHITE, fontFace: "Arial", bold: true, margin: 0
});
s8.addText("测你离愿力还有多远", {
  x: 0.8, y: 2.8, w: 8, h: 0.6, fontSize: 18, color: "AAAAAA", fontFace: "Arial", margin: 0
});
s8.addText("🔥 明天见", {
  x: 0.8, y: 4.0, w: 3, h: 0.5, fontSize: 20, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});

// ===================== DAY 2 =====================

// Slide 9: Cover Day 2
let s9 = pres.addSlide();
s9.background = { color: DEEP_BLUE };
s9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 4.2, w: 10, h: 1.425, fill: { color: GOLD, transparency: 85 }
});
s9.addText("🌊", { x: 0.8, y: 0.8, w: 1.5, h: 1.2, fontSize: 48, align: "center" });
s9.addText("愿力探索", {
  x: 0.8, y: 1.6, w: 4, h: 0.6, fontSize: 20, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s9.addText("3个标志，测你的愿力纯度", {
  x: 0.8, y: 2.3, w: 7, h: 1.0, fontSize: 34, color: WHITE, fontFace: "Arial", bold: true, margin: 0
});
s9.addText("Day 2", {
  x: 0.8, y: 3.5, w: 2, h: 0.5, fontSize: 16, color: GOLD, fontFace: "Arial", margin: 0
});
s9.addText("主讲：胡哥", {
  x: 6, y: 4.4, w: 3, h: 0.5, fontSize: 14, color: WHITE, fontFace: "Arial", align: "right", margin: 0
});

// Slide 10: Why can't you go far?
let s10 = pres.addSlide();
s10.background = { color: LIGHT_BG };
s10.addText("为什么走不远？", {
  x: 0.8, y: 0.4, w: 6, h: 0.6, fontSize: 22, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s10.addText("昨天你写了三个方向", {
  x: 0.8, y: 1.3, w: 8, h: 0.5, fontSize: 20, color: DARK_TEXT, fontFace: "Arial", margin: 0
});
s10.addText("不是不坚持", {
  x: 0.8, y: 2.0, w: 8, h: 0.5, fontSize: 20, color: DARK_TEXT, fontFace: "Arial", margin: 0
});
s10.addText("是驱动它们的力不够硬", {
  x: 0.8, y: 2.7, w: 8, h: 0.5, fontSize: 20, color: DARK_TEXT, fontFace: "Arial", margin: 0
});
s10.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 3.5, w: 3, h: 0.04, fill: { color: GOLD }
});
s10.addText("缺一个东西：「愿力三标」", {
  x: 0.8, y: 3.8, w: 8, h: 0.5, fontSize: 20, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});

// Slide 11: Three markers overview
let s11 = pres.addSlide();
s11.background = { color: DEEP_BLUE };
s11.addText("🔥 愿力三标", {
  x: 0.8, y: 0.4, w: 5, h: 0.6, fontSize: 24, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});

const markers = [
  { num: "①", title: "可承诺", desc: "没人看你也会做", y: 1.3 },
  { num: "②", title: "可承受", desc: "代价你能扛", y: 2.6 },
  { num: "③", title: "可生长", desc: "螺旋上升，不是循环", y: 3.9 }
];
markers.forEach(m => {
  s11.addShape(pres.shapes.RECTANGLE, {
    x: 0.8, y: m.y, w: 1.0, h: 1.0,
    fill: { color: GOLD, transparency: 85 }
  });
  s11.addText(m.num, {
    x: 0.8, y: m.y, w: 1.0, h: 1.0,
    fontSize: 30, color: GOLD, align: "center", valign: "middle", fontFace: "Arial", bold: true, margin: 0
  });
  s11.addText(m.title, {
    x: 2.0, y: m.y + 0.05, w: 3, h: 0.5,
    fontSize: 22, color: WHITE, fontFace: "Arial", bold: true, margin: 0
  });
  s11.addText(m.desc, {
    x: 2.0, y: m.y + 0.5, w: 5, h: 0.4,
    fontSize: 14, color: "AAAAAA", fontFace: "Arial", margin: 0
  });
});

// Slide 12: Marker 1 - Committed
let s12 = pres.addSlide();
s12.background = { color: LIGHT_BG };
s12.addText("① 可承诺", {
  x: 0.8, y: 0.4, w: 4, h: 0.6, fontSize: 24, color: DARK_TEXT, fontFace: "Arial", bold: true, margin: 0
});
s12.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.2, w: 8, h: 3.5,
  fill: { color: WHITE }
});
s12.addText("没人点赞 👍  没人转发 🔁", {
  x: 1.2, y: 1.5, w: 7, h: 0.5, fontSize: 18, color: DARK_TEXT, fontFace: "Arial", align: "center", margin: 0
});
s12.addText("没人夸你  没人给钱 💰", {
  x: 1.2, y: 2.1, w: 7, h: 0.5, fontSize: 18, color: DARK_TEXT, fontFace: "Arial", align: "center", margin: 0
});
s12.addText("你还会做吗？", {
  x: 1.2, y: 2.9, w: 7, h: 0.5, fontSize: 22, color: GOLD, fontFace: "Arial", bold: true, align: "center", margin: 0
});
s12.addText("是 → 这是愿力    否 → 只是愿望", {
  x: 1.2, y: 3.6, w: 7, h: 0.4, fontSize: 14, color: "888888", fontFace: "Arial", align: "center", margin: 0
});

// Slide 13: Marker 2 - Bearable
let s13 = pres.addSlide();
s13.background = { color: LIGHT_BG };
s13.addText("② 可承受", {
  x: 0.8, y: 0.4, w: 4, h: 0.6, fontSize: 24, color: DARK_TEXT, fontFace: "Arial", bold: true, margin: 0
});
s13.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.2, w: 8, h: 3.5,
  fill: { color: WHITE }
});
s13.addText("不是「能得到什么」", {
  x: 1.2, y: 1.5, w: 7, h: 0.5, fontSize: 20, color: DARK_TEXT, fontFace: "Arial", align: "center", margin: 0
});
s13.addText("是「愿意失去什么」", {
  x: 1.2, y: 2.1, w: 7, h: 0.5, fontSize: 20, color: GOLD, fontFace: "Arial", bold: true, align: "center", margin: 0
});
s13.addText("最差的情况——\n钱没了、时间花了、被人笑话了\n你后悔吗？", {
  x: 1.2, y: 2.8, w: 7, h: 1.2, fontSize: 16, color: "666666", fontFace: "Arial", align: "center", margin: 0
});

// Slide 14: Marker 3 - Growth
let s14 = pres.addSlide();
s14.background = { color: LIGHT_BG };
s14.addText("③ 可生长", {
  x: 0.8, y: 0.4, w: 4, h: 0.6, fontSize: 24, color: DARK_TEXT, fontFace: "Arial", bold: true, margin: 0
});
s14.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.2, w: 8, h: 3.5,
  fill: { color: WHITE }
});
s14.addText("一年后回头看——", {
  x: 1.2, y: 1.5, w: 7, h: 0.5, fontSize: 18, color: DARK_TEXT, fontFace: "Arial", align: "center", margin: 0
});
s14.addText("你知道得更多了", {
  x: 1.2, y: 2.0, w: 7, h: 0.5, fontSize: 20, color: DARK_TEXT, fontFace: "Arial", align: "center", margin: 0
});
s14.addText("问题也更难了", {
  x: 1.2, y: 2.5, w: 7, h: 0.5, fontSize: 20, color: DARK_TEXT, fontFace: "Arial", align: "center", margin: 0
});
s14.addText("但你想继续", {
  x: 1.2, y: 3.0, w: 7, h: 0.5, fontSize: 22, color: GOLD, fontFace: "Arial", bold: true, align: "center", margin: 0
});
s14.addText("螺旋上升 🌀  ≠  原地循环 ⟳", {
  x: 1.2, y: 3.7, w: 7, h: 0.4, fontSize: 14, color: "888888", fontFace: "Arial", align: "center", margin: 0
});

// Slide 15: Self-test table
let s15 = pres.addSlide();
s15.background = { color: LIGHT_BG };
s15.addText("三标自测表", {
  x: 0.8, y: 0.4, w: 4, h: 0.6, fontSize: 22, color: DARK_TEXT, fontFace: "Arial", bold: true, margin: 0
});
s15.addText("给每个方向打分（0-10）", {
  x: 0.8, y: 1.0, w: 5, h: 0.4, fontSize: 14, color: "888888", fontFace: "Arial", margin: 0
});

// Table
const tableHeader = [
  { text: "方向", options: { fill: { color: DEEP_BLUE }, color: WHITE, bold: true, fontSize: 14, align: "center", fontFace: "Arial" } },
  { text: "承诺", options: { fill: { color: DEEP_BLUE }, color: WHITE, bold: true, fontSize: 14, align: "center", fontFace: "Arial" } },
  { text: "承受", options: { fill: { color: DEEP_BLUE }, color: WHITE, bold: true, fontSize: 14, align: "center", fontFace: "Arial" } },
  { text: "生长", options: { fill: { color: DEEP_BLUE }, color: WHITE, bold: true, fontSize: 14, align: "center", fontFace: "Arial" } },
  { text: "总分", options: { fill: { color: GOLD }, color: WHITE, bold: true, fontSize: 14, align: "center", fontFace: "Arial" } }
];
const tableData = [
  tableHeader,
  [{ text: "方向1", options: { fontSize: 13, align: "center" } }, "", "", "", ""],
  [{ text: "方向2", options: { fontSize: 13, align: "center" } }, "", "", "", ""],
  [{ text: "方向3", options: { fontSize: 13, align: "center" } }, "", "", "", ""]
];
s15.addTable(tableData, {
  x: 0.8, y: 1.6, w: 8, h: 2.0,
  colW: [2, 1.5, 1.5, 1.5, 1.5],
  border: { pt: 0.5, color: "DDDDDD" }
});

s15.addText("> 20分 → 你可能找到了 ✅", {
  x: 0.8, y: 3.8, w: 4, h: 0.4, fontSize: 14, color: "2E7D32", fontFace: "Arial", bold: true, margin: 0
});
s15.addText("< 15分 → 放弃或降级 ❌", {
  x: 0.8, y: 4.2, w: 4, h: 0.4, fontSize: 14, color: "C62828", fontFace: "Arial", bold: true, margin: 0
});

// Slide 16: Homework
let s16 = pres.addSlide();
s16.background = { color: LIGHT_BG };
s16.addText("📝 今天的功课", {
  x: 0.8, y: 0.4, w: 4, h: 0.6, fontSize: 22, color: DARK_TEXT, fontFace: "Arial", bold: true, margin: 0
});
s16.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 1.2, w: 8, h: 3.5,
  fill: { color: WHITE }
});
s16.addText("① 选最像愿力的一件事", {
  x: 1.2, y: 1.5, w: 7, h: 0.5, fontSize: 18, color: DARK_TEXT, fontFace: "Arial", margin: 0
});
s16.addText("② 三标打分", {
  x: 1.2, y: 2.2, w: 7, h: 0.5, fontSize: 18, color: DARK_TEXT, fontFace: "Arial", margin: 0
});
s16.addText('③ 写一段话：\n"它值得我一辈子做吗？"', {
  x: 1.2, y: 2.9, w: 7, h: 0.8, fontSize: 18, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s16.addText("评论区见 👇", {
  x: 1.2, y: 3.9, w: 4, h: 0.4, fontSize: 14, color: "888888", fontFace: "Arial", margin: 0
});

// Slide 17: Final preview
let s17 = pres.addSlide();
s17.background = { color: DEEP_BLUE };
s17.addText("你已经找到了愿力。", {
  x: 0.8, y: 1.0, w: 8, h: 0.6, fontSize: 16, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});
s17.addText("为什么还是动不了？", {
  x: 0.8, y: 1.7, w: 8, h: 0.8, fontSize: 34, color: WHITE, fontFace: "Arial", bold: true, margin: 0
});
s17.addText("不是意志力问题", {
  x: 0.8, y: 2.8, w: 8, h: 0.6, fontSize: 20, color: "AAAAAA", fontFace: "Arial", margin: 0
});
s17.addText("🔥 明天揭秘", {
  x: 0.8, y: 4.0, w: 4, h: 0.5, fontSize: 20, color: GOLD, fontFace: "Arial", bold: true, margin: 0
});

// Write file
pres.writeFile({ fileName: "Day1-2-课件.pptx" })
  .then(() => console.log("OK"))
  .catch(err => console.error(err));
