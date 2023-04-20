import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="links_db",
    user="postgres",
    password="redeath25101993R"
)
cur = conn.cursor()
# cur.execute('SELECT version()')
# db_version = cur.fetchone()
# print(db_version)
# cur.execute("DROP TABLE paths")
cur.execute("CREATE TABLE paths (id SERIAL PRIMARY KEY, start_point varchar, finish_point varchar, path varchar[])")
cur.execute("INSERT INTO paths (start_point,finish_point,path) "
            "VALUES('Дружба', 'Рим', '{\"Дружба\"	, \"Якопо Понтормо\", \"Рим\"}')")
cur.execute("SELECT * FROM paths")

db_version = cur.fetchone()
print(db_version)
conn.commit()
cur.close()
conn.close()
