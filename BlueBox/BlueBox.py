import click
import conveyor
@click.command()
@click.option('-s', '--standalone', type=str, help="Executes conveyor file outside of a BlueBox intance")
@click.option('-e', '--exec', type=str, help="Executes conveyor file inside of a BlueBox intance")
def main(standalone, exec):
    if standalone:
        cnv = conveyor.cnv()
        cnv.execFile(standalone)
if __name__ == "__main__":
    main()