import requests
from Excel import excel
from bs4 import BeautifulSoup
from utils import get_vacancy_name, get_urls, get_html, get_description, get_skills, get_salary, get_emp_name


html1 = get_html('https://hh.ru/vacancies/programmist_python?hhtmFromLabel=rainbow_profession&hhtmFrom=main')
soup1 = BeautifulSoup(html1, 'html.parser')
urls = get_urls(soup1)
all_data = []
for page in urls:
    html = get_html(page)
    soup = BeautifulSoup(html, 'html.parser')
    vacancy_name = get_vacancy_name(soup)
    salary = get_salary(soup)
    description = get_description(soup)

    skills = get_skills(soup)
    skills_str = ", ".join(skills)

    emp_name = get_emp_name(soup)
    # print(page)
    # print(vacancy_name,salary,skills,emp_name)
    all_data.append([vacancy_name, salary, description, skills_str, emp_name])

filepath = excel(all_data, "table1")