from datetime import *
import math

class File:
    def __init__(self, name, size, format):
        self.name = name
        self.size = size
        self.format = format
        self.created = datetime.now()
        self.blocks = None

    def __str__(self): 
        return f"Archivo: (nombre= {self.name}, Tamaño= {self.size}, formato= {self.format}, creado en = {self.created}, bloques= {self.blocks})\n"

class Explorer():
    def __init__(self, diskSize, blockSize):
        self.diskSize = diskSize
        self.blockSize = blockSize
        self.totalBlocks = diskSize // blockSize
        self.disk = [None] * self.totalBlocks
        self.files = []
        self.recycleBin = []

    def freeDisk(self):
        free = self.diskSize
        for file in self.files:
            free -= file.size
        for file in self.recycleBin:
            free -= file.size
        return free

    def findFreeBlocks(self, neededBlocks):
        index = []
        for i in range(self.totalBlocks):
            if self.disk[i] is None:
                index.append(i)
                if len(index)== neededBlocks:
                    return index
            else:
                index = []
        return None

    def createFile(self, file):
        blocks = self.findFreeBlocks(math.ceil(file.size//self.blockSize))
        if blocks == None:
            return "No se encontro un espacio contiguo disponible"
        else:
            for block in blocks:
                self.disk[block] = file.name
            file.blocks = blocks
            self.files.append(file)
            return print(f"El archivo {file.name} se ha creado con exito")

    def deleteFile(self, fileName):
        for file in self.files:
            if file.name == fileName:
                self.recycleBin.append(file)
                self.files.remove(file)
                return print(f"Su archivo {file.name} ha sido movido a la papelera con exito")

    def cleanBin(self):
        for file in self.recycleBin:
            for i in range(len(self.disk)):
                if self.disk[i] == file.name:
                    self.disk[i] = None
            self.recycleBin.remove(file)
        return print("Su papelera de reciclaje ha sido vaciado correctamente.")
    
    def readFile(self, fileName):
        for file in self.files:
            if file.name == fileName:
                print(f"Su archivo {fileName} se ha encontrado: ")
                return print(file)
        for file in self.recycleBin:
            if file.name == fileName:
                print(f"Su archivo {fileName} se encuentra en la papelera: ")
                return print(file)
        return print(f"El archivo {fileName} no se encuentra")

    def __str__(self):
        info = f"--- Explorador ---\n"
        info += f"Tamano disco disponible: {self.freeDisk()}\n"
        info += f"Tamano bloque: {self.blockSize}\n"
        info += f"Total bloques: {self.totalBlocks}\n"
        info += f"- Bloques libres: {self.disk.count(None)}\n"
        info += f"- Bloques ocupados: {self.totalBlocks - self.disk.count(None)}\n\n"

        info += f"--- Archivos ---\n"
        if self.files:
            for f in self.files:
                info += str(f)
        else:
            info += "No hay archivos en el disco\n"

        info += f"\n--- Papelera ---\n"
        if self.recycleBin:
            for f in self.recycleBin:
                info += str(f)
        else:
            info += "Papelera vacia\n"

        return info


if __name__ == "__main__":
    explorer = Explorer(diskSize=100, blockSize=10)

    file1 = File("hola", 10, "txt")
    file2 = File("petuche", 30, "mp4")
    print(file1)

    print(explorer)
    explorer.createFile(file1)
    explorer.readFile("hola")
    print(explorer)
    explorer.deleteFile("hola")
    explorer.readFile("hola")
    print(explorer)
    explorer.createFile(file2)
    print(explorer)
    explorer.cleanBin()
    print(explorer)