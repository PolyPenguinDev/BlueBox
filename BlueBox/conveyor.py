import time
import random

class cnv:
    def __init__(self):
        self.exec_line = 0
        self.exec_running = False
        self.tags = {}
        self.vars = {}
        self.parsed = []
    def parse(self, file):
        lines = file.split('\n')
        listed = []
        for line in lines:
            if line.startswith("    "):
                line = line[4::]
            linel = []
            word = ""
            stri = False
            al = False
            for letter in line:
                
                if letter == " " and not stri:
                    linel.append(word)
                    word = ""
                else:
                    if letter == "\"" or letter == "\'":
                        stri = not stri
                    else:
                        if letter == "," and not stri:
                            linel.append(word)
                            word = ","
                        else:
                            word += letter
            linel.append(word) #fibb
            listed.append(linel)
        for i in enumerate(listed):
            tag = i[1][-1]
            if len(tag) > 0:
                if tag[0] == "#":
                    listed[i[0]].pop(-1)
                    self.tags[tag[1::]] = i[0]+1
        self.parsed=listed
        return listed
    def execCommand(self, in1, command, in2):
        if command == "":
            return None
        elif command == "string":
            return in2
        elif command == "tostring":
            return str(in1[0])
        elif command == "int":
            try:
                return int(in2)
            except:
                print("ERROR: invalid int (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "toint":
            try:
                return int(in1[0])
            except:
                print("ERROR: invalid int (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
                
        elif command == "end":
            self.exec_running = False
        elif command == "go":
            try:
                if in1 == []:
                    self.exec_line = self.tags[in2]-1
                else:
                    self.exec_line = self.tags[in1[0]]-1
            except:
                print("ERROR: invalid tag (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "sleep":
            try:
                if in1 == []:
                    time.sleep(int(in2))
                else:
                    time.sleep(in1[0])
            except:
                print("ERROR: invalid int (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "exec":
            try:
                if in1 == []:
                    self.execParsedLine(self.parsed[self.tags[in2]-1])
                else:
                    self.execParsedLine(self.parsed[self.tags[in1[0]]-1])
            except:
                print("ERROR: invalid tag (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "exif":
            try:
                if in1[0]:
                    if in2 == None:
                        self.execParsedLine(self.parsed[self.tags[in1[1]]-1])
                    else:
                        self.execParsedLine(self.parsed[self.tags[in2]-1])
                return in1[0]
            except:
                print("ERROR: invalid tag or bool (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "not":
            try:
                if in2 == None:
                    return not in1[0]
                else:
                    return not in2
            except:
                print("ERROR: invalid bool (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "goif":
            try:
                if in1[0]:
                    if in2 == None:
                        self.exec_line = self.tags[in1[1]]-1
                    else:
                        self.exec_line = self.tags[in2]-1
            except:
                print("ERROR: invalid tag or bool (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "print":
            print(in1[0])
        elif command == "input":
            return input(in1[0])
        elif command == "var":
            try:
                if len(in1) > 1:
                    self.vars[in2][in1[0]] = in1[1]
                elif in1 != []:
                    try:
                        self.vars[in2]= in1[0].copy()
                    except:
                        self.vars[in2]= in1[0]
                return self.vars[in2]
            except:
                print("ERROR: variable error (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "equals":
            try:
                if in2 == None:
                    return in1[0] == in1[1]
                else:
                    return in1[0] == in2
            except:
                print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "add":
            try:
                if in2 == None:
                    return in1[0] + in1[1]
                else:
                    return in1[0] + in2
            except:
                print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "greater":
            try:
                return in1[0] > in1[1]
            except:
                print("ERROR: invalid int (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "less":
            try:
                return in1[0] < in1[1]
            except:
                print("ERROR: invalid int (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "and":
            try:
                return in1[0] and in1[1]
            except:
                print("ERROR: invalid boolean inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "or":
            try:
                return in1[0] or in1[1]
            except:
                print("ERROR: invalid boolean inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "randirange":
            try:
                if in2 == None:
                    return random.randint(in1[0], in1[1])
                else:
                    return random.randint(in1[0], int(in2))
            except:
                print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "power":
            try:
                return in1[0]**in1[1]
            except:
                print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "list":
            return []
        elif command == "append":
            try:
                in1[0].append(in1[1])
                return in1[0]
            except:
                print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "get":
            try:
                if in2 == None:
                    return in1[0][in1[1]]
                else:
                    return in1[0][in2]
            except:
                print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "join":
            try:
                if in2 == None:
                    return in1[1].join(in1[0])
                else:
                    return in2.join(in1[0])
            except:
                print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "pass":
            return None
        elif command == "multiply":
            try:
                return in1[0]*in1[1]
            except:
                print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "divide":
            try:
                return in1[0]/in1[1]
            except:
                print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "subtract":
            try:
                return in1[0]-in1[1]
            except:
                print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "float":
            try:
                return float(in2)
            except:
                print("ERROR: invalid float (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        elif command == "tofloat":
            try:
                return float(in1[0])
            except:
                print("ERROR: invalid float (line "+str(self.exec_line)+")")
                self.exec_running = False
                return None
        else:
            print("ERROR: invalid function \""+ command+"\" (line "+str(self.exec_line)+")")
            self.exec_running = False
        return None
    def execParsedLineSegment(self, line, start=[]):
        if line[0].startswith("//"):
            return
        if len(line) == 0:
            return
        payload = None
        if len(line) > 1:
            if line[1] != "->" and line[1] != "=>" and line[1] != ",":
                payload = line[1]
        out = self.execCommand(start, line[0], payload)
        if not self.exec_running:
            return
        n = []
        if out != None:
            n = [out]
        while line[0] != "->" and line[0] != "=>" and line[0] != ",":
            line.pop(0)
            if len(line) ==0:
                return out
        line.pop(0)
        self.execParsedLineSegment(line, n)
    def splitLine(self, line):
        set =[]
        this = []
        for i in line:
            if i == "," or i == "=>":
                set.append(this)
                this = []
            else:
                this.append(i)
        set.append(this)
        return set
    def execParsedLine(self, line):
        if line[0].startswith("//"):
            return
        line = line.copy()
        if "&" in line:
            lines = []
            liner = []
            for i in line:
                if i == "&":
                    lines.append(liner)
                    liner = []
                else:
                    liner.append(i)
            lines.append(liner)
            for i in lines:
                self.execParsedLine(i)
                if not self.exec_running:
                    return
        elif "," in line:
            splitted = self.splitLine(line)
            one = self.execParsedLineSegment(splitted[0])
            if not self.exec_running:
                return
            two = self.execParsedLineSegment(splitted[1])
            if not self.exec_running:
                return
            self.execParsedLineSegment(splitted[2], start=[one, two])
            if not self.exec_running:
                return
        else:
            self.execParsedLineSegment(line)
            if not self.exec_running:
                return
    def execParsed(self, parsed):
        self.exec_running = True
        self.exec_line = 0
        self.vars = {}
        while self.exec_running:
            self.exec_line += 1
            if self.exec_line > len(parsed):
                break   
            line = parsed[self.exec_line-1]
            if line != []:
                self.execParsedLine(line)
            
            
        self.exec_running = False
    def exec(self, text):
        self.execParsed(self.parse(text))
    def execFile(self, fp):
        with open(fp, "r") as f:
            file = f.read()
        self.exec(file)