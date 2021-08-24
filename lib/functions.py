import sqlite3
import random

database = sqlite3.connect('./database/database.sqlite')
cursor = database.cursor()

def select_card_rarity():
    random_number = random.randint(0, 1000)
    if random_number <= 1:
        result = '6'
    elif 1 < random_number <= 51:
        result = '5'
    elif 51 < random_number <= 151:
        result = '4'
    elif 151 < random_number <= 301:
        result = '3'
    elif 301 < random_number <= 501:
        result = '2'
    elif 501 < random_number <= 1000:
        result = '1'
    else: result = 'HOW DID WE GET HERE?'
    return(result)

def select_random_card(rarity):
    query1 = f"SELECT code FROM Cards WHERE rarity={rarity};"
    cursor.execute(query1); database.commit()
    cardlist = cursor.fetchall()
    code = random.choice(cardlist)
    code = code[0]
    query2 = f"SELECT game, team, player, issue, teamyear, image FROM Cards WHERE code='{code}';"
    cursor.execute(query2); database.commit()
    game, team, player, issue, teamyear, image = cursor.fetchall()[0]
    return(code, game, team, player, issue, teamyear, image)

def insert_card(game, team, player, rarity, issue, teamyear, code, userid, image):
    query1 = f"INSERT INTO UserCards VALUES ('{game}', '{team}', '{player}', {rarity}, {issue+1}, {teamyear}, '{code}', {userid}, '{image}')"
    cursor.execute(query1); database.commit()
    query2 = f"UPDATE Cards SET issue=issue+1 WHERE code='{code}'"
    cursor.execute(query2); database.commit()

def select_balance_rarity():
    random_number = random.randint(0, 1000)
    if random_number <= 1:
        result = '600'
    elif 1 < random_number <= 51:
        result = '500'
    elif 51 < random_number <= 151:
        result = '400'
    elif 151 < random_number <= 301:
        result = '300'
    elif 301 < random_number <= 501:
        result = '200'
    elif 501 < random_number <= 1000:
        result = '100'
    else: result = 'HOW DID WE GET HERE?'
    return(result)

def add_balance(balance, userid):
    query = f"UPDATE Users SET currency=currency+{balance} WHERE userid={userid}"
    cursor.execute(query); database.commit()