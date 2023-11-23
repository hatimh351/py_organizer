import os
from pathlib import Path
import OrganizerExceptions
import re

class Organizer:

    ''' 
        "The constructor's purpose is to parse the 'Organizer' file and set all the attributes I need."
    '''
    def __init__(self) -> None:
    # bool to check that every thing went good 
        self._good = True
    # searching attributes
        self._targets = []
        self._targetPath = []
        self._searchingStart = []
        self._find = False
    # orginizer attributes
        self._dirsToOrganize = []
        # we are parsing the file and calling on eache task it's function to parse it  
        with open("Organizer.org", 'r') as file:
            task = ["S:", "O:"]
            pars = [self.ParsSearching, self.ParsOrganizer]
            
            for line in file:
                tokens = line.split()
                if len(tokens) == 0:
                    continue
                idx = -1
                try:
                    idx = task.index(tokens[0])
                except:
                    print("Using of anknown task")
                    self._good = False
                    exit(0)
                # we are checking if the parssing throw an exception
                try:
                    pars[idx](tokens)
                except OrganizerExceptions.Parssing:
                    print("An error occurred while parsing the task {}".format(task[idx]))
                    self._good = False
                    exit(0)
                except OrganizerExceptions.FileDoesntExist:
                    print("A directory or File in the task {} dosen't exist".format(task[idx]))
                    self._good = False
                    exit(0)

    # *********************** The parsser of the Organizer task *********************** 
    def ParsOrganizer(self, tokens):
        if (len(tokens) < 2):
            raise Exception
        if (os.path.isdir(tokens[1])):
            self._dirsToOrganize.append(tokens[1])
        else:
            raise Exception

    # *********************** The Organizer task *********************** 
    def organizer(self):
        for dir in self._dirsToOrganize:
            os.chdir(dir)
            files = [file for file in os.listdir() if os.path.isfile(file)]
            ext = []
            for file in files:
                token = file.split('.')
                if len(token) == 2:
                    ext.append(token[1])
                    os.mkdir(ext[1:])
            for file in files:
                pass                

    # *********************** The parsser of the Searching task *********************** 
    def ParsSearching(self, tokens):
        if len (tokens) < 2:
            OrganizerExceptions.Parssing
        self._targets.append(tokens[1])
        if len(tokens) == 2:
            self._searchingStart.append(Path.home().__str__())
        else:
            if (os.path.exists(tokens[2])):
                self._searchingStart.append(tokens[2])
            # if the path doesn't exist
            else:
                raise OrganizerExceptions.FileDoesntExist
    # *********************** The Searching task *********************** 
    
    def searching(self) -> None:
        print("Searching !!\n" * 4, end="")
        # here we are searching
        
        for searchingStart, target in zip(self._searchingStart, self._targets):
            find = False
            for root, dirs, files in os.walk(searchingStart):
                if find == True:
                    break
                for file in dirs + files:
                    # if we find our target we save it's path and we break
                    if file == target:
                        self._targetPath.append(os.path.join(root, file))
                        find = True
                        break
            if find == False:
                self._targetPath.append("")

    # ***************** the purpose of the Destructor is to write to the file result at the end ,It provides a  summury of what this python program does **************
    def __del__(self):
            if (not self._good):
                return
            for target,path in zip(self._targets, self._targetPath):
                if (len(path)):
                    print("The {} was found their path is {}".format(target, path))
                else:
                    print("The {} wasn't found".format(target))