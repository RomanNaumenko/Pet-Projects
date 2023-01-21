from modules import *
import sys

SYSTEM_DATA = data_csv_read('SYSTEM_DATA.csv')  # Reading data from a file and writing it to a dictionary for further work.

actions_list = ['COURSE', 'EXCHANGE', 'STOP', 'TIPS']  # List of available actions for the user.

print('***** Welcome to "USD-UAH EXCHANGER" program. *****')
print()

while True:

    possible_actions(actions_list)  # Display available actions for the user on the screen.
    print()

    user_choice = str(input("INPUT THE REQUIRED ACTIVITY: ").upper())
    user_action = user_choice.split(' ')  # Split the user input string into a list by space to recognize the input.

    if user_action[0] == 'COURSE':
        print(course(SYSTEM_DATA, user_action))  # Displaying the exchange rate on the screen.

    elif user_action[0] == 'EXCHANGE':
        if user_action[1] in SYSTEM_DATA.keys():
            # Checking for currency input in the required format and its correctness.
            ex_to = user_action[1]
            transfer_amount = float(user_action[2])
            if ex_to == 'UAH':
                ex_from = 'USD'
            else:
                ex_from = 'UAH'
            print(exchange(transfer_amount, ex_from, ex_to, SYSTEM_DATA)) # Display the result of the currency exchange.
            data_csv_write(SYSTEM_DATA, 'SYSTEM_DATA.csv')  # Rewrite data to file.
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


