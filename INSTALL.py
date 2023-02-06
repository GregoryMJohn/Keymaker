#!/usr/bin/env python3

import sys
import os
import subprocess

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

for pkg in ['alive_progress','str2bool']:
        if not pkg in installed_packages:
                subprocess.run(f'yes | python3 -m pip install {pkg}', shell=True)

os.system("git clone https://github.com/nightblade9/simple-english-dictionary.git")
os.system("mv ./simple-english-dictionary/data/ .") 
os.system("sudo rm -R simple-english-dictionary/")
os.system('chmod 755 *.py')
cwd = os.getcwd()
subprocess.run('echo "#Keymaker" | sudo tee -a ~/.bashrc', shell=True)
subprocess.run(f'echo \'export PATH="{cwd}:$PATH"\' | sudo tee -a ~/.bashrc', shell=True)
os.system("touch tmp_script.sh")
os.system("chmod 777 tmp_script.sh")
with open("tmp_script.sh","w") as fh:
        fh.write("#!/bin/bash \n")
        fh.write("source ~/.bashrc")

subprocess.run("./tmp_script.sh")
os.remove("tmp_script.sh")
