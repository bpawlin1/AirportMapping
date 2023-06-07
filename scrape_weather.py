import requests
from bs4 import BeautifulSoup
import time

def scrape_metar_data():
    url = "https://www.aviationweather.gov/metar/data"
    
    # Send a GET request to the URL
    response = requests.get(url)
    print(response)
    # Create a BeautifulSoup object from the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    div = soup.find('div', id='awc_main_content_wrap')
    code_elements = div.find_all('code')

    # Iterate over the <code> elements and extract the ones with a value of '0'
    for code in code_elements:
        if code.get_text() == '0':
            print(code.get_text())
            break
