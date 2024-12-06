import psycopg2 
import pandas as pd 
from sqlalchemy import create_engine 


conn_string = 'postgresql://postgres:mukund@localhost/postgres'
players_url="https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/refs/heads/master/data/2024-25/players_raw.csv"

db = create_engine(conn_string) 
conn = db.connect() 


# our dataframe 
players_df=pd.read_csv(players_url)
players_df=players_df[['id', 'web_name']]


players_df.to_sql('players', con=conn, if_exists='replace', 
		index=False) 
conn = psycopg2.connect(conn_string 
						) 
conn.autocommit = True
cursor = conn.cursor() 

sql1 = '''select * from players LIMIT 10;'''
cursor.execute(sql1) 
for i in cursor.fetchall(): 
	print(i) 

# conn.commit() 
conn.close() 
