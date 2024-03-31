import pathlib
append = str(pathlib.Path(__file__).parent.parent.parent.resolve())+"\\"

def exec_command(self, in1, command, in2):
    commands = {"openfile" : cmd_openfile, "readfile" : cmd_readfile, "writefile" : cmd_writefile, "closefile" : cmd_closefile}
    if command in commands:
        out = commands[command](self, in1, in2)
        return out
    else:
        print("ERROR: invalid command (line "+str(self.exec_line)+")")
        self.exec_running = False

def cmd_openfile(self, in1, in2):
    try:
        if in2 == None:
            o = open(append + in1[0], 'r+')
            return o
        else:
            o = open(append + in2, 'r+')
            return o
    except:
        print("ERROR: nonexistent file (line "+str(self.exec_line)+")")
        self.exec_running = False
def cmd_readfile(self, in1, in2):
    try:
        c = in1[0].read()
        return c
    except:
        print("ERROR: invalid file object (line "+str(self.exec_line)+")")
        self.exec_running = False
def cmd_writefile(self, in1, in2):
    try:
        if in2 == None:
            in1[0].seek(0)
            in1[0].truncate(0)
            in1[0].write(in1[1])
            return in1[1]
        else:
            in1[0].write(in2)
            return in2
    except:
        print("ERROR: invalid file object or inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
def cmd_closefile(self, in1, in2):
    try:
        r = in1[0].read()
        in1[0].close()
        return r
    except:
        print("ERROR: invalid file object (line "+str(self.exec_line)+")")
        self.exec_running = False