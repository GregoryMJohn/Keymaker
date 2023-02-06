#!/usr/bin/env python3

import sys
import os
import subprocess

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

for pkg in ['alive_progress','str2bool']:
	if not pkg in installed_packages:
		cmd = subprocess.Popen('yes', stdout=subprocess.PIPE)
		subprocess.run(f'python3 -m pip install {pkg}',stdin=cmd.stdout)
		cmd.wait()

subprocess.run("git clone https://github.com/nightblade9/simple-english-dictionary.git")
subprocess.run("mv ./simple-english-dictionary/data/ .") 
subprocess.run("sudo rm -R simple-english-dictionary/")
subprocess.run('chmod 755 *.py')
tee = subprocess.Popen('pwd',stdout=subprocess.PIPE)
subprocess.run('sudo tee -a ~/.bashrc', stdin=tee.stdout)
tee.wait()
