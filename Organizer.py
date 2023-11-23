import os
from pathlib import Path

class Organizer:

    ''' 
        "The constructor's purpose is to parse the 'Organizer' file and set all the attributes I need."
    '''
    def __init__(self) -> None:
    # bool to check that every thing went good 
        self._good = True
    # searching attributes
        self._target = ""
        self._targetPath = ""
        self._searchingStart = ""
        self._find = False
        # we are parsing the file and calling on eache task it's function to parse it  
        with open("Organizer.org", 'r') as file:
            task = ["S:"]
            pars = [self.ParsSearching]
            
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
                except:
                    print("An error occurred while parsing the task {}".format(task[idx]))
                    self._good = False
                    exit(0)
    
    def cleaner():
        pass

    # *********************** The parsser of the Searching task *********************** 
    def ParsSearching(self, tokens):
        if len (tokens) < 2:
            return
        self._target = tokens[1]
        if len(tokens) == 2:
            self._searchingStart = Path.home().__str__()
        else:
            if (os.path.exists(tokens[2])):
                self._searchingStart = tokens[2]
            # if the path doesn't exist
            else:
                raise Exception
    # *********************** The Searching task *********************** 
    
    def searching(self) -> None:
        print("Searching !!\n" * 4, end="")
        # here we are searching
        for root, dirs, files in os.walk(self._searchingStart):
            if self._find == True:
                break
            for file in dirs + files:
                # if we find our target we save it's path and we break
                if file == self._target:
                    self._find = True
                    self._targetPath = os.path.join(root, file)
                    break
    # ***************** the purpose of the Destructor is to write to the file result at the end ,It provides a  summury of what this python program does **************
    def __del__(self):
            if (not self._good):
                return
            print(self._targetPath) if self._find  else print ("File not found")