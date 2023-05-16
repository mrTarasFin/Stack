from collections import defaultdict


def read_file(in_file: str) -> list:
    """
    Функция считывает файл и возвращает список платежей
    :param in_file: имя файла
    :return: список платежей
    """
    try:
        checks = []
        file = open(in_file, 'r', encoding="utf-8")
        for line in file:
            checks.append(line.strip('\n'))
        file.close()
        return checks
    except Exception as ex:
        print(f'Error: check correct path file {ex}')


def find_all_pay(list_checks: list) -> list:
    """
    Функция принимает список платежей и находит месяц со всеми платежами,
    согласно условия: минимум в одном месяце все платежи
    :param list_checks: список платежей из файла
    :return: список названий всех платежей
    """
    list_month = [item[item.find('_')+1:item.find('.')] for item in list_checks]
    max_month = max(list_month, key=list_month.count)
    all_pay = [pays[:pays.find('_')] for pays in list_checks if max_month in pays]
    return all_pay


def not_pay(list_pay: list, list_checks: list) -> list:
    """
    Функция проверяет в каких квантах(месяц) не оплачены платежи и формирует список из
    этих платежей
    :param list_pay: список всех возможных платежей
    :param list_checks: список платежей из файла
    :return: список не оплаченных
    """
    all_list_pay = []
    all_month = []
    for item in list_checks:
        all_month.append(item[item.find('_')+1:item.find('.')])
    for el in list_pay:
        for it in set(all_month):
            all_list_pay.append(f'{el}_{it}.pdf') # формируем список для всех месяцев со всеми платежами
    not_list_pay = list(set(all_list_pay).difference(list_checks)) # выборка неоплаченных квитанций
    return not_list_pay


def write_file_report_checks(checks: list):
    """
    Функция записывает в основной файл-отчет список платежей по месяцам
    :param checks: список платежей из файла
    """
    sort_list = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь",
                 "ноябрь", "декабрь"]
    dict_checks = {k: [] for k in sort_list}
    for item in checks:
        month = item[item.find('_')+1:item.find('.')]
        if month in dict_checks.keys():
            dict_checks[month].append(f'{month}/{item}')
    with open('report.txt', "w", encoding="utf-8") as file:
        for rep in dict_checks.values():
            for el in rep:
                file.write(f'{el}\n')


def write_file_report_not(not_pays: list):
    """
    Функция записывает в основной файл отчет по неоплаченным платежам
    :param not_pays: список неоплаченных квитанций
    """
    sort_list = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь",
                 "ноябрь", "декабрь"]
    dict_pay = {k: [] for k in sort_list}
    for item in not_pays:
        month = item[item.find('_') + 1:item.find('.')]
        if month in dict_pay.keys():
            dict_pay[month].append(f'{item[:item.find("_")]}')
    with open('report.txt', "a", encoding="utf-8") as file:
        for key, val in dict_pay.items():
            file.write(f'{key}\n')
            for el in val:
                file.write(f'   {el}\n')


def main():
    list_c = read_file('checks.txt')
    all_pay = find_all_pay(list_c)
    pays = not_pay(all_pay, list_c)
    write_file_report_checks(list_c)
    write_file_report_not(pays)


if __name__ == '__main__':
    main()
