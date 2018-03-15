#-----------------------------------------------------------------------------#
#
# Strategic voting (Cox 1994)
#
# Authors: Fabricio Vasselai & Samuel Baltz
#
# Purpose: To replicate Cox 1994 SNTV as an ABM
#
# Last modified: 15 March 2018
#
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
# Import libraries:
#-----------------------------------------------------------------------------#
import sys
import numpy as np
from scipy.stats import skellam

seed = np.random.randint(0,2**32 - 1)
print "Seed: " + str(seed) + "\n"
np.random.seed(seed)


from Elector import Elector
from Candidate import Candidate
import GlobalFuncs

#-----------------------------------------------------------------------------#
# Environmental or global variables
#-----------------------------------------------------------------------------#

#Initialize parameters:
nElectors = 100 #Number of electors
nCandidates = 4 #Number of candidates
minPreference = 0 #min value of 1-D preference of electors and candidates
maxPreference = 100 #max value of 1-D preference of electors and candidates
allElectors = [None] * nElectors #list that stores the electors
allCandidates = [None] * nCandidates #list that stores the candidates
leastCandidates = [0] * nCandidates 
MIN_UTIL = -10**10
MAX_ITERATION = 100


#-----------------------------------------------------------------------------#
# Populating the world:
#-----------------------------------------------------------------------------#

#Generate candidates:
for newCandidateID in range(0, nCandidates):
    cand = Candidate(newCandidateID)
    allCandidates[newCandidateID] = cand

#Generate electors:
for newElectorID in range(0, nElectors):
    elector = Elector(newElectorID, nCandidates)
    elector.calcSincereUtilities(allCandidates, minPreference,                \
                                 maxPreference, "uniform")
    allElectors[newElectorID] = elector

#print "Least preferred by: ",
#GlobalFuncs.plotLeastCandidates(leastCandidates, allElectors, allCandidates)
#print "\n"


#-----------------------------------------------------------------------------#
# Main simulation loop:
#-----------------------------------------------------------------------------#

lastVoteIntentions = [None] * nCandidates
currentVoteIntentions = [None] * nCandidates
iter = 0 #iteration counter

#Loop until convergence is met, i.e. in this simplistic version = when nothing
#changes from one iteration to the next:
while not GlobalFuncs.areIdentical(lastVoteIntentions, currentVoteIntentions) \
      or iter <= 1:

    lastVoteIntentions = currentVoteIntentions
    
    #Update strategic utility considerations of electors, given the current
    #winning probabilities of candidates:
    for elector in allElectors:
        elector.calculateStrategicUtilities(allCandidates,allElectors,MIN_UTIL,iter)

    #count the vote intention of all electors towards all candidates for the
    #current iterations:
    currentVoteIntentions = GlobalFuncs.countVoteIntentions(allElectors,      \
                                                        allCandidates,iter)            

#    for elector in allElectors:
#        if elector.ID == 0:
#            print "iteration: " + str(iter)
#            print "all votes: " + str(elector.allVotes)

    #Show vote intention shares in the first iteration:
    if iter == 0:
        GlobalFuncs.printElectResultsAsOfNow(allCandidates, nElectors)
    
    iter += 1
   
#Show vote intention shares after convergence:
GlobalFuncs.printElectResultsAsOfNow(allCandidates, nElectors)
        
print "Converged after " + str(iter - 1) + " iterations."
                             
#-----------------------------------------------------------------------------#
# End of file
#-----------------------------------------------------------------------------#
