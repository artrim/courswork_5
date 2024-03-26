from src.utils import get_hh_data, create_database, save_data_to_database
from src.db_manager import DBManager
from config import config

params = config()

db_name = input("Введите название базы данных:\n")
create_database(db_name, params)

user_input_employers = input("Введите название компаний через запятую, для просмотра\n").split(',')
data = get_hh_data(user_input_employers)
save_data_to_database(data, db_name, params)

print("Список компаний сохранен в базе данных\n")

db_manager = DBManager(db_name)
while True:
    print("Выберите число от 1 до 5:\n"
          "1. Получить список всех компаний и количество вакансий у каждой компании,\n"
          "2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки "
          "на вакансию,\n"
          "3. Получить среднюю зарплату по вакансиям,\n"
          "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям,\n"
          "5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова, "
          "например python\n"
          "Или введите 'exit' для выхода")

    number_user = input().strip()
    if number_user == 'exit':
        print("Всего хорошего!")
        break
    elif number_user == '1':
        for i in db_manager.get_companies_and_vacancies_count():
            print(f"Название компании - {i[0]}\nКоличество вакансии - {i[1]}\n")
    elif number_user == '2':
        for i in db_manager.get_all_vacancies():
            print(f"Компания - {i[0]}\nВакансия - {i[1]}\nМинимальная заработная плата - {i[2]}\nСсылка - {i[3]}\n")
    elif number_user == '3':
        for i in db_manager.get_avg_salary():
            print(f"Вакансия - {i[0]}\nСредняя зарплата - {i[1]}\n")
    elif number_user == '4':
        for i in db_manager.get_vacancies_with_higher_salary():
            print(f"Вакансия - {i[2]}\nГород - {i[3]}\nЗарплата - {i[4]}\nURL - {i[5]}\n")
    elif number_user == '5':
        word_user = input("Введите ключевое слово для поиска вакансий: \n")
        for i in db_manager.get_vacancies_with_keyword(word_user):
            print(f"Вакансия - {i[2]}\nГород - {i[3]}\nЗарплата - {i[4]}\nURL - {i[5]}\n")
    elif number_user not in ('1', '2', '3', '4', '5'):
        print("Вы ввели неверные данные. \n")
    user_question = input('\nЖелаете продолжить?:\n'
                          '1 - Да;\n'
                          '2 - Нет\n').strip()
    if user_question == '1':
        continue
    elif user_question == '2':
        print("Всего хорошего!")
        break
