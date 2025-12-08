import sqlite3
import os
from database.tables import fn_createDataBaseTables

print('''
*** XAU(Gold) Personal Tracker ***\n
To Add New Data Enter (1).
To Edit An Existing Data Enter (2).
To View Your Profits/Losses In Real-Time Enter (3).''')

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

	if not os.path.exists('./database/database.db'):
		fn_createDataBaseTables()

	connection = sqlite3.connect('./database/database.db')
	cursor = connection.cursor()

	soldOrHold = input('Do You Have This Investment In Your Portfolio Or You Sold It?[Sold/Hold]: ')

	while True:
		if soldOrHold.is_decimal() or soldOrHold.lower() not in ('sold', 'hold', 's', 'h'):
			soldOrHold = input('Invalid Input Please Make Sure To Either Hit (Sold or Hold): ')
		else:
			break

	cursor.execute('''
		INSERT INTO baseInvestment (karat, unit, weight, currency, purchase_date, purchase_price,
			, model_name) VALUES (?, ?, ?, ?, ?, ?);
		''', (karat, unit, weight, currency, dateOfPurchase, priceOfPurchase, modelName)
		)

	cursor.execute('''SELECT investment_id FROM baseInvestment
		ORDER BY investment_id DESC LIMIT 1;''')

	investmentId = fetchone()

	if soldOrHold.lower() == 'sold' or soldOrHold.lower() == 's':
		print('''
Fill The Following Data:
1) For How Much You Sold it?,
2) What Is The Date Of The Sold? In The Following Format (YYYY-MM-DD),
3) Notes (Not Required)
''')
		soldPrice = float(input('Sold Price: '))
		soldDate =  input('Sold Date: ')
		notes = input('Notes: ')

		if notes.strip() == '':
			cursor.execute('''
			INSERT INTO soldInvestment (investment_id, sold_price, sold_at) VALUES (
				investmentId, soldPrice, sold);
			''')
		else:
			cursor.execute('''
				INSERT INTO soldInvestment (investment_id, sold_price, sold_at, notes) VALUES (
					investmentId, soldPrice, sold, notes);
				''')

	if soldOrHold.lower() == 'hold' or soldOrHold.lower() == 'h':
		cursor.execute('''
			INSERT INTO holdInvestment (investment_id) VALUES (investmentId);''')

	print('Data Added To Your Portfolio.')

elif userChoice == '2':
	print('''
What Type Of Changes You Wanna Make?
Edit An Existing Data Enter (1),
Sold Data? Enter (2),
Delete Data? Enter (3).''')

	userEditOption = input(': ')

	if userEditOption.is_decimal() or userEditOption == '1':
		cursor.execute('''
			SELECT * FROM baseInvestment;
			''')
		allData = cursor.fetchall()

		for data in allData:
			print(data)

		investment_id = input('Based On The Data You Have Enter The investment_id You Update The Data For: ')

		cursor.execute('SELECT COUNT(*) FROM baseInvestment WHERE investment_id = ?;'
			, investment_id)
		validId = cursor.fetchone()

		while validId['COUNT'] == 0:
			print('There Is No investment_id In The Table, Try Again: ')
			cursor.execute('SELECT COUNT(*) FROM baseInvestment WHERE investment_id = ?;'
				, investment_id)
			validId = cursor.fetchone()

		userDataChanges = input('What You Wanna Change: ')
		updatedData = input('Enter The New Data: ')

		cursor.execute('''
			UPDATE baseInvestment SET ? = ? 
				WHERE investment_id = ?;''',
			 userDataChanges, updatedData, validId)

	elif userEditOption == '2':
		cursor.execute('''
			SELECT * FROM baseInvestment;''')
		allData = cursor.fetchall()

		for data in allData:
			print(data)

		soldId = input('Enter The investment_id That You Sold: ')
		cursor.execute('''
			SELECT COUNT(*) FROM baseInvestment WHERE investment_id = ?;''',
			soldId)

		validId = cursor.fetchone()

		while validId['COUNT(*)'] == 0:
			validId = input('There Is No investment_id In The Table, Try Again: ')
			cursor.execute('SELECT COUNT(*) FROM baseInvestment WHERE investment_id = ?;'
				, investment_id)
			validId = cursor.fetchone()

		cursor.execute('SELECT COUNT(*) FROM soldInvestment WHERE investment_id = ?;',
			validId)
		tableSoldId = cursor.fetchone()

		if tableSoldId['COUNT(*)'] > 0:
			print('These Data Already Sold.')
		else:
			soldPrice = input('How Much Did You Sold It For: ')
			soldDate = input ('At What Date You Sold It (YYYY-MM-DD): ')
			
			cursor.execute('''
				INSERT INTO soldInvestment (investment_id, sold_price, sold_at) VALUES
				(?, ?, ?);''', (validId, soldPrice, soldDate))

	elif userEditOption == '3':
		soldOrHold = input('You Wanna Delete Either [Hold/Sold]: ')

		if not soldOrHold.is_decimal() or soldOrHold.lower() in ['h', 'hold']:
			cursor.execute('''
				SELECT * FROM holdInvestment;''')
			allData = cursor.fetchall()

			for data in allData:
				print(data)

			deleteId = input('Enter The investment_id You Wanna Delete: ')
			cursor.execute('SELECT COUNT(*) FROM holdInvestment WHERE investment_id = ?',
				deleteId)

			validId = cursor.fetchone()

			while validId['COUNT(*)'] == 0:
				validId = input('There Is No investment_id In The Table, Try Again: ')
				cursor.execute('SELECT COUNT(*) FROM baseInvestment WHERE investment_id = ?;'
					, investment_id)
				validId = cursor.fetchone()

			cursor.execute('DELETE FROM holdInvestment, baseInvestment WHERE investment_id = ?;',
				validId)

			print('Data Deleted From Hold.')

		elif soldOrHold == not soldOrHold.is_decimal() or soldOrHold.lower() in ['s', 'sold']:
			cursor.execute('''
				SELECT * FROM soldInvestment;''')
			allData = cursor.fetchall()

			for data in allData:
				print(data)

			deleteId = input('Enter The investment_id You Wanna Delete: ')
			cursor.execute('SELECT COUNT(*) FROM soldInvestment WHERE investment_id = ?',
				deleteId)

			validId = cursor.fetchone()

			while validId['COUNT(*)'] == 0:
				validId = input('There Is No investment_id In The Table, Try Again: ')
				cursor.execute('SELECT COUNT(*) FROM baseInvestment WHERE investment_id = ?;'
					, investment_id)
				validId = cursor.fetchone()

			cursor.execute('DELETE FROM soldInvestment, baseInvestment WHERE investment_id = ?;',
				validId)

			print('Data Deleted From Sold.')			

elif userChoice == '3':
	
	# This is a calculations choice Where I do new table to save finance information
	pass

	# This choice relay on math and statistics

else:
	print('Invalid Input Please Try Again: ')

connection.commit()
cursor.close()