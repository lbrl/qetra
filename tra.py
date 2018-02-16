#! /usr/bin/env python

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


def getGr(f, name, k=1., colour=r.kRed, isProbability=False):
    x, y = [], []
    xy = []
    for line in f:
        lin = line.replace(',', '').split()
        li = [float(ltmp) for ltmp in lin]
        # print li
        if len(li) == 2:
            # x.append(li[0])
            # y.append(k*li[1])
            xy.append( [li[0], k*li[1]] )
    xy = sorted(xy)
    for z in xy:
        x.append(z[0])
        y.append(z[1])
    # print 'x', x
    # print 'y', y
    if isProbability:
        gr_tmp = r.TGraph(len(x), np.array(x), np.array(y))
        '''
        class fgr
        def fgr(xx, pp):
            return gr.Eval(xx[0])
        fgr = r.TF1('f'+name, fgr, x[0], x[-1], 0)
        print fgr.Eval(x[1])
        integ = fgr.Integral(x[0], x[-1])
        gr = r.TGraph(len(x), np.array(x)/integ, np.array(y)/integ)
        '''
        '''
        x.insert(0, x[0])
        y.insert(0, 0.)
        x.append(x[-1])
        y.append(0.)
        gr = r.TGraph(len(x), np.array(x), np.array(y))
        integ = gr.Integral()
        print 'integral', integ
        '''
        hgr = r.TH1F('hgr_'+name, 'hgr '+name, int(x[-1]-x[0]), x[0], x[-1]+1)
        for i in xrange( int(x[-1]-x[0])):
            hgr.SetBinContent(i+1, gr_tmp.Eval(hgr.GetBinCenter(i+1)))
        integ = hgr.Integral()
        print 'integral', integ
        '''
        c2 = r.TCanvas('c2', 'c2', 600, 600)
        hgr.Draw()
        gr_tmp.SetMarkerStyle(7)
        gr_tmp.SetMarkerColor(r.kRed)
        gr.SetMarkerStyle(24)
        gr.SetMarkerColor(r.kBlue)
        gr_tmp.Draw('p same')
        gr.Draw('p same')
        c2.Update()
        raw_input()
        '''
    else:
        integ = 1.
    gr = r.TGraph(len(x), np.array(x), np.array(y)/integ)
    gr.SetName(name)
    gr.SetTitle('')
    gr.SetLineColor(colour)
    gr.SetMarkerColor(colour)
    gr.SetLineWidth(2)
    return gr, x, np.array(y)/integ


def main():
    fpco = open('pco1600_w_ulenses.dat')
    fcsitl = open('csi_tl_saint_gobaint.dat')
    flens = open('lens.dat')
    ficf114 = open('icf114vpk_kovar_glass.dat')
    glens, xlens, ylens = getGr(flens, 'lens', .01)
    gcsitl, xcsitl, ycsitl = getGr(fcsitl, 'csitl', 1., r.kBlue, True)
    gpco, xpco, ypco = getGr(fpco, 'pco', .01, r.kGreen)
    gicf114, xicf114, yicf114 = getGr(ficf114, 'icf114vpk_kovar_glass', 1., r.kMagenta)
    #
    x, y = [], []
    for i, xcsi in enumerate(xcsitl):
        # print glens.Eval(xcsi), gpco.Eval(xcsi)
        # y.append( ycsitl[i] * glens.Eval(xcsi) * gpco.Eval(xcsi) )
        # y.append( ycsitl[i] * glens.Eval(xcsi) * gpco.Eval(xcsi) * gicf114.Eval(xcsi) )
        ytmp = ycsitl[i] * glens.Eval(xcsi) * gpco.Eval(xcsi) * gicf114.Eval(xcsi)
        if ytmp >= 0. :
            x.append( xcsi )
            y.append( ytmp )
    # gtra = r.TGraph(len(xcsitl), np.array(xcsitl), np.array(y))
    gtra = r.TGraph(len(x), np.array(x), np.array(y))
    gtra.SetName('traeff')
    gtra.SetTitle('transmission efficiency')
    gtra.SetMarkerColor(r.kViolet)
    gtra.SetLineColor(r.kViolet)
    gtra.SetLineWidth(2)
    #
    htot = r.TH1F('htot', 'htot', int(x[-1]-x[0]), x[0], x[-1]+1)
    for i in xrange( int(x[-1]-x[0])):
        htot.SetBinContent(i+1, gtra.Eval(htot.GetBinCenter(i+1)))
    integ_tot = htot.Integral()
    print 'total integral', integ_tot
    #
    c1 = r.TCanvas('c1', 'c1', 800, 800)
    glens.Draw('alp')
    glens.GetYaxis().SetRangeUser(0, 1)
    glens.GetYaxis().SetTitleOffset(1.2)
    glens.GetYaxis().SetTitle('Efficiency')
    glens.GetXaxis().SetTitle('Wave length, nm')
    gpco.Draw('pl same')
    gicf114.Draw('pl same')
    gcsitl.Draw('pl same')
    gtra.Draw('pl same')
    #
    fp0 = r.TF1('fp0', 'pol0(0)', 350, 720)
    fp0.SetParameter(0, .2)
    fp0.SetLineColor(r.kViolet)
    fp0.SetLineWidth(3)
    gtra.Fit(fp0, 'r', 'same')
    #
    leg = r.TLegend(.7, .4, .99, .8)
    leg.AddEntry(gcsitl, 'CsI emission', 'l')
    leg.AddEntry(gicf114, 'Kovar glass transmission eff.', 'l')
    leg.AddEntry(glens, 'Lens transmission eff.', 'l')
    leg.AddEntry(gpco, 'pco.1600 QE', 'l')
    leg.AddEntry(gtra, 'Total eff.', 'l')
    leg.AddEntry(fp0, 'Avr. total eff.', 'l')
    leg.Draw()
    #
    lat = r.TLatex()
    lat.SetTextColor(r.kViolet)
    p0 = fp0.GetParameter(0)
    p0err = fp0.GetParError(0)
    lat.DrawLatex(350, p0+.02, '%.3f #pm %.3f' % (p0, p0err))
    #
    c1.Update()
    raw_input()
    c1.SaveAs('transmission_eff.png')


if __name__ == '__main__':
    main()
