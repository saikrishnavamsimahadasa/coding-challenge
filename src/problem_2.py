import mysql.connector
import os
import csv
import time


def data_ingestion(station_id, recorded_date, max_temp, min_temp, precipitation):
    try:
        sql_Query = "REPLACE INTO WeatherData VALUES (%s,%s,%s,%s,%s)"
        columns = (station_id, recorded_date,
                   max_temp, min_temp, precipitation)
        cursor.execute(sql_Query, columns)
        connection.commit()

        # updating the number of records ingested
        global count
        count += 1

    except mysql.connector.Error as e:
        print("Error ingesting data to MySQL table: ", e)


def read_files(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter="\t")

        # making the station_id as the file name
        station_id = file_path[8:-4]

        for row in reader:
            (recorded_date, max_temp, min_temp, precipitation) = row

            # Changing the missing values to Null before ingesting to the database table
            if max_temp != "-9999":
                max_temp = int(max_temp)/10
            else:
                max_temp = None

            if min_temp != "-9999":
                min_temp = int(min_temp)/10
            else:
                min_temp = None

            if precipitation != "-9999":
                precipitation = int(precipitation)/100
            else:
                precipitation = None

            # Calling the function for ingesting the modified data
            data_ingestion(station_id, recorded_date,
                           max_temp, min_temp, precipitation)


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

    # Reading all the files from wx_data folder
    count = 0
    path = r"wx_data"
    for file in os.listdir(path):
        file_path = f"{path}/{file}"
        read_files(file_path)


except mysql.connector.Error as e:
    print("Error connecting to MySQL : ", e)


finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")

# Program End
end_time = time.time()
elapsed_time = end_time - start_time
print("Total time taken to ingest the weather data into the database : ",
      elapsed_time, " seconds")
print("Total number of weather records ingested into the database table : ", count)
