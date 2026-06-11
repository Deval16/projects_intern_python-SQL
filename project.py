import requests
import psycopg2
url = "https://finnhub.io/api/v1/quote?symbol=AAPL&token=d8j6urpr01qgth6irkogd8j6urpr01qgth6irkp0"

response = requests.get(url)
data = response.json()

price = data['c'] 
symbol = "AAPL"

print(f"Fetched Price: {price}")

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Shampoo@1234",
    sslmode="disable"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    price FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()

cursor.execute(
    "INSERT INTO stocks (symbol, price) VALUES (%s, %s)",
    (symbol, price)
)

conn.commit()

cursor.execute("SELECT * FROM stocks")

rows = cursor.fetchall()

print("\nStored Data:")
for row in rows:
    print(row)

print(f"\nLatest Price Stored: {price}")

cursor.close()
conn.close()