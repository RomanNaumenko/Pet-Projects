import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="wiki_data",
    user="postgres",
    password="redeath25101993R"
)
cur = conn.cursor()
cur.execute('SELECT version()')
db_version = cur.fetchone()
print(db_version)
