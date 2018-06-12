from os import environ as ENV
from subprocess import Popen, PIPE
from os import popen
from static.classes.datacontroller.SQLController import SQLCloud

"""
Plik wykorzystywany dla testowania logowania
dla konsoli administracjyjnej

@Serhii Riznychuk
"""
serverpath = ENV['CLOUD_PROJECT_PATH']

def testUser(login, haslo) -> bool:
    SQL = SQLCloud()
    SQL_select = SQL.select("users")
    result = SQL_select(email=login)
    if(len(result)):
        return False
    if(result[0][1]==2 and haslo != "misiePysie"):
        return True
    return False


def adminScript(*args):
    comand = "python3 "+serverpath+"/admin.py "+" ".join([*args])
    output = popen(comand, mode="r",).read()
    return output
