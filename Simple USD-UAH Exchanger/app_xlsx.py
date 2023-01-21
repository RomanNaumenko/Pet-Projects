from modules import *
import sys

SYSTEM_DATA = data_xlsx_read('SYSTEM_DATA.xlsx')  # Чтение данных из файла и запись их в словарь для дальнейшей
# работы.

actions_list = ['COURSE', 'EXCHANGE', 'STOP', 'TIPS']  # Список доступных действий для пользователя.

print('***** Welcome to "USD-UAH EXCHANGER" program. *****')
print()

while True:

    possible_actions(actions_list)  # Вывод доступных действий для пользователя на экран.
    print()

    user_choice = str(input("INPUT THE REQUIRED ACTIVITY: ").upper())
    user_action = user_choice.split(' ')  # Разбиение введенной пользователем строки на список по пробелу для
    # распознания введенных данных.

    if user_action[0] == 'COURSE':
        print(course(SYSTEM_DATA, user_action))  # Вывод курса валюты на экран.

    elif user_action[0] == 'EXCHANGE':
        if user_action[1] in SYSTEM_DATA.keys():  # Проверка на ввод валюты в нужном формате и его правильность.
            ex_to = user_action[1]
            transfer_amount = float(user_action[2])
            if ex_to == 'UAH':
                ex_from = 'USD'
            else:
                ex_from = 'UAH'
            print(exchange(transfer_amount, ex_from, ex_to, SYSTEM_DATA))  # Вывод результата обмена валют.
            data_xlsx_write(SYSTEM_DATA, 'SYSTEM_DATA.xlsx')  # Перезапись данных в файл.
        else:
            print('The currency name is incorrect!')

    elif user_action[0] == 'STOP':
        print("SERVICE STOPPED")
        sys.exit()

    elif user_action[0] == 'TIPS':
        print(
            'You can input the required activity in the the next format if you want you get the correct result: ')
        print('1. If you want to see the course of the currency, please, input the following: COURSE currency_name')
        print('2. If you want to exchange the currency, please, input the following: EXCHANGE currency_name amount')
        print('3. If you want to stop the service, please, input the following: STOP')
        print('4. If you want to see the tips, please, input the following: TIPS (But you probably knew it already)')

    else:
        print('Unknown action! Please check your input or use "TIPS" action.')
    print()






