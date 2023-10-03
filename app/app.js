var express = require('express');
var app = express();
var mysql = require('mysql');
const argv = require('yargs').argv;
const host_db = argv.db_host;
const db_user = argv.db_user;
const db_pass = argv.db_pass;
const db = argv.db;
const db_port = argv.db_port;



app.get('/', function (req, res) {

    // Configuration object for storing the mysql database credentials
    var dbConfig = {
        user: db_user,
        password: db_pass,
        database: db,
        host: host_db,
        port: db_port

    };

    // Create a connection to the database
    var sql_connection = mysql.createConnection(dbConfig);

    // Function to Generate random point
    function generateRandomPoint() {
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      return { x, y };
    }
    // Generate the Random Point 
    const myPoint = generateRandomPoint();

    // For debugging
    console.log(myPoint)

    // establish a connection to the database
    sql_connection.connect(function (err) {
        if (err) {
            console.error('Error connecting to MySQL:', err);
            return;
        }

        console.log('Successfully Connected to MySQL');

        // Query to find the distances

        const q = `
        SELECT x, y,
        SQRT(POWER(x - ${myPoint.x}, 2) + POWER(y - ${myPoint.y}, 2)) as euclidean_distances
        FROM table_ws5
        ORDER BY euclidean_distances
        LIMIT 1`;

        // query to the database and get the records
        sql_connection.query(q, function (err, results, fields) {
            if (err) {
                console.error('Error executing query:', err);
                res.status(500).send('Internal Server Error');
                return;
            }

            res.send(`
            <h1> The randomly generated point : (${myPoint.x}, ${myPoint.y}) <br> The Nearest point is: (${results[0].x}, ${results[0].y}) <br> The Distance between them: ${results[0].euclidean_distances}</h1>
            `);
        });

        // close the connection
        sql_connection.end(function (err) {
            if (err) {
                console.error('Error closing MySQL connection:', err);
            }
            console.log('Connection to the server is closed');
        });
    });
});

var server = app.listen(3000, function () {
    console.log('Server is listening');
});
