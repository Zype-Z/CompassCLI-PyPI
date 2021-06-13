#!/usr/bin/env python3
import sys
import os
import ZypeSDK as zsdk
import glob
import json
from rich import print
from rich.progress import track
from time import sleep
from rich.console import Console
from rich.traceback import install
from rich.syntax import Syntax
from rich.pretty import Pretty
from rich import pretty
from compasscli import __version__

def main():
    pretty.install()

    install()

    console = Console()

    arg = sys.argv

    os.chdir(os.getcwd())

    results = glob.glob('*.zype')

    try:
        if arg[1] == '--version' or arg[1] == '-v':
            print("Compass CLI [bold u cyan]v{}[/bold u cyan]".format(__version__))

        elif arg[1] == '--search' or arg[1] == '-s':
            for step in track(range(100), description="[cyan]Searching File(s)[/cyan]...."):
                sleep(0.001)

            sl = len(results)

            for step in track(range(100), description="[red]Compiling File(s)[/red]...."):
                sleep(0.001)

            print("Found [bold]{sl}[/bold] Files\n".format(sl=sl))

            for result in results:
                console.print("[h1][u cyan]{result}[/u cyan][/h1]\n".format(result=result), justify="center")
                print("{content}\n".format(content=json.dumps(zsdk.Open(result), indent=2)).replace('true', "[i violet]True[/i violet]").replace('false', "[i red]False[/i red]"))

        else:
            if os.path.isfile(arg[1]):
                try:
                    prefile = zsdk.Open(arg[1])
                    include = prefile['$include']
                    for files in include:
                        if os.path.isfile("{}.z".format(files)):
                            print(json.dumps(zsdk.Open('{}.z'.format(files)), indent=2))
                        else:
                            print("No such file to Include: {}".format("{}.z".format(files)))
                    prefile['$include'] = None
                except KeyError:
                    pass
                try:
                    if arg[2] == '--cache' or arg[2] == '-c':
                        for step in track(range(100), description="Compiling File(s)"):
                            sleep(0.001)
                        if not os.path.isdir('cache'):
                            os.mkdir('cache')
                        cache = 'cache'
                        with open(os.path.join(os.getcwd(), '{}'.format(os.path.join(cache, arg[1].replace('.zype', '.json')))), 'w') as Cache:
                            Content = json.dumps(zsdk.Open(arg[1]), indent=2)
                            Cache.write(Content)
                        cache = 'cache'
                        if os.path.isfile(os.path.join(cache, arg[1].replace('.zype', '.json'))):
                            with open(os.path.join(os.getcwd(), '{}'.format(os.path.join(cache, arg[1].replace('.zype', '.json')))), 'r') as CacheFile:
                                print(json.dumps(json.loads(CacheFile.read()), indent=2).replace('true', "[i violet]True[/i violet]").replace('false', "[i red]False[/i red]"))
                except IndexError:
                    print(json.dumps(zsdk.Open(arg[1]), indent=2).replace('true', "[i violet]True[/i violet]").replace('false', "[i red]False[/i red]"))
            else:
                print("[red]Compass[/red]: No such Zype File: {filename}".format(filename=arg[1]))
    except IndexError:
        print("[red]Compass[/red]: No Arguments given.")

if __name__=="__main__":
    main()
