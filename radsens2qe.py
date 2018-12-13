#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import os
import ROOT as r
import numpy as np
# import re
import sys
# import glob
import math
# import datetime as dt
# from array import array
# import subprocess as sp
# import time
# import random as rm

def getGr(finname):
    k = .1
    f = open( finname )
    x, y = [], []
    xy = []
    for line in f:
        lin = line.replace(',', '').split()
        li = [float(ltmp) for ltmp in lin]
        if len(li) == 2:
            xy.append( [li[0], li[1]] )
    xy = sorted(xy)
    for z in xy:
        x.append(z[0])
        y.append(z[1] * k * 1240. / z[0] * 100)
    gr = r.TGraph(len(x), np.array(x), np.array(y))
    gr.SetTitle('')
    gr.SetLineWidth(2)
    return [gr, x, y]


def main():
    finname = 'rad_sens_pmt_xp2282.dat'
    foutname = 'qe_pmt_xp2282.dat'
    gr = getGr( finname )
    gr[0].Draw( 'alp' )
    raw_input()
    fout = open( foutname, 'w' )
    for i in xrange( len(gr[1]) ):
        fout.write( '{}, {}\n'.format( gr[1][i], gr[2][i] ) )
    fout.close()


if __name__ == '__main__':
    main()
