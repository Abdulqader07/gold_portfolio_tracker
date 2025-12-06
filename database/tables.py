import sqlite3

def fn_createDataBaseTables():
	connection = sqlite3.connect('database.db')
	connection.execute("PRAGMA foreign_keys = ON;")

	cursor = connection.cursor()

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS historicalData(
			dateXAU DATE PRIMARY KEY NOT NULL,
			priceXAU FLOAT NOT NULL
		);''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS baseInvestment(
			investment_id INTEGER PRIMARY KEY AUTOINCREMENT,

			karat INT NOT NULL CHECK (karat IN (10, 12, 14, 18, 21, 24)),
			unit VARCHAR(8) NOT NULL CHECK (unit IN ('kg', 'grams', 'ounces')),

			weight FLOAT NOT NULL,
			currency VARCHAR(8) DEFAULT 'USD' CHECK (currency IN ('USD', 'SYP')),

			purchase_date DATE NOT NULL,
			purchase_price FLOAT NOT NULL,
			model_name TEXT,
			
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
			);''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS holdInvestment(
			investment_id INTEGER NOT NULL,
			hold_id INTEGER PRIMARY KEY AUTOINCREMENT,
			added_to_portfolio DATE DEFAULT (date('now')),

			FOREIGN KEY (investment_id) REFERENCES baseInvestment(investment_id)
			);''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS soldInvestment(
			investment_id INT NOT NULL,
			sold_id INTEGER PRIMARY KEY AUTOINCREMENT,
			sold_price FLOAT NOT NULL,
			sold_at DATE NOT NULL,
			notes TEXT,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			
			FOREIGN KEY (investment_id) REFERENCES baseInvestment(investment_id)
			);''')

	connection.commit()
	cursor.close()

	return 'DataBase Tables Are Created.'