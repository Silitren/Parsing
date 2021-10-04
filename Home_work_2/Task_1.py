import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
import re

# def parsing_vacancy (vacancy: str):
#     ip = 0
#     vacancys = []
#     url = 'https://hh.ru/'
#     page = -1
#     while url:
#         page += 1
#         params = {'area': '1',
#                   'fromSearchLine': 'true',
#                   'st': 'searchVacancy',
#                   'text': vacancy,
#                   'page': page}
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.607 Yowser/2.5 Safari/537.36'}
#         response = requests.get(url + 'search/vacancy', headers=headers, params=params)
#         print(response)
#         soup = bs(response.text, 'html.parser')
#         vacancy_list = soup.find_all('div', attrs='vacancy-serp-item')
#         page_next = soup.find_all('a', attrs={'class': 'bloko-button', 'data-qa': 'pager-next'})
#         print(page)
#         for vacancy in vacancy_list:
#             max_vacancy_salary = ''
#             vacancy_data = {}
#             vacancy_info = vacancy.find('a', attrs={'class': 'bloko-link', 'data-qa': 'vacancy-serp__vacancy-title'})
#             if vacancy_info is not None:
#                 vacancy_name = vacancy_info.text
#             vacancy_info_copmany = vacancy.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
#             if vacancy_info_copmany is not None:
#                 vacancy_company = vacancy_info_copmany.text
#                 vacancy_company = vacancy_company.replace(u'\xa0', u'')
#                 if vacancy_company == 'Meta Sistem':
#                     vacancy_company = None
#             vacancy_info_salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
#             if vacancy_info_salary is not None:
#                 vacancy_salary = vacancy_info_salary.getText().replace(u'\xa0', u'')
#                 vacancy_salary = re.split('\s|<|>', vacancy_salary)
#                 max_vacancy_salary = ''
#                 min_vacancy_salary = ''
#                 general_salary = ''
#                 if vacancy_salary[0] == 'до':
#                     for elements in range(1, len(vacancy_salary) - 1):
#                         max_vacancy_salary = max_vacancy_salary + ''.join(vacancy_salary[elements])
#                     max_vacancy_salary = int(max_vacancy_salary)
#                     min_vacancy_salary = None
#                 elif vacancy_salary[0] == 'от':
#                     for elements in range(1, len(vacancy_salary) - 1):
#                         min_vacancy_salary = min_vacancy_salary + ''.join(vacancy_salary[elements])
#                     min_vacancy_salary = int(min_vacancy_salary)
#                     max_vacancy_salary = None
#                 elif vacancy_salary[0] == 'по':
#                     min_vacancy_salary = None
#                     max_vacancy_salary = None
#                 else:
#                     for elements in range(len(vacancy_salary) - 1):
#                         general_salary = general_salary + ''.join(vacancy_salary[elements])
#                     general_salary = re.split(r'–', general_salary)
#                     min_vacancy_salary = int(general_salary[0])
#                     max_vacancy_salary = int(general_salary[1])
#             vacancy_data['Vacancy_name'] = vacancy_name
#             vacancy_data['Vacancy_company'] = vacancy_company
#             vacancy_data['Vacansy_salary_max'] = max_vacancy_salary
#             vacancy_data['Vacansy_salary_min'] = min_vacancy_salary
#             vacancys.append(vacancy_data)
#             pprint(vacancys)
#             print('___________________________________', params)
#
#
#         # except IndexError:
#         #     with open('data.txt', 'w') as f:
#         #         json.dump(vacancys, f)
#         #     break
#     #     if soup.find_all('a', attrs={'class': 'bloko-button', 'data-qa': 'pager-next'}) is not None:
#     #         page += 1
#     #     else:
#     #         break

vacancy_input = input('Insert_vacansy: ')
ip = 0
vacancys = []
url = 'https://hh.ru/'
page = 0
while url:
    params = {'area': '1',
                'fromSearchLine': 'true',
                'st': 'searchVacancy',
                'text': vacancy_input,
                'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.607 Yowser/2.5 Safari/537.36'}
    response = requests.get(url + 'search/vacancy', headers=headers, params=params)
    # print(response)
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.find_all('div', attrs='vacancy-serp-item')
    page_next = soup.find('a', attrs={'class': 'bloko-button', 'data-qa': 'pager-next'})
    # print(page)
    for vacancy in vacancy_list:
        max_vacancy_salary = ''
        vacancy_data = {}
        vacancy_info = vacancy.find('a', attrs={'class': 'bloko-link', 'data-qa': 'vacancy-serp__vacancy-title'})
        if vacancy_info is not None:
            vacancy_name = vacancy_info.text
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
        vacancy_data['Vacancy_name'] = vacancy_name
        vacancy_data['Vacancy_company'] = vacancy_company
        vacancy_data['Vacansy_salary_max'] = max_vacancy_salary
        vacancy_data['Vacansy_salary_min'] = min_vacancy_salary
        vacancys.append(vacancy_data)
        # pprint(vacancys)
    # print('___________________________________', params)
    if page <= 40:
        # print(page_next)
        # print(page_next_test)
        print('Page = ', page)
        page += 1
    else:
        print(len(vacancys))
        with open('data.json', 'w') as f:
            json.dump(vacancys, f)
        break

# parsing_vacancy(str(input('Insert vacany: ')))
