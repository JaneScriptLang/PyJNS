import parse
import json
import typer
import subprocess
import os
import sys
import functools

def main(file: str, transpile:bool=typer.Option(False, "-T", "--transpile-only"), cwd: str = typer.Option(os.getcwd(), "-cwd","--workdir", "-D"), noexec: bool = typer.Option(False, "--noexec","--compiler-mode", "-C", is_eager=True)):
    os.chdir(cwd)
    with open(file) as f:
        parse.Parser(f.read())
        if not noexec:
            subprocess.call([sys.executable, "outs.py"])
        if not transpile:
            os.remove("outs.py")
    sys.exit(0)

if __name__ == "__main__":
    typer.run(main)