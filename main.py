from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime


def get_temperature(text):
    temp = text.split('°')[0]
    temp = temp.strip()
    temp = float(temp)
    return round(temp)


def get_temp_from_html():
    response = urlopen('https://www.weerindelft.nl/')
    html = response.read()

    soup = BeautifulSoup(html, features='html.parser')
    ifrm_3 = soup.find(id='ifrm_3')
    ifrm_3_src = ifrm_3['src']

    ifrm_3_response = urlopen(ifrm_3_src)
    ifrm_3_html = ifrm_3_response.read()
    ifrm_3_soup = BeautifulSoup(ifrm_3_html, features='html.parser')
    temperature_span = ifrm_3_soup.find(id='ajaxtemp')
    temperature = get_temperature(temperature_span.text)
    print(f'Temperature from HTML: {temperature}°C')


def get_updated_temp():
    milliseconds = (datetime.now() - datetime(1970, 1, 1)).total_seconds() * 1000
    url = f'https://weerindelft.nl/clientraw.txt?{milliseconds}'
    server_response = urlopen(url)
    data = server_response.read().decode()
    temp = data.split(' ')[4]
    temp = round(float(temp))
    print(f'Temperature from server: {temp}°C')


if __name__ == '__main__':
    get_temp_from_html()
    get_updated_temp()
