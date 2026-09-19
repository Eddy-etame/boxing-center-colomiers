/**
 * cdp.mjs — piloter un Chrome SANS TÊTE, à nu (aucune dépendance), pour VOIR avant
 * de juger (règle d'Eddy du 18/09 : « you can't hate on something you haven't set
 * your eyes on »). Le volet navigateur de la session se déclare « hidden » : les
 * images d'animation n'y tournent pas, et toute mesure de révélation y est fausse.
 * Ici la page est réellement rendue, à la taille demandée, avec une vraie molette.
 *
 *   const p = await ouvrir({ w: 1440, h: 900 });            // ou { w: 390, h: 844, mobile: true, dpr: 3 }
 *   await p.aller("https://…");  await p.attendre(3000);
 *   const v = await p.evalue("document.title");
 *   await p.molette(600, 10);     // 10 crans de 600 px, comme une main
 *   await p.capture("C:/…/x.png");  await p.fermer();
 */
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const CHROME = "C:/Users/Mommy Jayce/AppData/Local/Google/Chrome/Application/chrome.exe";
const pause = (ms) => new Promise((r) => setTimeout(r, ms));

export async function ouvrir({ w = 1440, h = 900, mobile = false, dpr = 1 } = {}) {
  const port = 9300 + Math.floor((process.pid + w) % 500);
  const profil = mkdtempSync(join(tmpdir(), "cdp-"));
  const proc = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profil}`,
    "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "--mute-audio", "--autoplay-policy=no-user-gesture-required",
    `--window-size=${w},${h}`, "about:blank"], { stdio: "ignore" });
  let cible;
  for (let i = 0; i < 60 && !cible; i++) {
    await pause(250);
    try { cible = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === "page"); } catch {}
  }
  if (!cible) { proc.kill(); throw new Error("Chrome sans tête ne répond pas"); }
  const ws = new WebSocket(cible.webSocketDebuggerUrl);
  await new Promise((ok, ko) => { ws.onopen = ok; ws.onerror = ko; });
  let n = 0;
  const attente = new Map();
  const ecoutes = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && attente.has(m.id)) { const { ok, ko } = attente.get(m.id); attente.delete(m.id); m.error ? ko(new Error(m.error.message)) : ok(m.result); }
    else if (m.method) ecoutes.forEach((f) => f(m));
  };
  const cmd = (method, params = {}) => new Promise((ok, ko) => { const id = ++n; attente.set(id, { ok, ko }); ws.send(JSON.stringify({ id, method, params })); });
  await cmd("Page.enable"); await cmd("Runtime.enable");
  await cmd("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: dpr, mobile });
  if (mobile) {
    await cmd("Emulation.setTouchEmulationEnabled", { enabled: true });
    await cmd("Emulation.setUserAgentOverride", { userAgent: "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36" });
  }
  const erreurs = [];
  ecoutes.push((m) => { if (m.method === "Runtime.exceptionThrown") erreurs.push(m.params.exceptionDetails?.exception?.description || m.params.exceptionDetails?.text); });
  return {
    erreurs,
    attendre: pause,
    async aller(url) {
      const charge = new Promise((ok) => { const f = (m) => { if (m.method === "Page.loadEventFired") { ecoutes.splice(ecoutes.indexOf(f), 1); ok(); } }; ecoutes.push(f); });
      await cmd("Page.navigate", { url });
      await Promise.race([charge, pause(20000)]);
    },
    async evalue(expression) {
      const r = await cmd("Runtime.evaluate", { expression: `(async()=>{ ${expression} })()`, awaitPromise: true, returnByValue: true });
      if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
      return r.result.value;
    },
    /** la molette d'une main : `fois` crans de `dy` pixels, espacés */
    async molette(dy, fois = 1, entre = 120) {
      for (let i = 0; i < fois; i++) {
        if (mobile) await cmd("Input.synthesizeScrollGesture", { x: Math.round(w / 2), y: Math.round(h / 2), yDistance: -dy, speed: 1600 });
        else await cmd("Input.dispatchMouseEvent", { type: "mouseWheel", x: Math.round(w / 2), y: Math.round(h / 2), deltaX: 0, deltaY: dy });
        await pause(entre);
      }
    },
    async capture(fichier) {
      const r = await cmd("Page.captureScreenshot", { format: "png" });
      writeFileSync(fichier, Buffer.from(r.data, "base64"));
      return fichier;
    },
    async fermer() { try { ws.close(); } catch {} proc.kill(); await pause(400); try { rmSync(profil, { recursive: true, force: true }); } catch {} },
  };
}
