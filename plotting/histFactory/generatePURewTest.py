from cp3_llbb.ZATools.ZACnC import *

def printInPyWithSyst(f, g, name = '', variable = '', cut = '', weight = '', binning = '', writeInPlotIt = 0):
    f.write( "        {\n")
    f.write( "        'name': '"+name+"',\n")
    f.write( "        'variable': '"+variable+"',\n")
    f.write( "        'plot_cut': '"+cut+"',\n")
    f.write( "        'weight': '"+weight+"',\n")
    f.write( "        'binning': '"+binning+"'\n")
    f.write( "        },\n")
    if writeInPlotIt == 1 :
      g.write("'"+name+"':\n")
      g.write("  x-axis: '"+name+"'\n")
      g.write("  y-axis: 'Evt'\n")
      g.write("  y-axis-format: '%1% / %2$.0f GeV'\n")
      g.write("  normalized: false\n")
      g.write("  log-y: both\n")
      g.write("  save-extensions: ['png','pdf']\n")
      g.write("  show-ratio: true\n")

# binnings

nPV_binning = "(35,0,35)"
mll_binning = "(30,60,120)"

# mll

mll = "za_diLeptons[0].p4.M()"
mllName = "mll"

# PV N

nPV = "vertex_ndof.size()"
nPVName = "nVX"

# Cuts


ll_weights = "( event_run < 200000 ? (za_diLeptons[0].triggerSF * event_pu_weight * event_weight) : 1.)"

twoLCond = []
twoLCondName = []
twoLCond.append("za_mumu_Mll_cut")
twoLCond.append("za_elel_Mll_cut")
twoLCond.append("(za_mumu_Mll_cut ||  za_elel_Mll_cut)")
twoLCond.append("(za_muel_Mll_cut ||  za_elmu_Mll_cut)")
twoLCondName.append("mm")
twoLCondName.append("ee")
twoLCondName.append("ll")
twoLCondName.append("me")

twoLtwoJCond = []
twoLtwoJCondName = []
twoLtwoBCond = []
twoLtwoBCondName = []
twoLthreeBCond = []
twoLthreeBCondName = []
twoLtwoSubJCond = []
twoLtwoSubJCondName = []
twoLOneBFatJetTCond = []
twoLOneBFatJetTCondName = []
twoLTwoBSubJetsLLCond = []
twoLTwoBSubJetsLLCondName = []
twoLTwoBSubJetsMMCond = []
twoLTwoBSubJetsMMCondName = []
twoLTwoBHighMassCond = []
twoLTwoBHighMassCondName = []

basicJcond="(elel_TwoJets_cut || mumu_TwoJets_cut || muel_TwoJets_cut || elmu_TwoJets_cut)"
basicTwoBcond="(Length$(za_diJets) > 0) && ((elel_TwoBjets_cut || mumu_TwoBjets_cut || muel_TwoBjets_cut || elmu_TwoBjets_cut) "
basicThreeBcond="(elel_ThreeBjets_cut || mumu_ThreeBjets_cut || muel_ThreeBjets_cut || elmu_ThreeBjets_cut)"
basicSubJcond="(elel_TwoSubJets_cut || mumu_TwoSubJets_cut || muel_TwoSubJets_cut || elmu_TwoSubJets_cut)"
basicOneBFatJetTcond="((elel_OneBFatJetT_cut || mumu_OneBFatJetT_cut || muel_OneBFatJetT_cut || elmu_OneBFatJetT_cut) && (Length$(za_diLepFatJets) > 0))"
#basicOneBFatJetTcond="(Length$(za_diLepFatJets) > 0)"
basicTwoBSubJetsLLcond="(elel_TwoBSubJetsLL_cut || mumu_TwoBSubJetsLL_cut )"
basicTwoBSubJetsMMcond="(elel_TwoSubJetsMM_cut || mumu_TwoSubJetsMM_cut || muel_TwoSubJetsMM_cut || elmu_TwoSubJetsMM_cut)"
basictwoLTwoBHighMasscond="(Length$(za_diJets) > 0 && Length$(za_diLeptons) > 0 && za_diJets[0].p4.Pt() > 200 && za_diLeptons[0].p4.Pt() > 200)"
basicJcondName="jj"
basicTwoBcondName="bb"
basicThreeBcondName="bbb"
basicSubJcondName="fj"
basicOneBFatJetTcondName="bfj"
basicTwoBSubJetsLLcondName="sbjsbj"
basictwoLTwoBHighMasscondName="highmass"

