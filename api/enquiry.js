// Vercel serverless function: receives booking requests and newsletter sign-ups.
// Secrets live only in Vercel environment variables (see .env.example), never in front-end code.

const WINDOW_MS = 10 * 60 * 1000;   // rate-limit window
const MAX_PER_WINDOW = 5;           // requests per IP per window
const MAX_BODY = 8 * 1024;          // bytes
const NEEDS = ['Start dialysis', 'Transfer to Nikko', 'Holiday dialysis', 'Check my cover', 'Book a tour', 'Diet & education', 'Something else'];

// Best-effort, per-instance memory. For strict limits across instances, swap for Upstash Redis / Vercel KV.
const hits = new Map();
const seen = new Map();

function clientIp(req) {
  const xf = req.headers['x-forwarded-for'] || '';
  return (Array.isArray(xf) ? xf[0] : xf).split(',')[0].trim() || req.socket?.remoteAddress || 'unknown';
}
function limited(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  list.push(now);
  hits.set(ip, list);
  if (hits.size > 5000) hits.clear();
  return list.length > MAX_PER_WINDOW;
}
function duplicate(key) {
  if (!key) return false;
  const now = Date.now();
  for (const [k, t] of seen) if (now - t > 86400000) seen.delete(k);
  if (seen.has(key)) return true;
  seen.set(key, now);
  return false;
}
const clean = (v, max) => (typeof v === 'string' ? v.replace(/[\u0000-\u001F\u007F]/g, ' ').trim().slice(0, max) : '');
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const isEmail = (s) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s);
const isPhone = (s) => /^[0-9+ ()-]{9,18}$/.test(s) && s.replace(/\D/g, '').length >= 9;

function allowedOrigin(req) {
  const origin = req.headers.origin;
  if (!origin) return true; // same-origin form posts from some browsers omit Origin
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const extra = (process.env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
  try { return new URL(origin).host === host || extra.includes(origin); } catch { return false; }
}

async function sendEmail({ subject, html, replyTo }) {
  const key = process.env.RESEND_API_KEY, to = process.env.ENQUIRY_TO, from = process.env.ENQUIRY_FROM;
  if (!key || !to || !from) throw new Error('Email not configured');
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from, to: to.split(',').map((s) => s.trim()), subject, html, reply_to: replyTo || undefined }),
  });
  if (!r.ok) throw new Error('Email provider error ' + r.status);
}
async function webhook(payload) {
  const url = process.env.ENQUIRY_WEBHOOK_URL;
  if (!url) return;
  try { await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }); } catch (e) { console.error('webhook failed', e.message); }
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ error: 'Method not allowed' }); }
  if (!allowedOrigin(req)) return res.status(403).json({ error: 'Forbidden' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { return res.status(400).json({ error: 'Invalid JSON' }); } }
  if (!body || typeof body !== 'object') return res.status(400).json({ error: 'Invalid request' });
  if (JSON.stringify(body).length > MAX_BODY) return res.status(413).json({ error: 'Request too large' });

  // Honeypot: bots fill the hidden "website" field. Pretend success, do nothing.
  if (clean(body.website, 200)) return res.status(200).json({ ok: true });

  if (limited(clientIp(req))) return res.status(429).json({ error: 'Too many requests. Please call us instead.' });
  if (duplicate(clean(body.idempotencyKey, 80))) return res.status(200).json({ ok: true, duplicate: true });

  const received = new Date().toLocaleString('en-KE', { timeZone: 'Africa/Nairobi', dateStyle: 'medium', timeStyle: 'short' });

  try {
    if (body.type === 'newsletter') {
      const email = clean(body.email, 120).toLowerCase();
      if (!isEmail(email) || body.consent !== true) return res.status(422).json({ error: 'Please enter a valid email and tick consent.' });
      await sendEmail({ subject: 'Newsletter sign-up: ' + email, html: `<p>${esc(email)} subscribed to patient tips on ${esc(received)} (Nairobi time). Consent given via website.</p>` });
      await webhook({ type: 'newsletter', email, consent: true, received });
      return res.status(200).json({ ok: true });
    }

    const d = {
      needs: (Array.isArray(body.needs) ? body.needs : []).map((n) => clean(n, 40)).filter((n) => NEEDS.includes(n)),
      who: clean(body.who, 40), shift: clean(body.shift, 20), name: clean(body.name, 80), phone: clean(body.phone, 18),
      email: clean(body.email, 120).toLowerCase(), dates: clean(body.dates, 60), unit: clean(body.unit, 100),
      method: clean(body.method, 20), time: clean(body.time, 20), notes: clean(body.notes, 1000),
      marketing: body.marketing === 'yes', consent: body.consent === 'yes', tz: clean(body.tz, 60), page: clean(body.page, 60),
    };
    const errors = [];
    if (!d.needs.length) errors.push('needs');
    if (d.name.length < 2) errors.push('name');
    if (!isPhone(d.phone)) errors.push('phone');
    if (d.email && !isEmail(d.email)) errors.push('email');
    if (!d.consent) errors.push('consent');
    if (errors.length) return res.status(422).json({ error: 'Please check: ' + errors.join(', ') });

    const rows = [
      ['Needs', d.needs.join(', ')], ['For', d.who], ['Preferred shift', d.shift || '—'], ['Name', d.name], ['Phone', d.phone],
      ['Email', d.email || '—'], ['Travel dates', d.dates || '—'], ['Current unit', d.unit || '—'], ['Contact by', d.method],
      ['Best time (Nairobi)', d.time], ['Visitor time zone', d.tz || '—'], ['Notes', d.notes || '—'],
      ['Consent to contact', 'Yes'], ['Marketing opt-in', d.marketing ? 'Yes' : 'No'], ['Received', received + ' (Nairobi time)'],
    ];
    const html = `<h2 style="font-family:sans-serif">New website enquiry</h2><table style="font-family:sans-serif;border-collapse:collapse">${rows
      .map(([k, v]) => `<tr><td style="padding:6px 12px;color:#4A5878;vertical-align:top">${esc(k)}</td><td style="padding:6px 12px">${esc(v).replace(/\n/g, '<br>')}</td></tr>`)
      .join('')}</table>`;
    await sendEmail({ subject: `Enquiry: ${d.needs.join(', ')} — ${d.name}`, html, replyTo: d.email || undefined });
    await webhook({ type: 'enquiry', ...d, received });
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('enquiry failed', e.message);
    return res.status(500).json({ error: 'Could not send. Please call or WhatsApp us.' });
  }
};
