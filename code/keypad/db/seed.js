/**
 * db/seed.js — Populate the agents table.
 *
 * Usage:  npm run seed
 *
 * Each agent entry has:
 *   name       — Displayed name / call sign shown after access is granted
 *   code       — The numeric PIN they enter on the keypad (must be unique)
 *   soundFile  — Path (relative to the keypad root) to the audio played on
 *                successful login.  Drop per-agent MP3s into:
 *                  assets/sounds/agents/<filename>.mp3
 *                and reference them as 'assets/sounds/agents/<filename>.mp3'
 *                Fall back to 'assets/sounds/access-granted.mp3' until a
 *                custom file exists.
 */

const Database = require('better-sqlite3');
const path = require('path');

const db = new Database(path.join(__dirname, '..', 'database.sqlite'));

db.exec(`
  CREATE TABLE IF NOT EXISTS agents (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    code       TEXT    UNIQUE NOT NULL,
    sound_file TEXT    NOT NULL DEFAULT 'assets/sounds/access-granted.mp3'
  )
`);

// ── Agent roster ─────────────────────────────────────────────────────────────
// Add / edit agents here, then re-run:  npm run seed
const agents = [
  {
    name:      'Agent Daniel Worthington',
    code:      '0167',
    soundFile: 'assets/sounds/access-granted.mp3',   // replace with custom file when ready
  },
  // Example with a custom per-agent sound:
  // {
  //   name:      'Agent Viper',
  //   code:      '1138',
  //   soundFile: 'assets/sounds/agents/viper.mp3',
  // },
];

// ── Insert / update / delete ──────────────────────────────────────────────────
const upsert = db.prepare(`
  INSERT INTO agents (name, code, sound_file)
  VALUES (?, ?, ?)
  ON CONFLICT(code) DO UPDATE SET
    name       = excluded.name,
    sound_file = excluded.sound_file
`);

// Deletes any agent whose code is no longer in the list
const deleteMissing = db.prepare(`
  DELETE FROM agents WHERE code NOT IN (SELECT value FROM json_each(?))
`);

const seedAll = db.transaction((list) => {
  const codes = JSON.stringify(list.map(a => a.code));
  const { changes: deleted } = deleteMissing.run(codes);
  for (const agent of list) {
    upsert.run(agent.name, agent.code, agent.soundFile);
  }
  return deleted;
});

const deleted = seedAll(agents);

console.log(`✔  Seeded ${agents.length} agent(s). Removed ${deleted} stale agent(s).`);
db.close();
