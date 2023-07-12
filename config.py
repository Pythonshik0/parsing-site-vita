mqhost = '92.53.97.5'
mqlogin = 'artbot'
mqpassword = 'G1wDRx21TRygF15L'

DB_USER = 'pharmparser'
DB_PASSWORD = 'nn)TuwAWGW*'
DB_HOST = '92.53.97.5'
DB_NAME = 'pharmsraperdb'

R_HOST = "188.225.27.147"
R_PASSWORD = "bdcff9334960d8b090af975c204236e29a736722e199610085b9a81c5c30685a"

# info = [r['id'], r['site'], r['task_id'], r['main']['region'], r['main']['city']]
# for i in info[3]:
#     print(i)
# print(info)
# pgcon = await asyncpg.connect(host=DB_HOST, user=DB_USER, database=DB_NAME,
#                               password=DB_PASSWORD)
#
# command = f'''INSERT INTO products (
#                                     pharm,
#                                     region,
#                                     city,
#                                     product_name,
#                                     pharm_address,
#                                     product_price,
#                                     product_count,
#                                     product_use_befory,
#                                     task_id) VALUES(
#                                     '{product_row['site']}',
#                                     '{product_row['region']}',
#                                     '{product_row['city']}',
#                                     E'{product_row['name']}',
#                                     '{product_row['apteka']}',
#                                     '{product_row['price']}',
#                                     '{product_row['count']}',
#                                     '{product_row['dataGodn']}',
#                                     '{product_row['task_id']}'
#                                     );'''
#
# await pgcon.execute(command)
#
#
# await pgcon.close()