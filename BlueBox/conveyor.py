from importxl import importxl
import pathlib
import time
append = str(pathlib.Path(__file__).parent.parent.resolve())
class cnv:
    def request_tick(self, module, keepalive=[]):
        self.ticks.append([append+'\\FileSys\\modules\\'+module+"\\main.py", keepalive])

    def __init__(self):
        self.p_line = 0
        self.wtil = 0
        self.ticks=[]
        self.bb_sid = None
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
            linel.append(word) 
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
        builtin = importxl(append+'\\FileSys\\modules\\BUILTIN.py')
        return builtin.exec_command(self, in1, command, in2)
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
            if time.time() >= self.wtil:
                self.exec_line += 1
                self.p_line = self.exec_line
                if self.exec_line > len(parsed):
                    break   
                line = parsed[self.exec_line-1]
                if line != []:
                    self.execParsedLine(line)
            for i in self.ticks:
                tickker = importxl(i[0])
                tickker.tick(self, keepalive=i[1])
            
            
        self.exec_running = False
    def exec(self, text):
        self.execParsed(self.parse(text))
    def execFile(self, fp):
        with open(fp, "r") as f:
            file = f.read()
        self.exec(file)