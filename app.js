const express = require("express");
const mysql = require("mysql2/promise");

const app = express();
const PORT = process.env.PORT || 80;

const pool = mysql.createPool({
  host: process.env.DB_HOST || "localhost",
  user: process.env.DB_USER || "myuser",
  password: process.env.DB_PASS || "mypassword",
  database: process.env.DB_NAME || "pointsdb",
  port: process.env.DB_PORT || 3306,
  waitForConnections: true,
  connectionLimit: 10,
});

function randomPoint() {
  return {
    x: Math.random() * 100,
    y: Math.random() * 100
  };
}

app.get("/", async (req, res) => {
  try {
    const rand = randomPoint();

    const [rows] = await pool.query(
      "SELECT x, y, SQRT(POW(x - ?, 2) + POW(y - ?, 2)) AS dist FROM points ORDER BY dist ASC LIMIT 1",
      [rand.x, rand.y]
    );

    if (rows.length > 0) {
      res.json({
        random_point: rand,
        closest_point: { x: rows[0].x, y: rows[0].y },
        distance: rows[0].dist
      });
    } else {
      res.json({ error: "No points found in database" });
    }
  } catch (err) {
    console.error(err);
    res.status(500).send("Error querying database");
  }
});

app.listen(PORT, () => {
  console.log(`App running on port ${PORT}`);
});
