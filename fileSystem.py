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

class Dir():
    def __init__(self,name, parent=None):
        self.name = name
        self.parent = parent
        self.files = []
        self.subdir = []

    def addFile(self,file):
        self.files.append(file)

    def addSubDir(self,subdir):
        self.subdir.append(subdir)

    def getPath(self):
        if self.parent:
            return self.parent.getPath() + "/" + self.name
        return self.name

    def __str__(self):
        info = f"Directorio: {self.getPath()}\n"
        for d in self.subdir:
            info += f" <dir> {d.name}\n"
        for f in self.files:
            info += f" <archivo> {f.name}\n"
        return info

class Explorer():
    def __init__(self, diskSize, blockSize):
        self.diskSize = diskSize
        self.blockSize = blockSize
        self.totalBlocks = diskSize // blockSize
        self.disk = [None] * self.totalBlocks
        self.root = Dir("root")
        self.currentDir = self.root
        self.recycleBin = []

    def freeDisk(self):
        free = self.diskSize
        for file in self.currentDir.files:
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
            self.currentDir.addFile(file)
            return print(f"El archivo {file.name} se ha creado con exito en el directorio {self.currentDir.getPath()}")

    def deleteFile(self, fileName):
        for file in self.currentDir.files:
            if file.name == fileName:
                self.recycleBin.append(file)
                self.currentDir.files.remove(file)
                return print(f"Su archivo {file.name} ha sido movido a la papelera con exito")
        return print(f"El archivo {fileName} no se encuentra")

    def cleanBin(self):
        for file in self.recycleBin[:]:
            for i in range(len(self.disk)):
                if self.disk[i] == file.name:
                    self.disk[i] = None
            self.recycleBin.remove(file)
        return print("Su papelera de reciclaje ha sido vaciado correctamente.")
    
    def readFile(self, fileName):
        for file in self.currentDir.files:
            if file.name == fileName:
                print(f"Su archivo {fileName} se ha encontrado en el directorio {self.currentDir.getPath()} ")
                return print(file)
        for file in self.recycleBin:
            if file.name == fileName:
                print(f"Su archivo {fileName} se encuentra en la papelera: ")
                return print(file)
        return print(f"El archivo {fileName} no se encuentra")

    def createDir(self,name):
        newDir = Dir(name,self.currentDir)
        self.currentDir.addSubDir(newDir)
        print(f"Directorio {name} creado en {self.currentDir.getPath()}")

    def changeDir(self,name):
        if name == "..":
            if self.currentDir.parent is not None:
                self.currentDir = self.currentDir.parent
                print(f"Cambiado a {self.currentDir.getPath()}")
            else:
                print("Ya se encuentra en la raíz")
        else:
            for sub in self.currentDir.subdir:
                if sub.name == name:
                    self.currentDir = sub
                    return print(f"-- {self.currentDir.getPath()}")
            return print(f"No existe el subdirectorio {name}")

    
    def listDirectory(self):
        print(self.currentDir)

    def __str__(self):
        info = f"--- Explorador ---\n"
        info += f"Tamano disco disponible: {self.freeDisk()}\n"
        info += f"Tamano bloque: {self.blockSize}\n"
        info += f"Total bloques: {self.totalBlocks}\n"
        info += f"- Bloques libres: {self.disk.count(None)}\n"
        info += f"- Bloques ocupados: {self.totalBlocks - self.disk.count(None)}\n\n"

        info += f"--- Archivos ---\n"
        if self.currentDir.files:
            for f in self.currentDir.files:
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

    explorer.createDir("docs")
    explorer.createDir("media")
    explorer.listDirectory()

    explorer.changeDir("docs")
    explorer.createFile(file1)
    explorer.listDirectory()

    explorer.changeDir("..")
    explorer.changeDir("media")
    explorer.createFile(file2)
    explorer.listDirectory()

    print(explorer)

    explorer.deleteFile("petuche")
    explorer.cleanBin()
    print(explorer)