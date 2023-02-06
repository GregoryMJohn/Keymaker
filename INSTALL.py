#!/usr/bin/env python3

import sys
import os
import subprocess

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

for pkg in ['alive_progress','str2bool']:
	if not pkg in installed_packages:
		os.system(f'yes | python3 -m pip install {pkg}')

os.system("git clone https://github.com/nightblade9/simple-english-dictionary.git .")
os.system("mv ./simple-english-dictionary/data/ .") 
os.system("yes | rm -R simple-english-dictionary/")
