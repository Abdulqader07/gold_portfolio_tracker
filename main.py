import sqlite3

print('''
*** XAU(Gold) Personal Tracker ***\n
To Add New Data Press (1).
To Edit An Existing Data Press (2).
To View Your Profits/Losses In Real-Time Press (3).
''')

userChoice = input(': ')

if userChoice == '1':
	print('''
Enter The Following Values:
1) Karat (must be either (10, 12, 14, 18, 21, 24)),
2) Unit (either (ounces, grams, kg)),
3) Weight (pay attention to your input),
4) Currency either ((USD, SYP)),
5) The Date Of The Purchase In The Following Format (YYYY-MM-DD),
6) The Price Of The Purchase
7) The Model Name
''')
	karat = int(input('Karat: '))
	unit = input('Unit: ')
	weight = float(input('Weight: '))
	currency = input('Currency: ')
	dateOfPurchase = input('Date Of Purchase: ')
	priceOfPurchase = float(input('Price Of Purchase: '))
	modelName = input('Model Name: ')


connection = sqlite3.connect('./database/database.db')
cursor = connection.cursor()

cursor.execute('''
	INSERT INTO baseInvestment (karat, unit, weight, currency, purchase_date, purchase_price,
		, model_name) VALUES (?, ?, ?, ?, ?, ?);
	''')