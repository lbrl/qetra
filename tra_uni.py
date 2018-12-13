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


class Tra:

    def __init__(self):
        self.n = 0
        self.fnames = []
        self.names = []
        self.titles = []
        self.ks = []
        self.initInd = 0
        self.traeff = -1.
        self.gg = []
        self.xx = []
        self.yy = []
        self.xmin = 0.
        self.xmax = 0.
        self.colours = [r.kRed, r.kBlue, r.kGreen+2,
               r.kViolet, r.kCyan, r.kMagenta,
                r.kYellow+2, r.kOrange+7]

    def add(self, fname, name='nonomo', title='notitolo', k=1., isInit=False, tipo='qe', yunuo='1'):
        self.fnames.append(fname)
        self.names.append(name)
        self.titles.append(title)
        self.ks.append(k)
        if isInit:
            self.initInd = self.n
        if tipo != 'qe':
            if tipo == 'radsens':
                if 'yunuo' == 'mA/W':
                    yunit = 1.e-3
                elif 'yunuo' == 'A/W':
                    yunit = 1.
                else:
                    print "Can't recognise units."
                    raise SystemError
                    return 1
            else:
                print "Can't recognise the type."
                raise SystemError
                return 1
        self.addGr(self.n)
        self.n += 1
        return 0

    # def getGr(self, f, name, k=1., colour=r.kRed, isProbability=False):
    def addGr(self, i):
        f = open(self.fnames[i])
        name = self.names[i]
        title = self.titles[i]
        k = self.ks[i]
        colour = self.colours[(i+1) % len(self.colours)]
        if i == self.initInd:
            isProbability = True
        else:
            isProbability = False
        x, y = [], []
        xy = []
        for line in f:
            lin = line.replace(',', '').split()
            li = [float(ltmp) for ltmp in lin]
            if len(li) == 2:
                xy.append( [li[0], k*li[1]] )
        xy = sorted(xy)
        for z in xy:
            x.append(z[0])
            y.append(z[1])
        if isProbability:
            gr_tmp = r.TGraph(len(x), np.array(x), np.array(y))
            hgr = r.TH1F('hgr_'+name, 'hgr '+name, int(x[-1]-x[0]), x[0], x[-1]+1)
            for i in xrange( int(x[-1]-x[0])):
                hgr.SetBinContent(i+1, gr_tmp.Eval(hgr.GetBinCenter(i+1)))
            integ = hgr.Integral()
            print 'The area under the curve (integral) : ', integ
        else:
            integ = 1.
        gr = r.TGraph(len(x), np.array(x), np.array(y)/integ)
        gr.SetName(name)
        # gr.SetTitle(title)
        gr.SetTitle('')
        gr.SetLineColor(colour)
        gr.SetMarkerColor(colour)
        gr.SetLineWidth(2)
        self.gg.append(gr)
        self.xx.append(x)
        self.yy.append(np.array(y)/integ)
        return 0

    def calcTra(self):
        #
        # print 'xx', self.xx
        xmin = [min(x) for x in self.xx]
        xmax = [max(x) for x in self.xx]
        self.xmin = max(xmin)
        self.xmax = min(xmax)
        # self.xmin = max([min(x) for x in self.xx])
        # self.xmax = min([max(x) for x in self.xx])
        print 'max min x', xmin, self.xmin
        print 'min max x', xmax, self.xmax
        #
        # for i, xcsi in enumerate(xcsitl):
        # for i, xcsi in enumerate(self.xx[self.initInd]):
        x, y = [], []
        for i, xcsi in enumerate(self.xx[self.initInd]):
            if xcsi < self.xmin:
                continue
            if xcsi > self.xmax:
                continue
            # print '%.2f < %.2f < %.2f' % (self.xmin, xcsi, self.xmax)
            ytmp = self.gg[0].Eval(xcsi)
            for g in self.gg[1:]:
                ytmp *= g.Eval(xcsi)
            # ytmp = ycsitl[i] * glens.Eval(xcsi) * gpco.Eval(xcsi) * gicf114.Eval(xcsi)
            if ytmp >= 0.:
                # print xcsi, ytmp
                x.append( xcsi )
                y.append( ytmp )
        # for i, xx in enumerate(x):
        #   print xx, y[i]
        gtra = r.TGraph(len(x), np.array(x), np.array(y))
        gtra.SetName('traeff')
        # gtra.SetTitle('transmission efficiency')
        gtra.SetTitle('')
        gtra.SetMarkerColor(r.kBlack)
        gtra.SetLineColor(r.kBlack)
        gtra.SetLineWidth(2)
        #
        htot = r.TH1F('htot', 'htot', int(max(x)-min(x)), min(x), max(x)+1)
        for i in xrange( int(x[-1]-x[0]) ):
            htot.SetBinContent(i+1, gtra.Eval(htot.GetBinCenter(i+1)))
        integ_tot = htot.Integral()
        print 'total integral', integ_tot
        #
        self.fnames.append('Total efficiency')
        self.names.append('Total efficiency')
        self.titles.append('Total efficiency')
        self.ks.append(1.)
        self.gg.append(gtra)
        self.xx.append(x)
        self.yy.append(y)
        self.traeff = integ_tot
        self.n += 1
        #
        return 0

    def getTotalEff(self):
        return self.traeff

    def draw(self, foutname='none'):
        c1 = r.TCanvas('c1', 'c1', 600, 600)
        c1.SetLogy()
        self.gg[0].Draw('al')
        self.gg[0].GetYaxis().SetRangeUser(min(self.yy[-1])/2., 2.)
        self.gg[0].GetYaxis().SetTitleOffset(1.2)
        self.gg[0].GetYaxis().SetTitle('Efficiency')
        self.gg[0].GetXaxis().SetTitle('Wave length, nm')
        for g in self.gg[1:]:
            g.Draw('l same')
        leg = r.TLegend(.7, .6, .99, .99)
        for i, g in enumerate(self.gg):
            leg.AddEntry(g, self.titles[i], 'l')
            # leg.AddEntry(g, g.GetTitle(), 'l')
        leg.Draw()
        lat = r.TLatex()
        lat.SetTextFont(12)
        lat.SetTextSize(.04)
        lat.DrawLatexNDC(.4, .2, 'Detection efficiency is %.2f%%.' % (100*self.traeff))
        c1.Update()
        raw_input('Press ENTER to continue, please.')
        if foutname != 'none':
            c1.SaveAs(foutname)
        return 0


