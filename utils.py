from pydoc import classify_class_attrs
import re
import requests
from bs4 import BeautifulSoup


def get_html(url:str) -> str:
    headers = {
        'User-Agent':'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.raise_for_status()
        return response.text
    else:
        print("Ошибка запроса")
        return ""


def get_urls(soup: BeautifulSoup) -> list[str]:
    urls = []
    # url_addresses = soup.find_all('a', attrs= {"data-qa": "serp-item__title"})
    url_addresses = soup.find_all("a",
                                  class_="magritte-link___b4rEM_7-1-0 magritte-link_mode_primary___l6una_7-1-0 magritte-link_style_neutral___iqoW0_7-1-0 magritte-link_enable-visited___Biyib_7-1-0")
    for url in url_addresses:
        urls.append(url['href'])

    return urls


def get_vacancy_name(soup: BeautifulSoup) -> str:
    vacancy_name = soup.find(attrs = {"data-qa": "vacancy-title"})

    return vacancy_name.text

def get_emp_name(soup: BeautifulSoup) -> str:
    emp_name = soup.find(attrs = {"data-qa": "vacancy-company-name"})

    return emp_name.text

def get_salary(soup: BeautifulSoup) -> str:
    """Парсинг зарплаты специально для HH.ru"""
    try:
        # Для HH.ru часто используется такой data-атрибут
        salary_elem = soup.find(attrs={'data-qa': 'vacancy-salary'})

        if not salary_elem:
            # Альтернативный селектор для HH.ru
            salary_elem = soup.select_one('[data-qa="vacancy-salary-compensation-type-net"]')

        if not salary_elem:
            # Ищем по классам, содержащим "compensation"
            salary_elem = soup.find(class_=lambda x: x and 'compensation' in str(x).lower())

        if salary_elem:
            # Очищаем текст от лишних пробелов
            return ' '.join(salary_elem.text.split())

        return "Зарплата не указана"

    except Exception as e:
        return f"Ошибка: {e}"


def get_description(soup: BeautifulSoup) -> str:
    description = soup.find("div", attrs={"data-qa": "vacancy-description"})
    description_text = description.text
    description_parts = description_text.split("Требования")
    final_description = description_parts[0]
    return final_description

def get_skills(soup: BeautifulSoup) -> list[str]:
    all_skills = soup.find_all(attrs={"data-qa": "skills-element"})
    skills = []
    for skill in all_skills:
        skills.append(skill.text)

    # all_skills = []
    # for i in range(2):
    #     skill = soup.find("div", class_ = "magritte-tag__label___YHV-o_5-1-0").text
    #     all_skills.append(skill)
    return skills

attrs = {"data-qa": "vacancy-title"}
class_ = "magritte-text___pbpft_4-4-4 magritte-text_max-lines___iNa8I_4-4-4 magritte-text_style-primary___AQ7MW_4-4-4 magritte-text_typography-display-7-display___GcMI1_4-4-4"