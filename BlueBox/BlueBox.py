import click
import conveyor
import os
import json
import random
import pathlib

@click.command()
@click.option('-s', '--standalone', type=str, help="Executes conveyor file outside of a BlueBox instance")
@click.option('-e', '--exec', type=str, help="Executes conveyor file inside of a BlueBox instance")
@click.option('-i', '--instance', is_flag=True, help="Initalize a new BlueBox instance")
@click.option('-c', '--close', is_flag=True, help="Close the current BlueBox instance")

def main(standalone, exec, instance, close):
    inpath = str(pathlib.Path(__file__).parent.resolve())+'\\instances\\bbi.json'
    if instance:
        with open(inpath, 'w') as f:
            json.dump({"requests":[], "session id":random.randrange(10000, 99999)}, f)
    elif close:
        os.remove(inpath)
    elif standalone:
        cnv = conveyor.cnv()
        cnv.execFile(standalone)
    elif exec:
        cnv = conveyor.cnv()
        with open(inpath, 'r') as f:
            cnv.bb_sid = json.load(f)["session id"]
        cnv.execFile(exec)
if __name__ == "__main__":
    main()