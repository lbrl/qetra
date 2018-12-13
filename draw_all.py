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

import tra_uni


def main():
    tra = tra_uni.Tra()
    tra.add('qe_pmt_r2059.dat', 'pmt_r2059', 'PMT R2059 QE', .01, False)
    tra.add('qe_pmt_xp2282.dat', 'pmt_xp2282', 'PMT XP2282 QE', .01)
    tra.add('qe_pmt.dat', 'pmt_', 'PMT R1847S QE', .01, False)
    tra.add('nai_tl_leo_1987.dat', 'naitl', 'NaI(Tl) Leo 1987', 1., tipo='emission')
    tra.add('csi_tl_saint_gobaint.dat', 'csitl', 'CsI(Tl) Saint Gobaint', 1., tipo='emission')
    tra.add('csi_tl_pdg.dat', 'csitl', 'CsI(Tl) PDG', 1., tipo='emission')
    tra.draw(logy=0, print_qe=False, ymax=.35)


if __name__ == '__main__':
    main()
