# Class file
from static.classes.interfaces.IFile import File 

"""
Klasa reprezentacyjna pliku, wykorzystywana do przekazywania informacji o plikach
do widoków.

Autor: Rychel Mikołaj
"""
class File(File):

    def __init__(self, data: list):
        self.fileID=""
        self.Name=""
        self.Extension=""
        self.FilePath=""
        self.Size=""
        self.HashSum=""
        self.Icon=""
        self.construct(data)
        print(self.serialize())

    def construct(self, data: list):
        self.fileID = str(data[0])
        self.Name = str(data[1])
        self.Extension = str(data[2])
        self.FilePath = str(data[3])
        self.Size = str(data[4])
        self.HashSum = str(data[5])

        if(self.Extension == "None"):

            self.Icon = "folder-open-empty"
        else:
            self.Icon = "file-image"

    def serialize(self) -> str:
        """Serialized format ID:Name:Extension:FilePath:Size:HashSum"""
        return self.fileID+':'+self.Name+':'+str(self.Extension)+':'+self.FilePath+':'+self.Size+':'+self.HashSum+':'+self.Icon

