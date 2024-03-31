def exec_command(self, in1, command, in2):
    commands = {"execfile" : cmd_execfile, "exec" : cmd_exec}
    if command in commands:
        out = commands[command](self, in1, in2)
        return out
    else:
        print("ERROR: invalid command (line "+str(self.exec_line)+")")
        self.exec_running = False

def cmd_execfile(self, in1, in2):
    try:
        file = in1[0].read()
    except:
        print("ERROR: invalid file object (line "+str(self.exec_line)+")")
        self.exec_running = False
    exec(file, {}, self.vars)
def cmd_exec(self, in1, in2):
    try:
        if in2 == None:
            exec(in1[0], {}, self.vars)
        else:
            exec(in2, {}, self.vars)
    except:
        print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
        self.exec_running = False