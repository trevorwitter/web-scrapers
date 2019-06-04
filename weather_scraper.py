import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_weather(year,month,day):
    "Returns hourly weather for selected date"
    date = year+month+day
    url = 'https://www.timeanddate.com/scripts/cityajax.php?n=usa/new-york&mode=historic&hd={0}&month={1}&year={2}'.format(date,month,year)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    weather_df = pd.DataFrame(columns=['Time',
                                       'Temp',
                                       'Condition',
                                       'Wind',
                                       'Humidity',
                                       'Pressure',
                                       'Visibility'])
    data = {}
    for x in list(soup.find_all('tr'))[2:]:
        try:
            data['Time'] = x.find('th').text
            data['Temp'] = float(list(x.find_all('td'))[1].text[:2])
            data['Condition'] = list(x.find_all('td'))[2].text
            data['Wind'] = list(x.find_all('td'))[3].text
            data['Humidity'] = float(list(x.find_all('td'))[5].text[:2])
            data['Pressure'] = float(list(x.find_all('td'))[6].text[:5])
            data['Visibility'] = float(list(x.find_all('td'))[7].text[:2])
            weather_df = weather_df.append(data, ignore_index=True)
        except:
            pass
        
    wdate = weather_df['Time'][0][8:]
    weather_df['Time'][0] = weather_df['Time'][0][:8]
    weather_df['Time'] = weather_df['Time'] + " " + wdate
    weather_df['Time'] = pd.to_datetime(weather_df['Time'])

    return weather_df
