import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
import pandas as pd


host = 'https://spb.hh.ru'
articles = f'{host}/search/vacancy?text=python&area=1&area=2'


def get_headers():
    return Headers(browser="firefox", os="win").generate()


def get_text(url):
    return requests.get(url, headers=get_headers()).text

def find_articles(text_url):
    soup = BeautifulSoup(text_url, features='lxml')
    return soup.find_all('div', class_='serp-item')

def parser(content):
    hh_list = []
    for i in content:
        hh_job_title = i.find('a', class_='serp-item__title')
        hh_salary = ''
        try:
            hh_salary = i.find('span', class_='bloko-header-section-3').text
        except AttributeError:
            hh_salary = None
        if 'Django' in hh_job_title.text and 'Flask' in hh_job_title.text:
            hh_link = hh_job_title.get('href')
            hh_employer_name = i.find('a', class_='bloko-link bloko-link_kind-tertiary')
            hh_city_name = i.find('div', attrs= {'data-qa':'vacancy-serp__vacancy-address', 'class':'bloko-text'})
            hh_list.append({
                'Вакансия': hh_job_title.text,
                'Работадатель': hh_employer_name.text,
                'Город': hh_city_name.text,
                'Зарплата': hh_salary,
                'Ссылка': hh_link
            })
    return hh_list

def dict_transform(dict):
    result = []
    for idx in range(0, len(dict)-1):
        result.append([])
        result[idx].append(str(dict[idx]['Вакансия']))
        result[idx].append(str(dict[idx]['Зарплата']))
        result[idx].append(str(dict[idx]['Ссылка']))
        result[idx].append(str(dict[idx]['Работадатель']))
        result[idx].append(str(dict[idx]['Город']))
    return result

def dataframe(lst):
    df = pd.DataFrame(lst, columns = ['Вакансия', 'Зарплата', 'Ссылка', 'Работадатель', 'Город'])
    filename = 'hh.csv'
    df.to_json(filename)
    return df