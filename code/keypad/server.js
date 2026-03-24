const express = require('express');
const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 4000;

// ── Database ────────────────────────────────────────────────────────────────
const db = new Database(path.join(__dirname, 'database.sqlite'));

db.exec(`
  CREATE TABLE IF NOT EXISTS agents (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    code       TEXT    UNIQUE NOT NULL
  )
`);

// Prepared statements
const findAgent = db.prepare(
  'SELECT name FROM agents WHERE code = ?'
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

  const SOUNDS_DIR = "assets/sounds/"
  const agent = findAgent.get(code);
  const DEFAULT_SOUND = SOUNDS_DIR + "access-granted.mp3";

  if (agent) {
    const candidate = SOUNDS_DIR + "welcome-" + agent.name.toLowerCase().replace(/\s+/g, '-') + ".mp3";
    const sound_file = fs.existsSync(path.join(__dirname, candidate)) ? candidate : DEFAULT_SOUND;
    return res.json({
      valid: true,
      agentName: agent.name,
      soundFile: sound_file,
    });
  }

  return res.json({ valid: false });
});

// ── Start ────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`Keypad server running → http://localhost:${PORT}`);
});
