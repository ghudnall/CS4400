import pymysql

global connection
connection = pymysql.connect(host= 'localhost',
                             user='root',
                             password= 'blackdog',
                             db= 'store',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
global cursor
cursor = connection.cursor()

query = 'select username, zip from buyer where state = "Georgia";'
cursor.execute(query)
print(cursor.fetchall())