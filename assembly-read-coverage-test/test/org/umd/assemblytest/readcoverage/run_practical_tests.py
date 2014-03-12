#!/usr/bin/python

'''
Created on Dec 8, 2013

@author: kzampog
'''

import os, subprocess, glob, shutil
# import sys

if __name__ == '__main__':
    os.chdir('../../../../../../practical_tests')
    test_dirs = os.listdir('.')
    test_dirs = [d for d in test_dirs if os.path.isdir(d)]
    for d in test_dirs:
        os.chdir('./' + d)
        # Clean-up
        shutil.rmtree('./out', ignore_errors=True)
        for f in glob.glob('*.fq'):
            os.remove(f)
        # Run clipper
        f = open('./clipper.args')
        clipper_args = [l for l in f][0].strip()
        f.close()
        clipper_cmd = 'python ../../assembly-read-coverage/org/umd/assemblytest/readcoverage/clipper.py ' + clipper_args
        clipper_stdout = open('clipper.stdout', 'w')
        subprocess.call(clipper_cmd, stdout=clipper_stdout, shell=True)
        clipper_stdout.close()
        for f in glob.glob('./out/*.bt2') + glob.glob('./out/*.sam') + glob.glob('./out/*.stderr') + glob.glob('./out/*.stdout'):
            os.remove(f)
        # Run pythia
        o_file = glob.glob('*.oracle')[0]
        m_file = glob.glob('./out/*_OVER_BP.cov')[0]
        # o_file = m_file
        pythia_cmd = 'python ../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/pythia.py -m ' + m_file + ' -o ' + o_file
        pythia_stdout = open('pythia.stdout', 'w')
        subprocess.call(pythia_cmd, stdout=pythia_stdout, shell=True)
        pythia_stdout.close()
        os.chdir('..')
