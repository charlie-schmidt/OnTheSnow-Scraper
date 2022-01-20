from requests_html import HTML, HTMLSession
import csv
from datetime import date
import pyodbc

resortsList = [

    # AMC Resorts
('colorado', 'steamboat', 'Steamboat')
, ('colorado','winter-park-resort','Winter Park')
, ('utah','deer-valley-resort', 'Deer Valley')
, ('utah', 'solitude-mountain-resort','Solitude')
, ('montana','whitefish-mountain-resort','Whitefish')
, ('california','squaw-valley-usa','Palisades Tahoe')
, ('california','mammoth-mountain-ski-area','Mammoth')
, ('california','bear-mountain','Bear Mountain')
, ('california','snow-summit','Snow Summit')
, ('pennsylvania','blue-mountain-ski-area','Blue Mountain')
, ('washington','crystal-mountain-wa', 'Crystal')
, ('west-virginia','snowshoe-mountain-resort', 'Snowshoe')
, ('california','june-mountain', 'June')
, ('vermont','sugarbush','Sugarbush')
, ('quebec','tremblant','Tremblant')
]

# Get today's date + day of week
runDate = date.today()
dayOfWeek = runDate.weekday()
if dayOfWeek == 0: dayString = "Monday"
elif dayOfWeek == 1: dayString = "Tuesday"
elif dayOfWeek == 2: dayString = "Wednesday"
elif dayOfWeek == 3: dayString = "Thursday"
elif dayOfWeek == 4: dayString = "Friday"
elif dayOfWeek == 5: dayString = "Saturday"
elif dayOfWeek == 6: dayString = "Sunday"
else: dayString = "Null"

## Open/Set Up SQL Connection
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=charlietest-server.database.windows.net;'
                      'Database=charlietest-db;'
                      'UID=cschmidt;'
                      'PWD=7377GodLovesUgly$;')

cursor = conn.cursor()


for resort in resortsList:
    # Variables for building URL
    region = resort[0]
    resortName = resort[1]
    cleanName = resort[2]

    # Start session + render JS
    s = HTMLSession()
    r = s.get('https://www.onthesnow.com/%s/%s/skireport' % (region,resortName))
    r.html.render(sleep=2)           # Sleep delays the rendering to let the page load before scraping

    # Recent snowfall data
    recentSnow8day_list = r.html.find('table.styles_snowList__2rEYV', first=True)
    recentSnow8day = recentSnow8day_list.find('td')
    today_snow = recentSnow8day[7].text
    yesterday_snow = recentSnow8day[6].text

    ## Getting weather data from other page
    w = s.get('https://www.onthesnow.com/%s/%s/weather' % (region, resortName))
    w.html.render(sleep=2)

    ## General weather forecast
    dailyWeather_list = w.html.find('div.styles_iconWeather__R1V9M')
    today_weather = dailyWeather_list[0].find('span', first=True).text
    tomorrow_weather = dailyWeather_list[1].find('span', first=True).text

    ## Lo/Hi Temp @ Base
    baseTemp_list = w.html.find('td.styles_base__3P0bz')
    today_baseTemp = baseTemp_list[0].text
    tomorrow_baseTemp = baseTemp_list[1].text

    ## Lo/Hi Temp @ Summit
    summitTemp_list = w.html.find('td.styles_summit__6zwZl')
    today_summitTemp = summitTemp_list[0].text
    tomorrow_summitTemp = summitTemp_list[1].text
    
    ## Snow Forecasting
    snowForecast_list = w.html.find('td.styles_snow__2D5k7')
    tomorrow_snow = snowForecast_list[1].text

    # Write results to SQL Table
    cursor.execute(
        "INSERT INTO dbo.MtnData VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (runDate, dayString, cleanName, yesterday_snow, today_snow, tomorrow_snow, today_baseTemp, tomorrow_baseTemp, today_summitTemp, tomorrow_summitTemp, today_weather, tomorrow_weather)
    )



print("Data scrape complete")








