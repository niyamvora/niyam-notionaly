// OpCreative's morph-pairs test, run against library.html on the real engine: every base/twin
// pair must build a plan and morph to a drawable path halfway through. A smear or an empty
// frame both show up as a `d` that isn't a path. Run by build_library.py:  bun check_morph.js
const fs = require("fs");
const here = __dirname;
const MI = new Function(fs.readFileSync(`${here}/morphicons.iife.js`, "utf8") + ";return morphicons")();
const html = fs.readFileSync(process.argv[2] || `${here}/library.html`, "utf8");
const unescape = s => s.replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
let n = 0;
for (const m of html.matchAll(/data-morph="([^"]+)"/g)) {
  const cfg = JSON.parse(unescape(m[1]));
  const plan = MI.buildPlan(MI.resampleIcon(cfg.from), MI.resampleIcon(cfg.to));
  const out = MI.allocOutputs(plan);
  MI.interpPolar(plan, 0.5, out);
  const d = MI.serialize(out, plan.items.map(it => it.closed));
  if (!/^M/.test(d) || d.length < 20 || d.includes("NaN")) throw new Error(`${cfg.name}: midpoint frame is not a path`);
  if (cfg.piv.length !== MI.resampleIcon(cfg.from).length) throw new Error(`${cfg.name}: pivot table misaligned`);
  n++;
}
if (n === 0) throw new Error("no morph pairs found in library.html");
console.log(`morph pairs ok: ${n} (${MI.resampleIcon("M0 0L1 1").length ? "engine live" : "?"})`);
