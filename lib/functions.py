import sqlite3
import random

database = sqlite3.connect('./database/database.sqlite')
cursor = database.cursor()

def select_card_rarity():
    random_number = random.randint(0, 1000)
    if random_number <= 1: #0.1%
        result = '6'
    elif 1 < random_number <= 51: #5%
        result = '5'
    elif 51 < random_number <= 151: #10% 
        result = '4'
    elif 151 < random_number <= 301: #15%
        result = '3'
    elif 301 < random_number <= 501: #20%
        result = '2'
    elif 501 < random_number <= 1000: #49.9%
        result = '1'
    else: result = 'HOW DID WE GET HERE?'
    return(result)

def select_random_card(rarity):
    query1 = f"SELECT code FROM Cards WHERE rarity={rarity};"
    cursor.execute(query1); database.commit();
    cardlist = cursor.fetchall()
    CODE = random.choice(cardlist)
    CODE = CODE[0]
    query2 = f"SELECT game, team, player, issue, image FROM Cards WHERE code='{CODE}';"
    cursor.execute(query2); database.commit();
    GAME, TEAM, PLAYER, ISSUE, IMAGE = cursor.fetchall()[0]
    return(CODE, GAME, TEAM, PLAYER, ISSUE, IMAGE)

def insert_card(code, game, team, player, rarity, issue, userid):
    query1 = f"INSERT INTO UserCards VALUES ('{code}', '{game}', '{team}', '{player}', {rarity}, {issue+1}, {userid})"
    cursor.execute(query1); database.commit();
    query2 = f"UPDATE Cards SET issue=issue+1 WHERE code='{code}'"
    cursor.execute(query2); database.commit()

def select_balance_rarity():
    random_number = random.randint(0, 1000)
    if random_number <= 1: #0.1%
        result = '600'
    elif 1 < random_number <= 51: #5%
        result = '500'
    elif 51 < random_number <= 151: #10% 
        result = '400'
    elif 151 < random_number <= 301: #15%
        result = '300'
    elif 301 < random_number <= 501: #20%
        result = '200'
    elif 501 < random_number <= 1000: #49.9%
        result = '100'
    else: result = 'HOW DID WE GET HERE?'
    return(result)

def add_balance(balance, userid):
    query = f"UPDATE Users SET currency=currency+{balance} WHERE userid={userid}"
    cursor.execute(query); database.commit()