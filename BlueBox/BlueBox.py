import click
import conveyor
import os
import json
import random
@click.command()
@click.option('-s', '--standalone', type=str, help="Executes conveyor file outside of a BlueBox instance")
@click.option('-e', '--exec', type=str, help="Executes conveyor file inside of a BlueBox instance")
@click.option('-i', '--instance', is_flag=True, help="Initalize a new BlueBox instance")
@click.option('-c', '--close', is_flag=True, help="Close the current BlueBox instance")

def main(standalone, exec, instance, close):
    if instance:
        with open('BlueBox/instances/bbi.json', 'w') as f:
            json.dump({"requests":[], "session id":random.randrange(10000, 99999)}, f)
    elif close:
        os.remove('BlueBox/instances/bbi.json')
    elif standalone:
        cnv = conveyor.cnv()
        cnv.execFile(standalone)
    elif exec:
        cnv = conveyor.cnv()
        with open('BlueBox/instances/bbi.json', 'r') as f:
            cnv.bb_sid = json.load(f)["session id"]
        cnv.execFile(standalone)
if __name__ == "__main__":
    main()