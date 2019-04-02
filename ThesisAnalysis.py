'''
GOAL: Create a tidy csv file from different, but identically formatted text files procedurally generated
by a specific application. Originally for an independent research project, posted with permission from researcher.

Written by: Kathy Thompson, 3/31/19

'''
import os
import re

#Each file parsed has the same length, with the same categories described.
LENGTH_CATEGORIES = 12
FILE_LENGTH=145
CATEGORIES = ["cmx", "cml", "csi", "csq", "lin", "sli", "smu", "ssi", "sqm", "sqp", "tri", "tsq"]

NAME=re.compile(r'(subject\d|subject\d\d|s\d|s\d\d)+(transfer\d|transfer\d\d|learning\d|learning\d\d)')


#wrapping the data inside of a class decreases nesting and allows for easier parsing
#Called this class RAW_FILE since FILE is a reserved definition
class RAW_FILE:
    def __init__(self):
        self.totalacc = {}
        self.accuracy = {}
        self.response = {}
        self.stimulus_count = {}
        self.all = {}
        self.subject=None
        self.filename=None
        self.task=None
        
        self.t1 = {} 
        self.s1 = {}
        self.s2 = {}
        self.d1 = {}
        self.d2 = {}

        #taking just the values from a line
    def parse_line(self, line):
        equals = line.find("=")
        percent = line.find("%")
        value = line[equals+2: percent]
        return value

        
    def parse_section(self, line): 
        #for the first half of the file
        if "All Stimuli" in line:
            equals = line.find("=")
            value = line[equals+2:]
            self.all["All"] = value

        if "Total Accuracy (Resp)" in line:
            value = self.parse_line(line)
            self.totalacc["Resp"] = value

        if "Total Accuracy (Stim)" in line:
            value = self.parse_line(line)
            self.totalacc["Stim"] = value
        #for each category within the block of data
        for i in range(LENGTH_CATEGORIES): 
            if "Accuracy (" + str(CATEGORIES[i]) in line:
                value = self.parse_line(line)
                self.accuracy[str(CATEGORIES[i])] = value

            if "Responses (" + str(CATEGORIES[i]) in line:
                value = self.parse_line(line)
                self.response[str(CATEGORIES[i])] = value

            if "Stimuli   (" + str(CATEGORIES[i]) in line:
                value = self.parse_line(line)
                self.stimulus_count[str(CATEGORIES[i])] = value
        return

    def parse_category(self, line, f):
        for i in range(LENGTH_CATEGORIES):
            if line == str(CATEGORIES[i]):
                cat = CATEGORIES[i]
                line = f.readline().rstrip() #skips over t1

                line = f.readline().rstrip() #s1
                v = self.parse_line(line)
                self.s1[cat]= v

                line = f.readline().rstrip() #s2
                v = self.parse_line(line)
                self.s2[cat]= v

                line = f.readline().rstrip() #d1
                v = self.parse_line(line)
                self.d1[cat]= v

                line = f.readline().rstrip() #d2
                v = self.parse_line(line)
                self.d2[cat]= v
#end of class definitions

def parse_files(): #actual workhorse of the file
    list_files=os.listdir(os.getcwd())
    list_of_files = []
    for filename in list_files:
        if "txt" in filename:
            file_obj=RAW_FILE()
            search=NAME.search(filename)
            file_obj.subject=search.group(1)
            file_obj.task=search.group(2)
            file_obj.filename=search.group()
            with open(filename) as f:
                list_of_files.append(filename)
                for i in range(FILE_LENGTH):
                    line=f.readline().rstrip()
                    file_obj.parse_section(line)
                    file_obj.parse_category(line,f)
    return

#originally the goal was to output 8 different files corresponding to different "tasks", but we compromised on one
#this is why parse_files is not simply the main() function.

def main():
    parse_files()
    print("done")


if __name__ == "__main__":
    main()




