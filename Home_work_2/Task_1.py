import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

client = MongoClient('127.0.0.1', 27017)
db = client['db_hh_parsing']
hh_vacansys = db.hh_vacansys
#         params = {'area': '1',
#                   'fromSearchLine': 'true',
#                   'st': 'searchVacancy',
#                   'text': vacancy,
#                   'page': page}
vacancy_input = input('Insert_vacansy: ')
vacancys = []
url = 'https://hh.ru/'
page = 0
escape = False
while url:
    page_next = None
    response = None
    soup = None
    params = {'area': '1',
              'st': 'searchVacancy',
              'text': vacancy_input,
              'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.607 Yowser/2.5 Safari/537.36'}
    response = requests.get(url + 'search/vacancy?', headers=headers, params=params)
    pprint(page_next)
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.find_all('div', attrs='vacancy-serp-item')
    page_next = soup.find('a', attrs={'class': 'bloko-button', 'data-qa': 'pager-next'})
    pprint(page_next)
    page_current = soup.find('span', attrs={'class': 'bloko-button bloko-button_pressed', 'data-qa': 'pager-page'})
    for vacancy in vacancy_list:
        max_vacancy_salary = ''
        vacancy_data = {}
        vacancy_info = vacancy.find('a', attrs={'class': 'bloko-link', 'data-qa': 'vacancy-serp__vacancy-title'})
        if vacancy_info is not None:
            vacancy_name = vacancy_info.text
            vacancy_herf = vacancy_info.get('href')
        id = ''.join(re.findall(r'\d{8}', vacancy_herf))
        vacancy_info_copmany = vacancy.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
        if vacancy_info_copmany is not None:
            vacancy_company = vacancy_info_copmany.text
            vacancy_company = vacancy_company.replace(u'\xa0', u'')
            if vacancy_company == 'Meta Sistem':
                vacancy_company = None
        vacancy_info_salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy_info_salary is not None:
            vacancy_salary = vacancy_info_salary.getText().replace(u'\xa0', u'')
            vacancy_salary = re.split('\s|<|>', vacancy_salary)
            max_vacancy_salary = ''
            min_vacancy_salary = ''
            general_salary = ''
            if vacancy_salary[0] == 'до':
                for elements in range(1, len(vacancy_salary) - 1):
                    max_vacancy_salary = max_vacancy_salary + ''.join(vacancy_salary[elements])
                max_vacancy_salary = int(max_vacancy_salary)
                min_vacancy_salary = None
            elif vacancy_salary[0] == 'от':
                for elements in range(1, len(vacancy_salary) - 1):
                    min_vacancy_salary = min_vacancy_salary + ''.join(vacancy_salary[elements])
                min_vacancy_salary = int(min_vacancy_salary)
                max_vacancy_salary = None
            elif vacancy_salary[0] == 'по':
                min_vacancy_salary = None
                max_vacancy_salary = None
            else:
                for elements in range(len(vacancy_salary) - 1):
                    general_salary = general_salary + ''.join(vacancy_salary[elements])
                general_salary = re.split(r'–', general_salary)
                min_vacancy_salary = int(general_salary[0])
                max_vacancy_salary = int(general_salary[1])
        vacancy_data['_id'] = id
        vacancy_data['Vacancy_name'] = vacancy_name
        vacancy_data['Vacancy_company'] = vacancy_company
        vacancy_data['Vacansy_salary_max'] = max_vacancy_salary
        vacancy_data['Vacansy_salary_min'] = min_vacancy_salary
        try:
            hh_vacansys.insert_one (vacancy_data)
        except dke:
            pprint('Document already exist')
    page += 1
    pprint(f'Search page: {page}')
    if page_next is None:
        break

check_search = input('Search? y/n')
if check_search == 'y':
    insert_salary = int(input('Insert min salary:'))
    for doc in hh_vacansys.find(
            {'$or': [{'Vacansy_salary_max': {'$gt': insert_salary}}, {'min_vacancy_salary': {'$gt': insert_salary}}]}):
        pprint(doc)

#