def main():
    tra = Tra()
    tra.add('csi_tl_saint_gobaint.dat', 'csitl', 'CsI(Tl) emission', 1., True)
    tra.add('icf114vpk_kovar_glass.dat', 'icf114vpk_kovar_glass', 'Kovar glass trnsmssn eff.', 1.)
    tra.add('lens.dat', 'lens', 'Zeiss lens trnsmssn eff.', .01)
    tra.add('pco1600_w_ulenses.dat', 'pco', 'pco.1600 QE', .01)
    tra.calcTra()
    tra.draw()


def main2():
    tra = Tra()
    tra.add('csi_tl_saint_gobaint.dat', 'csitl', 'CsI(Tl) emission', 1., True)
    tra.add('qe_pmt.dat', 'pmt', 'PMT QE', .01)
    tra.calcTra()
    tra.draw('~/Downloads/csi_tl_pmt.png')


def main3():
    tra = Tra()
    # tra.add('csi_tl_saint_gobaint.dat', 'csitl', 'CsI emission', 1., True)
    tra.add('csi_tl_pdg.dat', 'csitl', 'CsI(Tl) emission', 1., True)
    tra.add('lens.dat', 'lens', 'Zeiss lens trnsmssn eff.', .01)
    tra.add('pco1600_w_ulenses.dat', 'pco', 'pco.1600 QE', .01)
    tra.calcTra()
    tra.draw('csi_tl_zeiss_pco1600.png')


def main4():
    tra = Tra()
    tra.add('csi_tl_saint_gobaint.dat', 'csitl', 'CsI(Tl) emission', 1., True)
    tra.add('qe_pmt_r2059.dat', 'pmt', 'PMT R2059 QE', .01)
    tra.calcTra()
    tra.draw('~/Downloads/csi_tl_pmt_r2059.png')


def main5():
    tra = Tra()
    tra.add('nai_tl_leo_1987.dat', 'naitl', 'NaI(Tl) emission', 1., True)
    tra.add('qe_pmt_r2059.dat', 'pmt', 'PMT R2059 QE', .01)
    tra.calcTra()
    tra.draw('~/Downloads/nai_tl_pmt_r2059.png')


def main6():
    tra = Tra()
    tra.add('nai_tl_leo_1987.dat', 'naitl', 'NaI(Tl) emission', 1., True)
    tra.add('qe_pmt_xp2282.dat', 'pmt', 'PMT XP2282 QE', .01)
    tra.calcTra()
    tra.draw('~/Downloads/nai_tl_pmt_xp2282.png')


if __name__ == '__main__':
    # main()
    # main2()
    # main3()
    main5()
    main6()
