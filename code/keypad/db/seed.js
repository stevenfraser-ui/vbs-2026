/**
 * db/seed.js — Populate the agents table.
 *
 * Usage:  npm run seed
 *
 * Each agent entry has:
 *   name       — Displayed name / call sign shown after access is granted
 *   code       — The numeric PIN they enter on the keypad (must be unique)
 */

const Database = require('better-sqlite3');
const path = require('path');

const db = new Database(path.join(__dirname, '..', 'database.sqlite'));

db.exec(`
  CREATE TABLE IF NOT EXISTS agents (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    code       TEXT    UNIQUE NOT NULL
  )
`);

// ── Agent roster ─────────────────────────────────────────────────────────────
// Add / edit agents here, then re-run:  npm run seed
const agents = [
  {
    name:      'Daniel Worthington',
    code:      '0167',
  },
  {
    name:      'Josiah Worthington',
    code:      '5714',
  },
  {
    name:      'Revan Worthington',
    code:      '3621',
  },
  {
    name:      'Nathan Worthington',
    code:      '4521',
  },
];

// ── Insert / update / delete ──────────────────────────────────────────────────
const upsert = db.prepare(`
  INSERT INTO agents (name, code)
  VALUES (?, ?)
  ON CONFLICT(code) DO UPDATE SET
    name       = excluded.name
`);

// Deletes any agent whose code is no longer in the list
const deleteMissing = db.prepare(`
  DELETE FROM agents WHERE code NOT IN (SELECT value FROM json_each(?))
`);

const seedAll = db.transaction((list) => {
  const codes = JSON.stringify(list.map(a => a.code));
  const { changes: deleted } = deleteMissing.run(codes);
  for (const agent of list) {
    upsert.run(agent.name, agent.code);
  }
  return deleted;
});

const deleted = seedAll(agents);

console.log(`✔  Seeded ${agents.length} agent(s). Removed ${deleted} stale agent(s).`);
db.close();
