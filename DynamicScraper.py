from requests_html import HTML, HTMLSession
import csv
import os.path
from datetime import date

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

# Get today's date as runDate
runDate = date.today()

## Open/Set Up CSV File
save_path = 'C:/Users/cschmidt/OneDrive - Alterra Mountain Company/OnTheSnow Scraper/CSV Data Output/'
new_file_name = 'dynamic_mtn_data-%s.csv' % (runDate)
completeName = os.path.join(save_path, new_file_name)
new_file = open(completeName, 'w', newline='')
csv_writer = csv.writer(new_file)
headers = ['Run-Date', 'Resort', 'New Snow Yesterday', 'New Snow Today', 'New Snow Tomorrow', 'Base Temp Today', 'Base Temp Tomorrow', 'Summit Temp Today', 'Summit Temp Tomorrow', 'Weather Today', 'Weather Tomorrow']
csv_writer.writerow(headers)


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

    # Write results to CSV
    resortData = [runDate, cleanName, yesterday_snow, today_snow, tomorrow_snow, today_baseTemp, tomorrow_baseTemp, today_summitTemp, tomorrow_summitTemp, today_weather, tomorrow_weather]
    csv_writer.writerow(resortData)

new_file.close()

print("Data scrape complete")








