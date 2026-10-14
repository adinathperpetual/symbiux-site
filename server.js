// Zero-dependency static server for the Symbiux clone.
// Usage: node server.js   (PORT env var optional, default 8080)
const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "public");
const PORT = Number(process.env.PORT) || 8080;

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
  ".txt": "text/plain; charset=utf-8",
};

function send(res, file, status = 200) {
  const ext = path.extname(file).toLowerCase();
  const headers = { "Content-Type": TYPES[ext] || "application/octet-stream" };
  // Hashed build assets can be cached forever; HTML must stay fresh.
  headers["Cache-Control"] = file.includes(`${path.sep}assets${path.sep}`)
    ? "public, max-age=31536000, immutable"
    : "no-cache";
  res.writeHead(status, headers);
  fs.createReadStream(file).pipe(res);
}

http
  .createServer((req, res) => {
    let urlPath;
    try {
      urlPath = decodeURIComponent(new URL(req.url, "http://x").pathname);
    } catch {
      res.writeHead(400).end("Bad request");
      return;
    }
    const file = path.normalize(path.join(ROOT, urlPath));
    if (!file.startsWith(ROOT)) {
      res.writeHead(403).end("Forbidden");
      return;
    }
    fs.stat(file, (err, st) => {
      if (!err && st.isFile()) return send(res, file);
      if (!err && st.isDirectory() && fs.existsSync(path.join(file, "index.html")))
        return send(res, path.join(file, "index.html"));
      // Unknown asset -> real 404; any other path -> SPA fallback to index.html
      if (urlPath.startsWith("/assets/")) {
        res.writeHead(404).end("Not found");
        return;
      }
      send(res, path.join(ROOT, "index.html"));
    });
  })
  .listen(PORT, () => console.log(`Symbiux clone running at http://localhost:${PORT}`));
