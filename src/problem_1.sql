SHOW DATABASES;

/* Creating a new database */

CREATE DATABASE CORTEVA;


/* Creating an user and granting permissions to work on corteva database */

CREATE USER 'sai'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL PRIVILEGES ON CORTEVA.* TO 'sai'@'%';
FLUSH PRIVILEGES;


/* Using corteva database */

USE CORTEVA;
-- SHOW TABLES;


/* Creating WeatherData table*/

CREATE TABLE WeatherData (
    Station_ID VARCHAR(20) NOT NULL,
    Recorded_Date DATE NOT NULL,
	Max_temp DECIMAL(4,1),
	Min_temp DECIMAL(4,1),
	Precipitation DECIMAL(4,2),
    CONSTRAINT PK_ID_Date PRIMARY KEY (Station_ID, Recorded_Date)
);

SHOW TABLES;



