import click
import conveyor
@click.command()
@click.option('-s', '--standalone', type=str, help="Executes conveyor file outside of a BlueBox instance")
@click.option('-e', '--exec', type=str, help="Executes conveyor file inside of a BlueBox instance")
def main(standalone, exec):
    if standalone:
        cnv = conveyor.cnv()
        cnv.execFile(standalone)
if __name__ == "__main__":
    main()