
/* Creating the Weather stats Analysis table */

CREATE TABLE WeatherAnalysis (
    Station_ID VARCHAR(20) NOT NULL,
    Recorded_year YEAR NOT NULL,
	Avg_max_temp DECIMAL(10,5),
	Avg_min_temp DECIMAL(10,5),
	Total_precipitation DECIMAL(10,2),
    CONSTRAINT PK_ID_Year PRIMARY KEY (Station_ID, Recorded_Year)
);