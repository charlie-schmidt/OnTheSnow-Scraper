from requests_html import HTML, HTMLSession
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
    today_snow = recentSnow8day[7].text.replace('"', '')
    yesterday_snow = recentSnow8day[6].text.replace('"', '')

    ## Getting weather data from other page
    w = s.get('https://www.onthesnow.com/%s/%s/weather' % (region, resortName))
    w.html.render(sleep=2)

    ## General weather forecast
    dailyWeather_list = w.html.find('div.styles_iconWeather__R1V9M')
    today_weather = dailyWeather_list[0].find('span', first=True).text
    tomorrow_weather = dailyWeather_list[1].find('span', first=True).text

    ## Lo/Hi Temp @ Base
    baseTemp_list = w.html.find('td.styles_base__3P0bz')
    today_baseTemp = baseTemp_list[0].text.replace('°', '').replace('F', '').split('/')
    today_baseTempLow = today_baseTemp[0]
    today_baseTempHigh = today_baseTemp[1]
    tomorrow_baseTemp = baseTemp_list[1].text.replace('°', '').replace('F', '').split('/')
    tomorrow_baseTempLow = tomorrow_baseTemp[0]
    tomorrow_baseTempHigh = tomorrow_baseTemp[1]

    ## Lo/Hi Temp @ Summit
    summitTemp_list = w.html.find('td.styles_summit__6zwZl')
    today_summitTemp = summitTemp_list[0].text.replace('°', '').replace('F', '').split('/')
    today_summitTempLow = today_summitTemp[0]
    today_summitTempHigh = today_summitTemp[1]
    tomorrow_summitTemp = summitTemp_list[1].text.replace('°', '').replace('F', '').split('/')
    tomorrow_summitTempLow = tomorrow_summitTemp[0]
    tomorrow_summitTempHigh = tomorrow_summitTemp[1]

    ## Snow Forecasting
    snowForecast_list = w.html.find('td.styles_snow__2D5k7')
    tomorrow_snow = snowForecast_list[1].text.replace('"', '')

    # Write results to SQL Table
    cursor.execute(
    "INSERT INTO dbo.MtnData VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (str(runDate), str(dayString), str(cleanName), float(yesterday_snow), float(today_snow), float(tomorrow_snow), float(today_baseTempLow), float(today_baseTempHigh), float(tomorrow_baseTempLow), float(tomorrow_baseTempHigh), float(today_summitTempLow), float(today_summitTempHigh), float(tomorrow_summitTempLow), float(tomorrow_summitTempHigh), str(today_weather), str(tomorrow_weather))
    )

    conn.commit()


print("Data scrape complete")








