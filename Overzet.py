from pymongo import MongoClient
import psycopg2

import MongoDB
import PGAdmin


def inputproducts(items, connection, cursor, newcolumns):
    for item in items[:100]:
        productdict = {}
        for key in item.keys():
            if key in newcolumns.keys():
                if 'Products' not in newcolumns[key]:
                    table = newcolumns[key].split('(')[0]
                    returnedvalue = key + 'id'
                    selectquery = f'select {returnedvalue} from {table} where {key}=(%s)'
                    cursor.execute(f'insert into {newcolumns[key]} select (%s) where not exists ({selectquery})',
                                   (item[key], item[key]))
                    cursor.execute(selectquery, (item[key],))
                    column = cursor.fetchone()[0]
                    productdict[newcolumns[key].replace('(', '').replace(')', '')+'id'] = column
                else:
                    if key == 'price':
                        productdict[key] = item[key]['selling_price']
                    else:
                        if type(item[key]) == type(True):
                            value = f'B{int(item[key])}'
                        else:
                            value = item[key]
                        productdict[newcolumns[key].split('(')[1].replace(')', '')] = value
        connection.commit()
        columns, values = list(productdict.keys()), list(productdict.values())
        inputcolumns = ','.join(columns)
        inputvalues = ','.join(['%s']*len(values))
        insertquery = 'insert into Products({}) values ({})'.format(inputcolumns, inputvalues)
        cursor.execute(insertquery, values)
        connection.commit()



oldtonewproducts = {'_id': 'Products(productid)', 'brand': 'Brands(brand)', 'category': 'Categories(category)',
                    'description': 'Products(description)', 'herhaalaankopen': 'Products(herhaalaankopen)',
                    'gender': 'Genders(gender)',
                    'recommendable': 'Products(recommendable)', 'name': 'Products(name)', 'price': 'Products(price)',
                    'sub_category': 'Sub_categories(sub_category)', 'sub_sub_category': 'Sub_sub_categories(sub_sub_category)'}

client = MongoClient()
db = client.huwebshop
collection = db.products
items = MongoDB.getitems(collection)

connection = PGAdmin.makeconnection('localhost', 'Recommendation', 'postgres', 'broodje123')
cursor = PGAdmin.makecursor(connection)
inputproducts(items, connection, cursor, oldtonewproducts)
PGAdmin.closeconnection(connection, cursor)

#items die bijvoorbeeld geen naam of prijs hebben niet in de nieuwe database zetten