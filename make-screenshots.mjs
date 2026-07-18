// Screenshot-Paket der Suppwert-Seite für Design-Reviews (z. B. v0.dev / Design-KIs).
// Headless-Chrome/Edge via CDP (kein Puppeteer, Node >=22 hat WebSocket) — nötig, weil
// --window-size bei schmalen Breiten am Fenster-Minimum (~500px) scheitert und Hell/Dunkel
// über Emulation.setEmulatedMedia sauber erzwungen wird (die Seite folgt prefers-color-scheme).
//
//   node make-screenshots.mjs [--out <ordner>]   (Default: Desktop\suppwert-screenshots)
//
// Läuft gegen die lokale index.html (file://) — kein Server nötig.

import { spawn } from "node:child_process";
import { mkdir, writeFile, rm } from "node:fs/promises";
import { existsSync, readFileSync } from "node:fs";
import { tmpdir, homedir } from "node:os";
import path from "node:path";

const args = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i !== -1 && args[i + 1] ? args[i + 1] : fallback;
};
/* Windows leitet den sichtbaren Desktop oft auf OneDrive um — dort ablegen, wo Biyan ihn sieht */
const oneDriveDesktop = path.join(homedir(), "OneDrive", "Desktop");
const OUT = opt("out", path.join(existsSync(oneDriveDesktop) ? oneDriveDesktop : path.join(homedir(), "Desktop"), "suppwert-screenshots"));
const BASE = "file:///" + path.join(import.meta.dirname, "index.html").replaceAll("\\", "/");

const CHROME_PATHS = [
  process.env.CHROME_PATH,
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
].filter(Boolean);
const chrome = CHROME_PATHS.find((p) => existsSync(p));
if (!chrome) {
  console.error("Kein Chrome/Edge gefunden — CHROME_PATH setzen.");
  process.exit(1);
}

/** Minimaler CDP-Client über den Browser-WebSocket (flatten sessions). */
class Cdp {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.eventWaiters = [];
    ws.addEventListener("message", (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      } else if (msg.method) {
        this.eventWaiters = this.eventWaiters.filter((w) => {
          if (w.method === msg.method && (!w.sessionId || w.sessionId === msg.sessionId)) {
            w.resolve(msg.params);
            return false;
          }
          return true;
        });
      }
    });
  }
  send(method, params = {}, sessionId) {
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params, sessionId }));
    });
  }
  waitFor(method, sessionId, timeoutMs = 20000) {
    return new Promise((resolve, reject) => {
      const t = setTimeout(() => reject(new Error(`Timeout: ${method}`)), timeoutMs);
      this.eventWaiters.push({ method, sessionId, resolve: (p) => { clearTimeout(t); resolve(p); } });
    });
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function shoot(cdp, { file, hash, width, height, scheme }) {
  const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });
  const s = (m, p) => cdp.send(m, p, sessionId);
  try {
    await s("Page.enable");
    await s("Runtime.enable");
    await s("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: width < 700 });
    await s("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: scheme }] });
    const loaded = cdp.waitFor("Page.loadEventFired", sessionId);
    await s("Page.navigate", { url: BASE + (hash || "") });
    await loaded;
    await s("Runtime.evaluate", { expression: "document.fonts.ready.then(() => true)", awaitPromise: true });
    await sleep(2200); // Scroll-Reveal-Failsafe (1,6 s) + Entrance-Animationen abwarten
    const { data } = await s("Page.captureScreenshot", { format: "png" });
    const buf = Buffer.from(data, "base64");
    const out = path.join(OUT, file);
    await writeFile(out, buf);
    console.log(`OK ${file} (${buf.readUInt32BE(16)}x${buf.readUInt32BE(20)})`);
  } finally {
    await cdp.send("Target.closeTarget", { targetId });
  }
}

await mkdir(OUT, { recursive: true });
const profile = path.join(tmpdir(), `suppwert-shots-${Date.now()}`);
const proc = spawn(chrome, [
  "--headless=new",
  "--remote-debugging-port=0",
  `--user-data-dir=${profile}`,
  "--no-first-run",
  "--hide-scrollbars",
  "--force-color-profile=srgb",
  "about:blank",
]);
proc.on("error", (e) => { console.error("Browser-Start fehlgeschlagen:", e.message); process.exit(1); });

let port = null;
for (let i = 0; i < 60 && !port; i++) {
  await sleep(250);
  try { port = parseInt(readFileSync(path.join(profile, "DevToolsActivePort"), "utf8").split("\n")[0], 10) || null; } catch {}
}
if (!port) { console.error("Debug-Port nicht gefunden."); proc.kill(); process.exit(1); }

const { webSocketDebuggerUrl } = await fetch(`http://127.0.0.1:${port}/json/version`).then((r) => r.json());
const ws = new WebSocket(webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.addEventListener("open", res); ws.addEventListener("error", rej); });
const cdp = new Cdp(ws);

try {
  const SHOTS = [
    { file: "01-uebersicht-desktop-dunkel.png", hash: "",           width: 1440, height: 900,  scheme: "dark" },
    { file: "02-uebersicht-desktop-hell.png",   hash: "",           width: 1440, height: 900,  scheme: "light" },
    { file: "03-uebersicht-lang-dunkel.png",    hash: "",           width: 1440, height: 2600, scheme: "dark" },
    { file: "04-produkte-desktop-dunkel.png",   hash: "#produkte",  width: 1440, height: 2200, scheme: "dark" },
    { file: "05-produkte-desktop-hell.png",     hash: "#produkte",  width: 1440, height: 2200, scheme: "light" },
    { file: "06-sets-desktop-dunkel.png",       hash: "#sets",      width: 1440, height: 2200, scheme: "dark" },
    { file: "07-vergleich-desktop-dunkel.png",  hash: "#vergleich", width: 1440, height: 1400, scheme: "dark" },
    { file: "08-uebersicht-mobil-dunkel.png",   hash: "",           width: 375,  height: 812,  scheme: "dark" },
    { file: "09-uebersicht-mobil-hell.png",     hash: "",           width: 375,  height: 812,  scheme: "light" },
    { file: "10-produkte-mobil-dunkel.png",     hash: "#produkte",  width: 375,  height: 1600, scheme: "dark" },
  ];
  for (const sh of SHOTS) await shoot(cdp, sh);
  console.log(`Fertig -> ${OUT}`);
} finally {
  ws.close();
  proc.kill();
  await sleep(500);
  await rm(profile, { recursive: true, force: true }).catch(() => {});
}
