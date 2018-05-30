import getpass
from os import environ as ENV
from functools import wraps
import MySQLdb
from static.tool.Logs import LogType, Log

class Permission:
    '''
    :Nazwa: Permission
    Klasa sworzona dla tego, żebym
    sterować dostępem dla niktórych
    funkcuj, zapotrzebujących lącz-
    enia do Bazy danych.
    Posiada dwa decoratora:
     - dataBaseAuthentificate
     - login

    @Serhii Riznychuk
    '''
    @staticmethod
    @Log(LogType.INFO, 103, "Login to the system", printToConsole=True)
    def login(f):
        """
        :Nazwa: Login
        funkcja tupu dekoratora dla
        możliwości testownaia logowania do bazy danych
        Nie prowadzi autentyfikacji jężeli Login oraz
        haslo już w zmiennych śriodowiska
        :param f: funkcja przekazywana do śriodka logowania
        :return: function

        @Serhii Rinzychuk
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            if(not Permission._test_authorization()):
                return f(*args, **kwargs) if Permission._db_autoriazation() else Permission._error_exit()
            else:
                return f(*args, **kwargs)
        return decorated

    @staticmethod
    #@Log(LogType.INFO, 105, "Brutforce login", printToConsole=False)
    def dataBaseAuthentificate(func):
        '''
        :Nazwa: dataBaseAuthentificate
        Funkcja-dekorator
        Obowiązkowe logowania lub przelogowania do systemu,
        :param func: funkcja przekazywana do śriodka logowania
        :return: function

        @Serhii Riznychuk
        '''
        @wraps(func)
        def with_logging(*args, **kwargs):
            return func(*args, **kwargs) if Permission._db_autoriazation() else Permission._error_exit()
        return with_logging

    @staticmethod
    def _db_autoriazation() -> bool:
        '''
        Nazwa: _db_autoriazation(privat)
        metoda dla nawiązania polącznia do DB, przez wypelneinia formularza
        :return: True, jeżeli udalo sie nawiązać polączneia

        @Serhii Riznychuk
        '''
        try:
            print("Please login to (DB)system")
            login = input("Login: ")
            passwd = getpass.getpass()
        except KeyboardInterrupt:
            return False
        try:
            db = MySQLdb.connect(ENV["TRASHPANDA_HOST"], login, passwd, "mysql")
            ENV["TRASHPANDA_LOGIN"] = login
            ENV["TRASHPANDA_PASSWD"] = passwd
            db.close()
            del(db)
            return True
        except MySQLdb.MySQLError:
            return False
        finally:
            del(login, passwd)

    @staticmethod
    #@Log(LogType.CRITICAL, 2, "Error: error connection with DataBase", printToConsole=False)
    def _error_exit():
        print("\nBye!")

    @staticmethod
    def _test_authorization():
        '''
        :Nazwa: _test_authorization(privat)
        metoda dla testowania polączenia o podanych śriodowiskowych zmiennych
        :return: T/F
        '''
        try:
            db = MySQLdb.connect(ENV["TRASHPANDA_HOST"], ENV["TRASHPANDA_LOGIN"], ENV["TRASHPANDA_PASSWD"], "mysql")
            db.close()
            del(db)
            return True
        except MySQLdb.MySQLError:
            return False