for x in range(0,4):
	twoLtwoJCond.append("("+twoLCond[x]+" && "+basicJcond+")")
	twoLtwoBCond.append("("+twoLCond[x]+" && "+basicTwoBcond+")")
	twoLthreeBCond.append("("+twoLCond[x]+" && "+basicThreeBcond+")")
	twoLtwoSubJCond.append("("+twoLCond[x]+" && "+basicSubJcond+")")
	twoLOneBFatJetTCond.append("("+twoLCond[x]+" && "+basicOneBFatJetTcond+")")
	twoLTwoBSubJetsLLCond.append("("+twoLCond[x]+" && "+basicTwoBSubJetsLLcond+")")
	twoLTwoBHighMassCond.append("("+twoLCond[x]+" && "+basictwoLTwoBHighMasscond+")")
	twoLtwoJCondName.append(twoLCondName[x]+basicJcondName)
	twoLtwoBCondName.append(twoLCondName[x]+basicTwoBcondName)
        twoLthreeBCondName.append(twoLCondName[x]+basicThreeBcondName)
	twoLtwoSubJCondName.append(twoLCondName[x]+basicSubJcondName)
	twoLOneBFatJetTCondName.append(twoLCondName[x]+basicOneBFatJetTcondName)
        twoLTwoBSubJetsLLCondName.append(twoLCondName[x]+basicTwoBcondName+basicTwoBSubJetsLLcondName)
	twoLTwoBHighMassCondName.append(twoLCondName[x]+basicTwoBcondName+basictwoLTwoBHighMasscondName)
	print twoLtwoJCond[x]


#test_highMass_cond = "(Length$(za_diJets) > 0 && Length$(za_diLeptons) > 0 && za_diJets[0].p4.Pt() > 200 && za_diLeptons[0].p4.Pt() > 200)"
#test_highMass =  twoL_cond + " * " + twoB_cond + " * " + test_highMass_cond + weights
#test_highMassName = "highPt"


# Writing the JSON

## 2 Muons 2 Jets :

fjson = open('plots_test.py', 'w')
fjson.write( "plots = [\n")
fyml = open('plots_test.yml', 'w')

'''
weights = "event_pu_weight * event_weight"
weights_puup = "event_pu_weight_up * event_weight"
weights_pudown = "event_pu_weight_down * event_weight"
za_diLeptons[0].triggerSF
* (jet_sf_csvv2_medium[za_diJets[0].idxJet1][0] * jet_sf_csvv2_medium[za_diJets[0].idxJet2][0] ))
'''

weights = "event_pu_weight * event_weight"
weights_puup = "event_pu_weight_up * event_weight"
weights_pudown = "event_pu_weight_down * event_weight"

llTrigSF = "(event_is_data !=1 ?( za_diLeptons[0].triggerSF * event_pu_weight * event_weight) : 1.0)"

btagSF = "(jet_sf_csvv2_medium[za_diJets[0].idxJet1][0] * jet_sf_csvv2_medium[za_diJets[0].idxJet2][0] )"
btagSFup = "(jet_sf_csvv2_medium[za_diJets[0].idxJet1][1] * jet_sf_csvv2_medium[za_diJets[0].idxJet2][1] )"
btagSFdown = "(jet_sf_csvv2_medium[za_diJets[0].idxJet1][2] * jet_sf_csvv2_medium[za_diJets[0].idxJet2][2] )"

llweights = {'': llTrigSF+'*'+btagSF+'*'+weights,
             '__puup': llTrigSF+'*'+btagSF+'*'+weights_puup,
             '__pudown': llTrigSF+'*'+btagSF+'*'+weights_pudown,
             '__btagup': llTrigSF+'*'+btagSFup+'*'+weights,
	     '__btagdown': llTrigSF+'*'+btagSFdown+'*'+weights
    }


## Plots for combine

options = options_()

for x in range(0,1):
    for cutkey in options.cut :
        for s,w in llweights.iteritems() :
            print 'cutkey : ', cutkey
            ### get M_A and M_H ###
            #mH[0] = float(options.mH_list[cutkey])
            #mA[0] = float(options.mA_list[cutkey])

            ### SIGNAL Region ###
            printInPyWithSyst(fjson, fyml, 
                    name = twoLtwoBCondName[x]+"SR"+cutkey+s, 
                    variable = '0.5', 
                    cut = options.cut[cutkey]+" && "+twoLtwoBCond[0]+" )", 
                    weight = w, 
                    binning = "(1,0,1)", 
                    writeInPlotIt = (1 if s==''  else 0)
                    )
            ### BACKGROUND Region ###
            printInPyWithSyst(fjson, fyml, 
                    name = mllName+'_'+twoLtwoBCondName[x]+"BR"+cutkey+s, 
                    variable = mll, 
                    cut = "!"+options.cut[cutkey]+" && "+twoLtwoBCond[0]+" )", 
                    weight = w, 
                    binning = mll_binning, 
                    writeInPlotIt = (1 if s==''  else 0)
                    )

## Control Plots :

for x in range(0,1):
    for s,w in llweights.iteritems() : 
	print x, s, w 
	#printInJsonNoVar(fjson, fyml, nPV, nPVName, twoLCond[x]+weights, twoLCondName[x], nPV_binning, 0)
        printInPyWithSyst(fjson, fyml, name=nPVName+'_'+twoLCondName[x]+s, variable=nPV, cut=twoLCond[x], weight=w, binning=nPV_binning, writeInPlotIt= (1 if s==''  else 0))
        #printInPyWithSyst(f, g, name = '', variable = '', cut = '', weight = '', binning = '', isLastEntry=0):

fjson.write( "        ]\n")

