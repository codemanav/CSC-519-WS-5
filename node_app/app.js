const express = require('express');
const mysql = require('mysql2');

const app = express();
const port = 1717;

const dbHost = process.env.DB_HOST;
const dbUser = process.env.DB_USER;
const mysqlPassword = process.env.DB_PASSWORD;
const dbName = 'coordinates';

const connection = mysql.createConnection({
  host: dbHost,
  user: dbUser,
  password: mysqlPassword,
  database: dbName
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL database:', err);
    return;
  }
  console.log('Connected to MySQL database');

  app.get('/', async (req, res) => {
    try {
      const randomPoint = getRandomPoint();
      const closestPoint = await findClosestPoint(randomPoint);

      res.json({
        randomPoint,
        closestPoint,
        distance: closestPoint[0].distance.toFixed(2),
      });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  app.listen(port, () => {
    console.log(`Node.js app is running on port ${port}`);
  });
});

function getRandomPoint() {
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  return { x, y };
}

function findClosestPoint(randomPoint) {
  return new Promise((resolve, reject) => {
    const query = `SELECT x, y,
                   SQRT(POW(x - ?, 2) + POW(y - ?, 2)) AS distance
                   FROM cartesian_coordinate
                   ORDER BY distance
                   LIMIT 1`;
    connection.query(query, [randomPoint.x, randomPoint.y], (err, result, fields) => {
      if (err) {
        console.error('Error occurred while executing query -> ', err);
        reject(err);
      } else {
        resolve(result);
      }
    });
  });
}
