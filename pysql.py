import pymysql
from config import dbkey
con = pymysql.connect(host='localhost',user='root',password=dbkey,db='userdata',charset='utf8')
cur=con.cursor()
sql='select userpoint from t_user where userid=2'
cur.execute(sql)
emps=cur.fetchall()
if not(emps):
    print('emps')
