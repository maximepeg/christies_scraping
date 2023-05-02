import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


def urls(begin=2018, end=2022):
    tmp = []
    for year in range(begin, end + 1):
        for month in range(1, 13):
            tmp.append('https://www.christies.com/results?sc_lang=en&month=' + str(month) + '&year=' + str(year))

    return tmp



def get_auction_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def soup_to_data(soup, year=2021):
    auction_sections = soup.find_all("section", {"class": "container-fluid chr-event-tile__container"})

    tmp = []
    for section in auction_sections:
        title = section.find("a", {"class": "chr-event-tile__title"}).text.strip()
        location = section.find("span", {"class": "chr-label-s"}).text.strip()
        month = section.find("span", {"class": "chr-heading-xs-sans"}).text.strip().split(' ')[-1]

        tmp.append([title, location, month, year])
    return tmp

def data_to_df(data):
    df = pd.DataFrame(data, columns=['title', 'location', 'month', 'year'])
    return df



def get_auction_dataframe():
    all_urls = urls()
    data = []
    for url in tqdm(all_urls):
        year = url.split('=')[-1]
        soup = get_auction_data(url)
        data += soup_to_data(soup, year)

    df = data_to_df(data)
    return df
