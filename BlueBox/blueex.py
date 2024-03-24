import json
import pathlib
inpath = str(pathlib.Path(__file__).parent.resolve())+'\\instances\\bbi.json'
append = str(pathlib.Path(__file__).parent.parent.resolve())+"\\FileSys\\"
def add_request(what):
    with open(inpath, 'r') as f:
        l = json.load(f)
        l["requests"].append(what)
    with open(inpath, 'w') as f:
        json.dump(l, f)
def run(self, in1, in2, command, sid):
        try:
            with open(inpath, 'r') as f:
                truesid = json.load(f)["session id"]
        except:
            print("ERROR: invalid BlueBox instance (line "+str(self.exec_line)+")")
            self.exec_running = False
            return None
        if truesid != sid:
            print("ERROR: invalid BlueBox instance (line "+str(self.exec_line)+")")
            self.exec_running = False
            return None
        elif command == "openfile":
            try:
                if in2 == None:
                    o = open(append + in1[0], 'r+')
                    add_request("opened file \""+in1[0]+"\"")
                    return o
                else:
                    o = open(append + in2, 'r+')
                    add_request("opened file \""+in2+"\"")
                    return o
            except:
                print("ERROR: um... that file doesn't exist (line "+str(self.exec_line)+")")
                self.exec_running = False
        elif command == "readfile":
            try:
                c = in1[0].read()
                add_request("read file")
                return c
            except:
                print("ERROR: so... that's not a file object (line "+str(self.exec_line)+")")
                self.exec_running = False
        elif command == "writefile":
            try:
                if in2 == None:
                    in1[0].seek(0)
                    in1[0].truncate(0)
                    in1[0].write(in1[1])
                    add_request("wrote to file")
                    return in1[1]
                else:
                    in1[0].write(in2)
                    add_request("wrote to file")
                    return in2
            except:
                print("ERROR: sir... that's not a file object or you aren't giving me something to write (line "+str(self.exec_line)+")")
                self.exec_running = False
        elif command == "closefile":
            try:
                r = in1[0].read()
                in1[0].close()
                add_request("closed/read file")
                return r
            except:
                print("ERROR: so... that's not a file object (line "+str(self.exec_line)+")")
                self.exec_running = False

