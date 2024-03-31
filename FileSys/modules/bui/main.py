
import tkinter as tk

class gui:
    def __init__(self):
        self.settag = []
        self.last = {}
    def exitwindow(self):
        self.cnv.exec_running = False
        self.root.destroy()

    def tick(self, cnv):
        self.cnv = cnv
        self.root.update_idletasks()
        self.root.update()
        if self.variables != self.last:
            for k, v in self.variables.items():
                if k in self.last:
                    if v.get()!= self.last[k]:
                        cnv.vars[k] = v.get()
        for k, v in cnv.vars.items():
            if k in self.variables:
                if v != self.variables[k].get():
                    self.variables[k].set(v)
        for i in self.settag:
            cnv.execParsedLine(cnv.parsed[cnv.tags[i] -1])
        self.settag = []
        self.last = cnv.vars.copy()
        return [self]

    def exec_command(self, cnv, in1, command, in2):
        commands = {"startgui" : self.cmd_startgui}
        if command in commands:
            out = commands[command](cnv, in1, in2)
            return out
        else:
            print("ERROR: invalid command (line "+str(cnv.exec_line)+")")
            cnv.exec_running = False

    def cmd_startgui(self, cnv, in1, in2):
        try:
            if in2 == None:
                self.read_file(in1[0])
            else:
                self.read_file(in2)
            self.last = self.variables.copy()
            cnv.request_tick('bui', keepalive=[self])
            return self
        except:
            print("ERROR: starting gui failed (line "+str(cnv.exec_line)+")")
            cnv.exec_running = False
    def execute_command(self, command):
        g = command.strip()
        self.settag.append(g)
    def doline(self, line, root):
        if line.startswith("'") and line.endswith("'"):
            text_var = tk.StringVar()
            text, var_name = line[1:-1].split(' : ')
            text_var.set(text)
            tk.Label(root, textvariable=text_var).pack(side = tk.LEFT)
            self.variables[var_name.strip()] = text_var
        elif line.startswith('[') and line.endswith(']'):
            button_text, command = line[1:-1].split(' : ')
            tk.Button(root, text=button_text, command=lambda cmd=command: self.execute_command(cmd)).pack(side = tk.LEFT)
        elif line.startswith('<') and line.endswith('>'):
            checkbox_text, var_name = line[1:-1].split(' : ')
            checkbox_var = tk.BooleanVar()
            tk.Checkbutton(root, text=checkbox_text, variable=checkbox_var).pack(side = tk.LEFT)
            self.variables[var_name.strip()] = checkbox_var
        elif line.startswith('{') and line.endswith('}'):
            parts = line[1:-1].split(' : ')
            default_text, var_name, command = parts[0], parts[1], parts[2]
            entry_var = tk.StringVar()
            entry_var.set(default_text)
            entry = tk.Entry(root, textvariable=entry_var)
            entry.pack(side = tk.LEFT)
            entry.bind('<Return>', lambda event, cmd=command, var=entry_var: self.execute_command(cmd))
            self.variables[var_name.strip()] = entry_var
        elif line.startswith('|') and line.endswith('|'):
            text, var_name = line[1:-1].split(' : ')
            entry_var = tk.StringVar()
            entry_var.set(text)
            textbox = tk.Entry(root, textvariable=entry_var)
            textbox.pack(side = tk.LEFT)
            self.variables[var_name.strip()] = entry_var

        elif line.startswith('(') and line.endswith(')'):
            image_path = line[1:-1]
            img = tk.PhotoImage(file=image_path)
            self.images.append(img)  # Store reference to image object to prevent it from being garbage collected
            tk.Label(self.root, image=img).pack(side = tk.LEFT)
    def read_file(self, filename):
        self.variables = {}
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.exitwindow)
        self.images = []
        # Function to read the file and create GUI elements accordingly
        with open(filename, 'r') as file:
            window_title = file.readline().strip()[1:]
            self.root.title(window_title)

            for line in file:
                frame = tk.Frame(self.root)
                frame.pack(side = tk.TOP)
                for part in line.split(" & "):
                    self.doline(part.strip(), frame)

def tick(cnv, keepalive=[]):
    keepalive[0].tick(cnv)
def exec_command(cnv, in1, command, in2):
    if command == "closegui":
        try:
            in1[0].root.destroy()
        except:
            print("ERROR: invalid gui (line "+str(cnv.exec_line)+")")
            cnv.exec_running = False
    else:
        bui = gui()
        return bui.exec_command(cnv, in1, command, in2)