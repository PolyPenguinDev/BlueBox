import time
import random

class cnv:
    def __init__(self):
        self.exec_line = 0
        self.exec_running = False
        self.tags = {}
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
        if command == "string":
            return in2
        elif command == "tostring":
            return str(in1[0])
        elif command == "int":
            return int(in2)
        elif command == "toint":
            return int(in1[0])
        elif command == "end":
            exec_running = False
        elif command == "go":
            if in1 == []:
                exec_line = self.tags[in2]-1
            else:
                exec_line = self.tags[in1[0]]-1
        elif command == "sleep":
            if in1 == []:
                time.sleep(int(in2))
            else:
                time.sleep(int(in1[0]))
        elif command == "exec":
            if in1 == []:
                self.execParsedLine(self.parsed[self.tags[in2]-1])
            else:
                self.execParsedLine(self.parsed[self.tags[in1[0]]-1])
        elif command == "exif":
            if in1[0]:
                if in2 == None:
                    self.execParsedLine(self.parsed[self.tags[in1[1]]-1])
                else:
                    self.execParsedLine(self.parsed[self.tags[in2]-1])
            return in1[0]
        elif command == "not":
            if in2 == None:
                return not in1[0]
            else:
                return not in2
        elif command == "goif":
            if in1[0]:
                if in2 == None:
                    exec_line = self.tags[in1[1]]-1
                else:
                    exec_line = self.tags[in2]-1
        elif command == "print":
            print(in1[0])
        elif command == "input":
            return input(in1[0])
        elif command == "var":
            if len(in1) > 1:
                vars[in2][in1[0]] = in1[1]
            elif in1 != []:
                try:
                    vars[in2]= in1[0].copy()
                except:
                    vars[in2]= in1[0]
            return vars[in2]
        elif command == "equals":
            if in2 == None:
                return in1[0] == in1[1]
            else:
                return in1[0] == in2
        elif command == "add":
            if in2 == None:
                return in1[0] + in1[1]
            else:
                return in1[0] + in2
        elif command == "greater":
            return in1[0] > in1[1]
        elif command == "less":
            return in1[0] < in1[1]
        elif command == "and":
            return in1[0] and in1[1]
        elif command == "or":
            return in1[0] or in1[1]
        elif command == "randirange":
            if in2 == None:
                return random.randint(in1[0], in1[1])
            else:
                return random.randint(in1[0], int(in2))
        elif command == "power":
            return in1[0]**in1[1]
        elif command == "list":
            return []
        elif command == "append":
            in1[0].append(in1[1])
            return in1[0]
        elif command == "get":
            if in2 == None:
                return in1[0][in1[1]]
            else:
                return in1[0][in2]
        elif command == "join":
            if in2 == None:
                return in1[1].join(in1[0])
            else:
                return in2.join(in1[0])
        elif command == "pass":
            return None
        elif command == "multiply":
            return in1[0]*in1[1]
        elif command == "divide":
            return in1[0]/in1[1]
        elif command == "subtract":
            return in1[0]**in1[1]
        elif command == "float":
            return float(in2)
        elif command == "tofloat":
            return float(in1[0])
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
        elif "," in line:
            splitted = self.splitLine(line)
            one = self.execParsedLineSegment(splitted[0])
            two = self.execParsedLineSegment(splitted[1])
            self.execParsedLineSegment(splitted[2], start=[one, two])
        else:
            self.execParsedLineSegment(line)
    def execParsed(self, parsed):
        global exec_running
        global exec_line
        global vars
        exec_running = True
        exec_line = 0
        vars = {}
        while exec_running:
            exec_line += 1
            line = parsed[exec_line-1]
            if line != []:
                self.execParsedLine(line)
            
            
        exec_running = False
    def exec(self, text):
        self.execParsed(self.parse(text))
    def execFile(self, fp):
        with open(fp, "r") as f:
            file = f.read()
        exec(file)