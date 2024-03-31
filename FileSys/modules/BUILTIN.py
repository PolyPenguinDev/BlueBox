import random
import time
import importlib.util
import pathlib

def importxl(module_path):
    module_path = str(pathlib.Path(__file__).parent)+"\\"+module_path+"\\main.py"
    spec = importlib.util.spec_from_file_location("example_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
def exec_command(self, in1, command, in2):
    commands = {"string" : cmd_string, "tostring" : cmd_tostring, "int" : cmd_int, "toint" : cmd_toint, "end" : cmd_end, "go" : cmd_go, "sleep" : cmd_sleep, "exec" : cmd_exec, "exif" : cmd_exif, "not" : cmd_not, "goif" : cmd_goif, "print" : cmd_print, "input" : cmd_input, "var" : cmd_var, "equals" : cmd_equals, "add" : cmd_add, "greater" : cmd_greater, "less" : cmd_less, "and" : cmd_and, "or" : cmd_or, "randirange" : cmd_randirange, "power" : cmd_power, "list" : cmd_list, "append" : cmd_append, "get" : cmd_get, "join" : cmd_join, "pass" : cmd_pass, "multiply" : cmd_multiply, "divide" : cmd_divide, "subtract" : cmd_subtract, "float" : cmd_float, "tofloat" : cmd_tofloat, "down" : cmd_down, "v" : cmd_down}
    if command == "":
        return None
    elif command in commands:
        return commands[command](self, in1, in2)
    elif "." in command:
        mod = importxl(command.split(".")[0])
        return mod.exec_command(self, in1, command.split(".")[1], in2)
    else:
        print("ERROR: invalid command (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None


def cmd_string(self, in1, in2):
    return in2
def cmd_tostring(self, in1, in2):
    return str(in1[0])
def cmd_int(self, in1, in2):
    try:
        return int(in2)
    except:
        print("ERROR: invalid int (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_toint(self, in1, in2):
    try:
        return int(in1[0])
    except:
        print("ERROR: invalid int (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None               
def cmd_end(self, in1, in2):
    self.exec_running = False
def cmd_go(self, in1, in2):
    try:
        if in1 == []:
            self.exec_line = self.tags[in2]-1
        else:
            self.exec_line = self.tags[in1[0]]-1
    except:
        print("ERROR: invalid tag (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_sleep(self, in1, in2):
    try:
        if in1 == []:
            self.wtil = time.time() + float(in2)
        else:
            self.wtil = time.time() + in1[0]
    except:
        print("ERROR: invalid float/int (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_exec(self, in1, in2):
    try:
        if in1 == []:
            self.p_line = self.tags[in2]-1
            self.execParsedLine(self.parsed[self.tags[in2]-1])
        else:
            self.p_line = self.tags[in1[0]]
            self.execParsedLine(self.parsed[self.tags[in1[0]]-1])
    except:
        print("ERROR: invalid tag (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_exif(self, in1, in2):
    #try:
        if in1[0]:
            if in2 == None:
                self.p_line = self.tags[in1[1]]-1
                self.execParsedLine(self.parsed[self.tags[in1[1]]-1])
            else:
                self.p_line = self.tags[in2]
                self.execParsedLine(self.parsed[self.tags[in2]-1])
        return in1[0]
        '''except:
        print("ERROR: invalid tag or bool (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None'''
def cmd_down(self, in1, in2):
    self.execParsedLine(self.parsed[self.p_line-1])
def cmd_not(self, in1, in2):
    try:
        if in2 == None:
            return not in1[0]
        else:
            return not in2
    except:
        print("ERROR: invalid bool (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_goif(self, in1, in2):
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
def cmd_print(self, in1, in2):

    print(in1[0])
def cmd_input(self, in1, in2):
    return input(in1[0])
def cmd_var(self, in1, in2):
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
def cmd_equals(self, in1, in2):
    try:
        if in2 == None:
            return in1[0] == in1[1]
        else:
            return in1[0] == in2
    except:
        print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_add(self, in1, in2):
    try:
        if in2 == None:
            return in1[0] + in1[1]
        else:
            return in1[0] + in2
    except:
        print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_greater(self, in1, in2):
    try:
        return in1[0] > in1[1]
    except:
        print("ERROR: invalid int (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_less(self, in1, in2):
    try:
        return in1[0] < in1[1]
    except:
        print("ERROR: invalid int (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_and(self, in1, in2):
    try:
        return in1[0] and in1[1]
    except:
        print("ERROR: invalid boolean inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_or(self, in1, in2):
    try:
        return in1[0] or in1[1]
    except:
        print("ERROR: invalid boolean inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_randirange(self, in1, in2):
    try:
        if in2 == None:
            return random.randint(in1[0], in1[1])
        else:
            return random.randint(in1[0], int(in2))
    except:
        print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_power(self, in1, in2):
    try:
        return in1[0]**in1[1]
    except:
        print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_list(self, in1, in2):
    return []
def cmd_append(self, in1, in2):
    try:
        in1[0].append(in1[1])
        return in1[0]
    except:
        print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_get(self, in1, in2):
    try:
        if in2 == None:
            return in1[0][in1[1]]
        else:
            return in1[0][in2]
    except:
        print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_join(self, in1, in2):
    try:
        if in2 == None:
            return in1[1].join(in1[0])
        else:
            return in2.join(in1[0])
    except:
        print("ERROR: invalid inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_pass(self, in1, in2):
    return None
def cmd_multiply(self, in1, in2):
    try:
        return in1[0]*in1[1]
    except:
        print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_divide(self, in1, in2):
    try:
        return in1[0]/in1[1]
    except:
        print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_subtract(self, in1, in2):
    try:
        return in1[0]-in1[1]
    except:
        print("ERROR: invalid intager inputs (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_float(self, in1, in2):
    try:
        return float(in2)
    except:
        print("ERROR: invalid float (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None
def cmd_tofloat(self, in1, in2):
    try:
        return float(in1[0])
    except:
        print("ERROR: invalid float (line "+str(self.exec_line)+")")
        self.exec_running = False
        return None