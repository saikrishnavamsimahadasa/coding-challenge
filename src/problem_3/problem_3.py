import mysql.connector
import time


def data_ingestion(station_id, recorded_year, avg_max_temp, avg_min_temp, total_precipitation):
    try:
        sql_Query = "REPLACE INTO WeatherAnalysis VALUES (%s,%s,%s,%s,%s)"
        columns = (station_id, recorded_year,
                   avg_max_temp, avg_min_temp, total_precipitation)
        cursor.execute(sql_Query, columns)
        connection.commit()

        # updating the number of records ingested
        global count
        count += 1

    except mysql.connector.Error as e:
        print("Error ingesting data to MySQL table: ", e)


# Program start
start_time = time.time()

try:
    # Establishing MySQL connection
    connection = mysql.connector.connect(host='localhost',
                                         database='CORTEVA',
                                         user='sai',
                                         password='password',
                                         auth_plugin='mysql_native_password')
    print("MySQL connection is established")
    cursor = connection.cursor()

    sql_select_Query = "SELECT Station_ID, YEAR(Recorded_date), AVG(Max_temp) as Avg_max_temp, AVG(Min_temp) as Avg_min_temp, SUM(Precipitation) as Total_precipitation FROM WeatherData GROUP BY Station_ID, YEAR(Recorded_date)"
    cursor.execute(sql_select_Query)

    # get all records
    records = cursor.fetchall()
    count = 0
    for row in records:
        (station_id, recorded_year, avg_max_temp,
         avg_min_temp, total_precipitation) = row

        # calling function to insert the weather analysis data
        data_ingestion(station_id, recorded_year, avg_max_temp,
                       avg_min_temp, total_precipitation)


except mysql.connector.Error as e:
    print("Error retriving weather data : ", e)


finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")

# Program End
end_time = time.time()
elapsed_time = end_time - start_time
print("Total time taken to ingest the weather stats into the database : ",
      elapsed_time, " seconds")
print("Total number of weather stats ingested into the database table : ", count)
