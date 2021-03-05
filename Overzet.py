from pymongo import MongoClient
import psycopg2

import MongoDB
import PGAdmin


def inputproducts(items, connection, cursor, newcolumns):
    '''Deze functie zet meegegeven data in de relationele database op basis van de
    meegegeven nieuwe kolommen'''
    for item in items:
        # deze dictionary houdt bij welke waardes in een rij in de 'Products' tabel gaat staan
        productdict = {}
        skip = False
        for key in item.keys():
            # vergelijkt alle keys met de keys in de meegegeven dictionary om alleen de gevraagde waardes
            # over te zetten
            if key in newcolumns.keys():
                # als 'Products' niet in de waarde zit van de meegegeven dictionary betekent dit dat
                # deze waarde in een andere tabel moet als als foreign key in de 'Products' tabel
                if 'Products' not in newcolumns[key]:
                    table = newcolumns[key].split('(')[0]
                    returnedvalue = key + 'id'
                    selectquery = f'select {returnedvalue} from {table} where {key}=(%s)'
                    if isinstance(item[key], list):
                        # een item in de database heeft als waarde voor de category een lijst en die nemen
                        # wij niet mee
                        print(f'Item dat niet wordt meegenomen:\n{item}')
                        skip = True
                        continue
                    elif item[key] is not None:
                        PGAdmin.insertdata(cursor, f'insert into {newcolumns[key]}'
                                                   f'select (%s) where not exists ({selectquery})',
                                           (item[key], item[key]))
                        column = PGAdmin.getdata(cursor, selectquery, (item[key],))[0]
                    else:
                        column = None
                    productdict[newcolumns[key].replace('(', '').replace(')', '')+'id'] = column
                else:
                    if key == 'price':
                        # de kolom 'price' is de enige kolom van de kolommen die we gebruiken
                        # die als waarde een dictionary heeft
                        productdict[key] = item[key]['selling_price']
                    else:
                        if isinstance(item[key], bool):
                            # zet een boolean om naar een bit type voor de relationele database
                            value = f'B{int(item[key])}'
                        else:
                            value = item[key]
                        productdict[newcolumns[key].split('(')[1].replace(')', '')] = value
        if skip:
            continue
        connection.commit()
        columns, values = list(productdict.keys()), list(productdict.values())
        inputcolumns = ','.join(columns)
        inputvalues = ','.join(['%s']*len(values))
        insertquery = 'insert into Products({}) values ({})'.format(inputcolumns, inputvalues)
        PGAdmin.insertdata(cursor, insertquery, values)
        connection.commit()


def inputsessions(sessions, connection, cursor, newcolumns):
    for session in sessions[:100]:
        sessiondict = {}
        for key in session.keys():
            if key in newcolumns.keys():
                if key == 'buid':
                    sessiondict['sessionid'] = session[key][0]
                else:
                    if type(session[key]) == type(True):
                        value = f'B{int(session[key])}'
                    else:
                        value = session[key]
                    sessiondict[newcolumns[key]] = value
        connection.commit()
        columns, values = list(sessiondict.keys()), list(sessiondict.values())
        inputcolumns = ','.join(columns)
        inputvalues = ','.join(['%s'] * len(values))
        insertquery = 'insert into Sessions({}) values ({})'.format(inputcolumns, inputvalues)
        cursor.execute(insertquery, values)
        connection.commit()


def inputprofiles(profiles, connection, cursor, newcolumns):
    for profile in profiles:
        profiledict = {}
        updatedict = {}
        for key in profile.keys():
            if key in newcolumns.keys():
                value = str(profile[key])
                profiledict[newcolumns[key]] = value
            else:
                if key == 'buids':
                    updatedict[value] = (profile[key])
        connection.commit()
        columns, values = list(profiledict.keys()), list(profiledict.values())
        inputcolumns = ','.join(columns)
        inputvalues = ','.join(['%s'] * len(values))
        insertquery = 'insert into Profiles({}) values ({})'.format(inputcolumns, inputvalues)
        cursor.execute(insertquery, values)
        for key, value in updatedict.items():
            if len(value) == 1:
                updatequery = "update sessions SET profilesprofileid = '{}' WHERE sessionid LIKE '{}'".format(key, str(value[0]))
                cursor.execute(updatequery)
            elif len(value) > 1:
                updatequery = "update sessions SET profilesprofileid = '{}' WHERE sessionid IN {}".format(key, tuple(value))
                cursor.execute(updatequery)
        connection.commit()


oldtonewproducts = {'_id': 'Products(productid)', 'brand': 'Brands(brand)', 'category': 'Categories(category)',
                    'description': 'Products(description)', 'herhaalaankopen': 'Products(herhaalaankopen)',
                    'gender': 'Genders(gender)', 'recommendable': 'Products(recommendable)',
                    'name': 'Products(name)', 'price': 'Products(price)',
                    'sub_category': 'Sub_categories(sub_category)',
                    'sub_sub_category': 'Sub_sub_categories(sub_sub_category)'}

oldtonewsessions = {'buid': 'sessionid', 'profilesprofileid': '', 'session_start': 'sessionstart',
                    'session_end': 'sessionend', 'has_sale': 'has_sale'}

oldtonewprofiles = {'_id': 'profileid'}

client = MongoClient()
db = client.huwebshop
collection = db.products
items = MongoDB.getitems(collection)
sessioninfo = db.sessions
sessions = MongoDB.getitems(sessioninfo)
profileinfo = db.profiles
profiles = MongoDB.getitems(profileinfo)


connection = PGAdmin.makeconnection('localhost', 'Recommendation', 'postgres', 'broodje123')
cursor = PGAdmin.makecursor(connection)
inputproducts(items, connection, cursor, oldtonewproducts)
# inputsessions(sessions, connection, cursor, oldtonewsessions)
# inputprofiles(profiles, connection, cursor, oldtonewprofiles)
PGAdmin.closeconnection(connection, cursor)

#items die bijvoorbeeld geen naam of prijs hebben niet in de nieuwe database zetten