#! /usr/bin/env python

# Python imports
#import os, sys, argparse, getpass
from datetime import datetime
# User imports
from classes import *
import CombineHarvester.CombineTools.ch as ch
# ROOT imports
import ROOT
from ROOT import gROOT
from ROOT import TChain, TFile, TCanvas
from ROOT import TH1F
from cp3_llbb.ZATools.ZACnC import *

#gROOT.Reset()
#gROOT.SetBatch()
#ROOT.PyConfig.IgnoreCommandLineOptions = True

def main():
  options = options_()
  for cutkey in options.cut :
    print 'cutkey : ', cutkey
    ### get M_A and M_H ###
    mH = float(options.mH_list[cutkey])
    mA = float(options.mA_list[cutkey])
    print mH, mA

    """Main function"""
    # start the timer
    tstart = datetime.now()
    print 'starting...'
    # get the options
    #options = get_options()

    intL = options.lumi # in pb-1    
    #tag = 'v1.2.0+7415-19-g7bbca78_ZAAnalysis_1a69757'
    #path = '/nfs/scratch/fynu/amertens/cmssw/CMSSW_7_4_15/src/cp3_llbb/CommonTools/histFactory/16_01_28_syst/build'
    tag = 'v1.1.0+7415-83-g2a9f912_ZAAnalysis_2ff9261'
    #tag = 'v1.1.0+7415-57-g4bff5ea_ZAAnalysis_b1377a8'
    path = options.path 
    CHANNEL = options.CHANNEL
    ERA = options.ERA
    MASS = str(mH)+"_"+str(mA)
    ANALYSIS = options.ANALYSIS
    DEBUG = 0

    c = ch.CombineHarvester()
    cats = [(0, "mmbbSR"+cutkey),
            (1, "mll_mmbbBR"+cutkey),
            (2, "eebbSR"+cutkey),
            (3, "mll_eebbBR"+cutkey)
            ]

    bins = {}
    bins['signalregion_mm'] = "mmbbSR"+cutkey
    bins['mll_bkgregion_mm'] = "mll_mmbbBR"+cutkey
    bins['signalregion_ee'] = "eebbSR"+cutkey
    bins['mll_bkgregion_ee'] = "mll_eebbBR"+cutkey

    processes = {}
    p = Process('data_obs')
    #DoubleMuon_Run2015D_v1.1.0+7415-57-g4bff5ea_ZAAnalysis_b1377a8_histos.root
    p.prepare_process(path, 'data_obs', 'DoubleMuon_DoubleEG_Run2015D', tag)
    processes['data_obs'] = p
    if DEBUG: print p
    # define signal
    # define backgrounds
    # zz
    p = Process('zz')
    p.prepare_process(path, 'zz', 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_MiniAODv2', tag)
    processes['zz'] = p
    if DEBUG: print p

    # ttbar
    p = Process('ttbar')
    p.prepare_process(path, 'ttbar', 'TTTo2L2Nu_13TeV-powheg_MiniAODv2', tag)
    processes['ttbar'] = p
    p = Process('ttbar')
    if DEBUG: print p
    '''
    # drell-yan
    p = Process('dy1')
    p.prepare_process(path, 'dy1', 'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX_MiniAODv2', tag)
    processes['dy1'] = p
    if DEBUG: print p
    '''
    p = Process('dy2')
    p.prepare_process(path, 'dy2', 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX_MiniAODv2', tag)
    processes['dy2'] = p
    if DEBUG: print p



    c.AddObservations([MASS], [ANALYSIS], [ERA], [CHANNEL], cats)
    c.AddProcesses([MASS], [ANALYSIS], [ERA], [CHANNEL], ['ZA'], cats, True)
    c.AddProcesses([MASS], [ANALYSIS], [ERA], [CHANNEL], ['ttbar', 'dy2','zz'], cats, False)
    c.cp().process(['ttbar', 'dy2','ZA']).AddSyst(
        c, "lumi", "lnN", ch.SystMap('channel', 'era', 'bin_id')
        ([CHANNEL], [ERA],  [0,1,2,3], 1.046))

    c.cp().process(['ttbar', 'dy2','ZA']).AddSyst(
        c, "trig", "lnN", ch.SystMap('channel', 'era', 'bin_id')
        ([CHANNEL], [ERA],  [0,1,2,3], 1.04))

    c.cp().process(['ttbar', 'dy2']).AddSyst(
        c, "btag", "shape", ch.SystMap()(1.0))

    c.cp().process(['ttbar', 'dy2']).AddSyst(
        c, "jec", "shape", ch.SystMap()(1.0))

    c.cp().process(['ttbar', 'dy2']).AddSyst(
        c, "jer", "shape", ch.SystMap()(1.0))

    c.cp().process(['ttbar', 'dy2']).AddSyst(
        c, "pu", "shape", ch.SystMap()(1.0))

    c.cp().process(['ttbar']).AddSyst(
        c, "TTpdf", "shape", ch.SystMap()(1.0))

    c.cp().process(['dy2']).AddSyst(
        c, "DYpdf", "shape", ch.SystMap()(1.0)) 

    c.cp().process(['dy2']).AddSyst(
        c, "DYnorm", "lnN", ch.SystMap('channel', 'era', 'bin_id')
        ([CHANNEL], [ERA],  [0,1], 1.1))
    
    c.cp().process(['ttbar']).AddSyst(
        c, "TTnorm", "lnN", ch.SystMap('channel', 'era', 'bin_id')
        ([CHANNEL], [ERA],  [0], 1.1))


    nChannels = len(bins)
    nBackgrounds = len([processes[x] for x in processes if processes[x].type > 0])
    nNuisances = 1

    systematics = {'':'','_btagUp':'__btagup', '_btagDown':'__btagdown',
                         '_jecUp':'__jecup','_jecDown':'__jecdown',
                         '_jerUp':'__jerup','_jerDown':'__jerdown', 
                         '_puUp':'__puup', '_puDown':'__pudown',
                         '_TTpdfUp':'__pdfup','_TTpdfDown':'__pdfdown', '_DYpdfUp':'__pdfup','_DYpdfDown':'__pdfdown'}
    outputRoot = "shapes.root"
    f = TFile(outputRoot, "recreate")
    f.Close()
    for b in bins:
        print b , bins[b]
        for p in processes:
          if p == 'data_obs' :
            file_in = TFile(processes[p].file,"READ")
            print " Getting ", bins[b], " in file ", processes[p].file
            h = file_in.Get(bins[b])
            h.SetDirectory(0)
            file_in.Close()
            f = TFile(outputRoot, "update")
            h.SetName("hist_"+bins[b]+"_"+p)
            h.Write()
            f.Write()
            f.Close()


          else :
            for s1,s2 in systematics.iteritems() :
              file_in = TFile(processes[p].file,"READ")
              print " Getting ", bins[b]+s2, " in file ", processes[p].file
              h = file_in.Get(bins[b]+s2)
              h.SetDirectory(0)
              file_in.Close()
              f = TFile(outputRoot, "update")
              h.SetName("hist_"+bins[b]+"_"+p+s1)
              h.Sumw2()
              #h.Scale(processes[p].xsection * intL / processes[p].sumW)
              h.Scale(intL)
              h.Write()
              f.Write()
              f.Close()



    # Fill signal histograms FIXME: read efficiencies from eff.root
    
    eff_file = TFile("eff.root", "READ")
    effee_hist = eff_file.Get("effee")
    eff_ee = effee_hist.Interpolate(mA,mH)
    effmm_hist = eff_file.Get("effmm")
    eff_mm = effmm_hist.Interpolate(mA,mH)

    print "lumi : ", options.lumifb
    print "eff at ", mA, mH, ":", eff_ee, eff_mm
    print "ZA yields: ", options.lumifb*eff_mm, options.lumifb*eff_ee
    

    f = TFile(outputRoot, "update")
    h1 = TH1F("hist_"+bins['signalregion_mm']+"_ZA","hist_"+bins['signalregion_mm']+"_ZA",1,0,1)
    h1.Fill(0.5,options.lumifb*eff_mm)
    h1.Write()
    
    h2 = TH1F("hist_"+bins['mll_bkgregion_mm']+"_ZA","hist_"+bins['mll_bkgregion_mm']+"_ZA",60,60,120)
    h2.Write()

    h3 = TH1F("hist_"+bins['signalregion_ee']+"_ZA","hist_"+bins['signalregion_ee']+"_ZA",1,0,1)
    h3.Fill(0.5,options.lumifb*eff_ee)
    h3.Write()

    h4 = TH1F("hist_"+bins['mll_bkgregion_ee']+"_ZA","hist_"+bins['mll_bkgregion_ee']+"_ZA",60,60,120)
    h4.Write()


    f.Write()
    f.Close()

    c.cp().backgrounds().ExtractShapes(
        outputRoot, "hist_$BIN_$PROCESS", "hist_$BIN_$PROCESS_$SYSTEMATIC")
    c.cp().signals().ExtractShapes(
        outputRoot, "hist_$BIN_$PROCESS", "hist_$BIN_$PROCESS_$SYSTEMATIC")
    writer = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$CHANNEL_$ERA.dat',
                   '$TAG/common/$ANALYSIS_$CHANNEL_$MASS.input_$ERA.root')
    writer.WriteCards('CARDS/', c)

#
# main
#
if __name__ == '__main__':
    main()
