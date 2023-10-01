LOAD DATA INFILE '/var/lib/mysql-files/rand-x-y-data.csv'
INTO TABLE cartesian_coordinate
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
