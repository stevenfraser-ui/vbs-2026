const express = require('express');
const Database = require('better-sqlite3');
const path = require('path');

const app = express();
const PORT = 3000;

// ── Database ────────────────────────────────────────────────────────────────
const db = new Database(path.join(__dirname, 'database.sqlite'));

db.exec(`
  CREATE TABLE IF NOT EXISTS agents (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    code       TEXT    UNIQUE NOT NULL,
    sound_file TEXT    NOT NULL DEFAULT 'assets/sounds/access-granted.mp3'
  )
`);

// Prepared statements
const findAgent = db.prepare(
  'SELECT name, sound_file FROM agents WHERE code = ?'
);

// ── Middleware ───────────────────────────────────────────────────────────────
app.use(express.json());
app.use(express.static(__dirname));      // serves index.html, assets/, etc.

// ── API ──────────────────────────────────────────────────────────────────────
app.post('/api/validate', (req, res) => {
  const { code } = req.body;

  // Reject anything that isn't 1-6 digits
  if (!code || typeof code !== 'string' || !/^\d{1,6}$/.test(code)) {
    return res.status(400).json({ valid: false });
  }

  const agent = findAgent.get(code);

  if (agent) {
    return res.json({
      valid: true,
      agentName: agent.name,
      soundFile: agent.sound_file,
    });
  }

  return res.json({ valid: false });
});

// ── Start ────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`Keypad server running → http://localhost:${PORT}`);
});
