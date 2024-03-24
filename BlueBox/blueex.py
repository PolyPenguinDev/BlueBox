import json
def run(self, in1, in2, command, sid):
        with open("BlueBox/instances/bbi.json", 'r') as f:
            truesid = json.load(f)["session id"]
        if truesid != sid:
            print("ERROR: invalid BlueBox instance (line "+str(self.exec_line)+")")
            self.exec_running = False
            return None
        elif command == "openfile":
            try:
                if in2 == None:
                    return open(in1[0], 'w+')
                else:
                    return open(in2, 'w+')
            except:
                print("ERROR: um... that file doesn't exist (line "+str(self.exec_line)+")")
                self.exec_running = False
        elif command == "readfile":
            try:
                return in1[0].read()
            except:
                print("ERROR: so... that's not a file object (line "+str(self.exec_line)+")")
                self.exec_running = False
        elif command == "writefile":
            try:
                if in2 == None:
                    return in1[0].write(in1[1])
                else:
                    return in1[0].write(in2)
            except:
                print("ERROR: sir... that's not a file object or you arn't giving me something to write (line "+str(self.exec_line)+")")
                self.exec_running = False
        elif command == "closefile":
            try:
                return in1[0].close()
            except:
                print("ERROR: so... that's not a file object (line "+str(self.exec_line)+")")
                self.exec_running = False

