from flask import Flask, request
from flask_mysqldb import MySQL
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# MySQL config
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "sai"
app.config['MYSQL_PASSWORD'] = "password"
app.config['MYSQL_DB'] = "CORTEVA"

mysql = MySQL(app)

# flask swagger config
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Weather Data and Stats API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/')
def index():
    return ("Please follow the link to use the WeatherData API --->>>>> http://localhost:5000/swagger/")


# GET Endpoint - /api/weather
@app.route('/api/weather/<int:page>')
def get_weather_data(page):

    # filter parameters
    if 'date' in request.args:
        date = request.args['date']
    else:
        date = None
    if 'station_id' in request.args:
        sid = request.args['station_id']
    else:
        sid = None

    # Pagination
    perpage = 10
    if page == 1:
        startat = 0
    else:
        startat = (page-1)*perpage

    cursor = mysql.connection.cursor()

    if date and sid:
        sql_query = "SELECT Station_ID, Recorded_date, Max_temp, Min_temp, Precipitation FROM WeatherData WHERE Recorded_date = %s and Station_ID = %s LIMIT %s, %s"
        fields = (date, sid, startat, perpage)
    elif date:
        sql_query = "SELECT Station_ID, Recorded_date, Max_temp, Min_temp, Precipitation FROM WeatherData WHERE Recorded_date = %s LIMIT %s, %s"
        fields = (date, startat, perpage)
    elif sid:
        sql_query = "SELECT Station_ID, Recorded_date, Max_temp, Min_temp, Precipitation FROM WeatherData WHERE Station_ID = %s LIMIT %s, %s"
        fields = (sid, startat, perpage)
    else:
        sql_query = "SELECT Station_ID, Recorded_date, Max_temp, Min_temp, Precipitation FROM WeatherData LIMIT %s, %s"
        fields = (startat, perpage)

    cursor.execute(sql_query, fields)

    records = list(cursor.fetchall())

    cursor.close()

    output = []
    for row in records:
        row_dict = {}
        row_dict['Station_ID'] = row[0]
        row_dict['Recorded_date'] = row[1]
        if row[2]:
            row_dict['Max_temp'] = float(row[2])
        else:
            row_dict['Max_temp'] = None
        if row[3]:
            row_dict['Min_temp'] = float(row[3])
        else:
            row_dict['Min_temp'] = None
        if row[4]:
            row_dict['Precipitation'] = float(row[4])
        else:
            row_dict['Precipitation'] = None

        output.append(row_dict)

    return output


# GET endpoint - /api/weather/stats
@app.route('/api/weather/stats/<int:page>')
def get_weather_stats(page):

    # filter parameters
    if 'year' in request.args:
        year = request.args['year']
    else:
        year = None
    if 'station_id' in request.args:
        sid = request.args['station_id']
    else:
        sid = None

    # Pagination
    perpage = 10
    if page == 1:
        startat = 0
    else:
        startat = (page-1)*perpage

    cursor = mysql.connection.cursor()

    if year and sid:
        sql_query = "SELECT Station_ID, Recorded_year, Avg_max_temp, Avg_min_temp, Total_precipitation FROM WeatherAnalysis WHERE Recorded_year = %s and Station_ID = %s LIMIT %s, %s"
        fields = (year, sid, startat, perpage)
    elif year:
        sql_query = "SELECT Station_ID, Recorded_year, Avg_max_temp, Avg_min_temp, Total_precipitation FROM WeatherAnalysis WHERE Recorded_year = %s LIMIT %s, %s"
        fields = (year, startat, perpage)
    elif sid:
        sql_query = "SELECT Station_ID, Recorded_year, Avg_max_temp, Avg_min_temp, Total_precipitation FROM WeatherAnalysis WHERE Station_ID = %s LIMIT %s, %s"
        fields = (sid, startat, perpage)
    else:
        sql_query = "SELECT Station_ID, Recorded_year, Avg_max_temp, Avg_min_temp, Total_precipitation FROM WeatherAnalysis LIMIT %s, %s"
        fields = (startat, perpage)

    cursor.execute(sql_query, fields)

    records = list(cursor.fetchall())

    cursor.close()

    output = []
    for row in records:
        row_dict = {}
        row_dict['Station_ID'] = row[0]
        row_dict['Recorded_year'] = row[1]
        if row[2]:
            row_dict['Avg_max_temp'] = float(row[2])
        else:
            row_dict['Avg_max_temp'] = None
        if row[3]:
            row_dict['Avg_min_temp'] = float(row[3])
        else:
            row_dict['Avg_min_temp'] = None
        if row[4]:
            row_dict['Total_precipitation'] = float(row[4])
        else:
            row_dict['Total_precipitation'] = None

        output.append(row_dict)

    return output


if __name__ == "__main__":
    app.run(debug=True)
