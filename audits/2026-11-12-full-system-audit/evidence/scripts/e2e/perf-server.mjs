// AUD-2026-11-12 · D2 · performans ölçümü için üretim benzeri sunucu (yalnızca localhost:4173).
// frontend-tst/dist'i deploy/nginx/davetkart.conf'taki kurallarla sunar: gzip (css/js/json/svg/txt/html),
// /assets/ → immutable, bilinmeyen yol → index.html, /api ve /storage → backend-e2e (127.0.0.1:8000).
// `vite preview` sıkıştırma yapmadığı için aktarım boyutlarını ~3 kat büyük gösterirdi.
import http from 'node:http';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { extname, join, normalize } from 'node:path';
import { createGzip } from 'node:zlib';

const DIST = 'D:/Projects/davetkart/_audit-snap/frontend-tst/dist';
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.mp4': 'video/mp4', '.webm': 'video/webm', '.txt': 'text/plain' };
const GZIP = new Set(['.html', '.js', '.css', '.json', '.svg', '.txt']);

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/storage/')) {
    const p = http.request({ host: '127.0.0.1', port: 8000, path: req.url, method: req.method, headers: { ...req.headers, host: 'localhost:8000' } }, (r) => { res.writeHead(r.statusCode, r.headers); r.pipe(res); });
    p.on('error', () => { res.writeHead(502); res.end(); });
    req.pipe(p);
    return;
  }
  let file = normalize(join(DIST, decodeURIComponent(url.pathname)));
  if (!file.startsWith(normalize(DIST)) || !existsSync(file) || statSync(file).isDirectory()) {
    if (url.pathname.startsWith('/assets/')) { res.writeHead(404); res.end(); return; }
    file = join(DIST, 'index.html');
  }
  const ext = extname(file);
  const headers = { 'Content-Type': TYPES[ext] ?? 'application/octet-stream' };
  if (url.pathname.startsWith('/assets/')) headers['Cache-Control'] = 'public, max-age=31536000, immutable';
  else if (file.endsWith('index.html')) headers['Cache-Control'] = 'no-cache';
  const gz = GZIP.has(ext) && /gzip/.test(req.headers['accept-encoding'] ?? '') && statSync(file).size >= 1024;
  if (gz) { headers['Content-Encoding'] = 'gzip'; headers.Vary = 'Accept-Encoding'; } else headers['Content-Length'] = statSync(file).size;
  res.writeHead(200, headers);
  gz ? createReadStream(file).pipe(createGzip({ level: 6 })).pipe(res) : createReadStream(file).pipe(res);
}).listen(4173, '127.0.0.1', () => console.log('perf-server hazır: http://localhost:4173'));
