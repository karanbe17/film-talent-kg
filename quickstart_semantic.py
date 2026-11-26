"""Create an isolated virtual environment, install dependencies and launch the local app."""
from pathlib import Path
import argparse, os, subprocess, sys, venv
ROOT=Path(__file__).resolve().parent
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--virtuoso',action='store_true'); p.add_argument('--reset',action='store_true',help='replace the working graph with the sample'); p.add_argument('--port',type=int,default=8000); a=p.parse_args()
 env=ROOT/'.venv'; interpreter=env/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
 if not interpreter.exists(): venv.EnvBuilder(with_pip=True).create(env)
 subprocess.check_call([str(interpreter),'-m','pip','install','-r',str(ROOT/'requirements-semantic.txt')],cwd=ROOT)
 args=[str(interpreter),str(ROOT/'semantic_main.py'),'--port',str(a.port)]
 if a.reset:args.append('--reset')
 if a.virtuoso:args.append('--virtuoso')
 subprocess.call(args,cwd=ROOT)
