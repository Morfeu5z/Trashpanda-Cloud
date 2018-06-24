import datetime
import hashlib
import os

from static.tool.FileManager import FileManager
from static.classes.datacontroller.SQLController import SQLCloud

"""
Klasa tymczasowa, przechowuje dane o pliku, ktory zostal wlasnie wrzucony na serwer.
Sluzy do szybkiej i porecznej aktualizacji bazy danych

Autor: Rychel Mikołaj
"""

class Uploaded_File():
    def __init__(self):
        self.ID_file = ""
        self.ID_File = ""
        self.Version = "1.0"
        self.Name = ""
        self.HashSum = ""
        self.Size = ""
        self.extension = ""
        self.path = ""
        self.accessType = "1"
        self.garbage = "0"
        self.timeCreate = str(datetime.datetime.today())
        self.lastAccess = str(datetime.datetime.today())
        self.OwnerID = ""
        self.Description = ""

    def getInfo(self,filename: str, file_dir: str, destination_DIR: str, google_ID: str, description: str):
        self.HashSum = str(FileUpload.countHashSum(file_dir))
        self.Size = str(os.stat(file_dir).st_size)
        self.extension = FileManager.extensionSpliter(file_dir)
        self.Name = filename
        self.path = destination_DIR + self.HashSum + self.extension
        self.OwnerID = str(google_ID)
        self.Description = description

"""
Uploads the shit

Autor: Rychel Mikołaj
"""  
    def uploadTheShit(self):
        try:
            """Inicjalizacja SQL controller'a"""
            DB = SQLCloud()

            """Wyszukanie uzytkownika po google id"""
            SQL_Select = DB.select("users")
            user_data = SQL_Select(google_id = self.OwnerID)

            """Przypisanie bazodanowego user ID, podany do konstruktora ID jest tylko ID google'a"""
            ID = user_data[0][0]

            """Upload informacji o pliku do bazy"""
            SQL_Insert = DB.insert("file")
            SQL_Select = DB.select("file")

            SQL_Insert(ID, self.Name)
            file_data = SQL_Select(idUser=ID, description= self.Name)

            """Pobranie ID pliku"""
            File_ID = file_data[0][0]

            SQL_Insert = DB.insert("version")
            SQL_Insert(file_data[0][0], self.Version, self.HashSum, self.Size, self.extension, self.path, self.accessType, self.garbage, self.timeCreate, self.lastAccess)

            SQL_Insert = DB.insert("info")
            SQL_Insert(str(File_ID), ID,  self.Description, "Nie wiem co to jest")

            print("Dodano")
            return True
        except Exception as m :
            print(m)
            print("Blad")
            raise ValueError()
            
            
class FileUpload():
"""
Przygotowuje listę plików do upload'u, wykonuje sprawdzenie zgodnosci z polityka aplikacji.
Autor: Rychel Mikołaj
"""
    @staticmethod
    def upload(REQUESTED_FILE, path, google_ID, Description):
        DUMP_DIR = "/srv/DUMP/"
        Destination_DIR = "/srv/Data" + path

        """Lista mówiąca ile plików udało się pobrać bez problemów"""
        statusList = list()

        try:
            """Magia Uploadu pliku, Cała logika znajduje się tutaj"""
            filename = REQUESTED_FILE.filename
            DUMP_destination = DUMP_DIR + filename
            """Grand Finale - Zapis Pliku na dysku"""

            REQUESTED_FILE.save(DUMP_destination)

            SHA1 = FileUpload.countHashSum(DUMP_destination)
            print(SHA1)
            print(Destination_DIR)
            print("DUMP Destination: " + DUMP_destination)

            DB = SQLCloud()
            DB_Select = DB.select("version")
            result = DB_Select(hashsume=SHA1)
            print(str(len(result)))

            if len(result) < 1:

                if not FileManager.moveFile(DUMP_destination, Destination_DIR, SHA1):
                    FileManager.remove(DUMP_destination)
                    statusList.append([False, filename, DUMP_destination, str(datetime.datetime.today())])
                else:
                    try:
                        temp = Uploaded_File()
                        File_DIR = Destination_DIR + SHA1 + FileManager.extensionSpliter(filename)
                        temp.getInfo(filename, File_DIR, Destination_DIR, google_ID, Description)

                        temp.uploadTheShit()
                        statusList.append([True, filename, File_DIR, str(datetime.datetime.today())])
                    except:
                        print("SQL FAKAP")
            else:
                print('Resoult 1, go to else')
                pathA = result[0][6]
                pathB = Destination_DIR
                FileManager.createLink(pathA, pathB)

        except Exception as Ex:
            print(Ex)

        return statusList
"""
Liczenie hashsumy dla zawartosci pliku

Autor: Rychel Mikołaj
"""

    @staticmethod
    def countHashSum(destination : str):

        """Variables"""
        BUF_SIZE = 65536
        sha1 = hashlib.sha1()

        with open(destination, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha1.update(data)

        return sha1.hexdigest()
