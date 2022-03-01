from requests_html import HTML, HTMLSession
import csv
from datetime import date

resortsList = [

    # Partners
    ('utah', 'alta-ski-area', 'Alta', 'Partner')
    , ('utah', 'snowbird', 'Snowbird', 'Partner')
    , ('utah', 'brighton-resort','Brighton', 'Partner')
    , ('wyoming','jackson-hole','Jackson Hole', 'Partner')
    , ('british-columbia','revelstoke-mountain','Revelstoke', 'Partner')
    , ('colorado', 'arapahoe-basin-ski-area', 'Arapahoe Basin', 'Partner')
    , ('colorado', 'copper-mountain-resort', 'Copper', 'Partner')
    , ('colorado','eldora-mountain-resort','Eldora', 'Partner')
    , ('colorado','aspen-snowmass','Aspen Snowmass', 'Partner')
    , ('montana', 'big-sky-resort', 'Big Sky', 'Partner')
    , ('michigan', 'boyne-highlands', 'Boyne Highlands', 'Partner')
    , ('michigan', 'boyne-mountain-resort', 'Boyne Mountain', 'Partner')
    , ('british-columbia', 'cypress-mountain', 'Cypress Mountain', 'Partner')
    , ('vermont', 'killington-resort', 'Killington', 'Partner')
    , ('alberta', 'lake-louise', 'Lake Louise', 'Partner')
    , ('new-hampshire', 'loon-mountain', 'Loon Mountain', 'Partner')
    , ('oregon', 'mt-bachelor', 'Mt. Bachelor', 'Partner')
    , ('alberta', 'ski-banff-norquay', 'Mt. Norquay', 'Partner')
    , ('british-columbia','red-resort','Red Mountain', 'Partner')
    , ('idaho', 'schweitzer', 'Schweitzer', 'Partner')
    , ('maine','sugarloaf','Sugarloaf', 'Partner')
    , ('washington', 'the-summit-at-snoqualmie', 'Summit at Snoqualmie', 'Partner')
    , ('maine','sunday-river','Sunday River', 'Partner')
    , ('alberta', 'sunshine-village', 'Sunshine Village', 'Partner')
    , ('new-mexico','taos-ski-valley','Taos Ski Valley', 'Partner')
    , ('new-york','windham-mountain','Windham Mountain', 'Partner')
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

## Open/Set Up CSV File
new_file_name = 'C:/Users/cschmidt/OneDrive - Alterra Mountain Company/OnTheSnow Scraper/CSV Data Output/dynamic_mtn_data-partners-%s.csv' % (runDate)
new_file = open(new_file_name, 'w', newline='')
csv_writer = csv.writer(new_file)
headers = ['Run-Date', 'Day of Week','Resort', 'Resort Type', 'New Snow Yesterday', 'New Snow Today', 'New Snow Tomorrow', 'Low Base Temp Today','High Base Temp Today', 'Low Base Temp Tomorrow','High Base Temp Tomorrow' ,'Low Summit Temp Today', 'High Summit Temp Today','Low Summit Temp Tomorrow', 'High Summit Temp Tomorrow','Weather Today', 'Weather Tomorrow']
csv_writer.writerow(headers)


for resort in resortsList:
    # Variables for building URL
    region = resort[0]
    resortName = resort[1]
    cleanName = resort[2]
    resortType = resort[3]

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

    # Write results to CSV
    resortData = [runDate, dayString, cleanName, resortType, yesterday_snow, today_snow, tomorrow_snow, today_baseTempLow, today_baseTempHigh, tomorrow_baseTempLow, tomorrow_baseTempHigh, today_summitTempLow, today_summitTempHigh, tomorrow_summitTempLow, tomorrow_summitTempHigh, today_weather, tomorrow_weather]
    csv_writer.writerow(resortData)


new_file.close()

print("Data scrape complete")








