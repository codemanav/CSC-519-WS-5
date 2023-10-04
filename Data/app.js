/**
 * This is the Node.js server that will be running on the Data server.
 * @author Meles Meles 
 */
const express = require("express");
const redis = require("redis");
const { promisify } = require("util");
const app = express();
const port = 3000; // You can change this to another port if you like

// Initialize Redis client with password from environment variable
const client = redis.createClient({
  host: "127.0.0.1",
  port: 6379,
  password: process.env.REDIS_PASS,
});

// Handle Redis errors
client.on("error", (error) => {
  console.error(`Redis client encountered an error: ${error}`);
});

const getAsync = promisify(client.get).bind(client);

// Utility function to calculate Cartesian distance
const cartesianDistance = (x1, y1, x2, y2) => {
  return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
};

app.get("/", async (req, res) => {
  try {
    let x_rand = Math.random() * 100;
    let y_rand = Math.random() * 100;

    let closest_point = null;
    let min_distance = Infinity;

    // Using Redis SCAN to get all keys matching "point:*"
    let cursor = "0";
    do {
      const reply = await promisify(client.scan).bind(client)(
        cursor,
        "MATCH",
        "point:*"
      );
      cursor = reply[0];
      const keys = reply[1];

      for (let key of keys) {
        const point_json = await getAsync(key);
        const point = JSON.parse(point_json);
        const x = point.x;
        const y = point.y;

        const distance = cartesianDistance(x_rand, y_rand, x, y);

        if (distance < min_distance) {
          min_distance = distance;
          closest_point = point;
        }
      }
    } while (cursor !== "0");

    res.json({
      random_point: { x: x_rand, y: y_rand },
      closest_point: closest_point,
      distance: min_distance,
    });
  } catch (error) {
    console.error(
      "An error occurred while finding the closest point locally:",
      error
    );
    res.status(500).send("Internal server error");
  }
});

app.listen(port, () => {
  console.log(`Server running on http://0.0.0.0:${port}/`);
});
