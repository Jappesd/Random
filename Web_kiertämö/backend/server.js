const express = require("express");
const path = require("path");
const Database = require("better-sqlite3");
require("dotenv").config();
const app = express();
const PORT = 3000;

//middleware
app.use(express.json());

app.use(express.static(path.join(__dirname, "../frontend")));

//database

const db = new Database(path.join(__dirname, "db", "database.sqlite"));
db.prepare(
  `
  CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`,
).run();

// admin auth
function requireAdmin(req, res, next) {
  const key = req.headers["x-admin-key"];

  if (!key || key !== process.env.ADMIN_KEY) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  next();
}

// routes
app.post("/rate", (req, res) => {
  const { rating } = req.body;
  const validRatings = ["huono", "ok", "hyvä"];
  // basic validation
  if (!validRatings.includes(rating)) {
    return res.status(400).json({ error: "invalid rating" });
  }

  try {
    const stmt = db.prepare("INSERT INTO ratings (rating) VALUES (?)");
    stmt.run(rating);
    res.status(200).json({ success: true });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Database error" });
  }
});
app.get("/stats", requireAdmin, (req, res) => {
  try {
    const row = db
      .prepare(
        `
            SELECT rating, COUNT(*) as count
            FROM ratings
            GROUP BY rating
            `,
      )
      .all();
    res.json(row);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});
// export to csv
app.get("/export.csv", requireAdmin, (req, res) => {
  try {
    const rows = db
      .prepare(
        `
            SELECT id, rating, created_at
            FROM ratings
            ORDER BY created_at ASC
            `,
      )
      .all();

    //CSV header
    let csv = "id,rating,created_at\n";
    // rows
    for (const row of rows) {
      csv += `${row.id},${row.rating},${row.created_at}\n`;
    }

    res.setHeader("Content-Type", "text/csv");
    res.setHeader("Content-Disposition", "attachment; filename=ratings.csv");
    res.send(csv);
  } catch (err) {
    console.error("CSV EXPORT ERROR:", err);
    res.status(500).send("Export failed");
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Arvostelu serveri käynnissä portissa ${PORT}`);
});
