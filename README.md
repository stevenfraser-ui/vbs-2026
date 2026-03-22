# VBS 2026

## Keypad App (`code/keypad`)

Requires [Node.js / npm](https://nodejs.org).

```bash
cd code/keypad
npm install          # first time only
npm run seed         # writes agents to database.sqlite (edit db/seed.js to add/remove agents)
npm start            # serves the app at http://localhost:3000
```

To add or change agents, edit the `agents` array in [code/keypad/db/seed.js](code/keypad/db/seed.js) and re-run `npm run seed`. Agents removed from the list are deleted from the database automatically.
