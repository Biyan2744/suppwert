/* Service Worker:
   - HTML (Navigationen): NETWORK-FIRST — Inhalte aendern sich woechentlich, Besucher sollen
     nie eine veraltete Seite sehen; der Cache ist nur Offline-Fallback.
   - Assets (Bilder, Fonts, Manifest): stale-while-revalidate — aendern sich praktisch nie.
   Externe Hosts (Shopify-CDN) laufen bewusst am Cache vorbei. */
const CACHE = "mn-vergleich-v2";
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  const isDoc = e.request.mode === "navigate" || u.pathname.endsWith(".html");
  if (isDoc) {
    e.respondWith((async () => {
      try {
        const r = await fetch(e.request);
        if (r && r.ok) (await caches.open(CACHE)).put(e.request, r.clone());
        return r;
      } catch (err) {
        const hit = await caches.match(e.request);
        if (hit) return hit;
        throw err;
      }
    })());
    return;
  }
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(e.request);
    const net = fetch(e.request).then(r => { if (r && r.ok) c.put(e.request, r.clone()); return r; }).catch(() => hit);
    return hit || net;
  }));
});
