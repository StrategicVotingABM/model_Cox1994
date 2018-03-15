#-----------------------------------------------------------------------------#
# Elector-owned Variables:
#    ID: an unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    strategicUtilities: a list with the elector's sincere expectation for each
#                        candidate
#-----------------------------------------------------------------------------#

import GlobalFuncs
import numpy as np
from scipy.stats import skellam
import math

class Elector:
    
    #overload of class constructor, that initializes elector-owned variables
    def __init__(self, passedID, nCandidates):
        self.ID = passedID
        self.strategicUtilities = [None] * nCandidates
        self.sincereUtilities = [None] * nCandidates
        self.tieProbs = np.zeros([nCandidates,nCandidates])
        self.pivotalityProbs = np.zeros([nCandidates,nCandidates])
        self.winnerProbs = np.zeros([nCandidates,nCandidates])
        self.pivotalities = np.zeros([nCandidates,nCandidates])
        self.newUtilitySum = np.zeros(nCandidates)
        self.newUtilDiff = np.zeros(nCandidates)

    #calculate the sincere utility - that is, without/before strategic conside-
    #rations - that this elector assigns for all candidates and stores them:
    def calcSincereUtilities(self, passedCandidate, minPreference,  	        \
                             maxPreference, distribution):
        nCandidates = len(passedCandidate)
        self.sincereUtilities = GlobalFuncs.randUtilities(minPreference,      \
                                                          maxPreference,      \
                                                          nCandidates,
                                                          distribution)
        self.sincereUtilities[GlobalFuncs.argMin(self.sincereUtilities)] = 0
        self.sincereUtilities[:] = [x / sum(self.sincereUtilities)            \
                                  for x in self.sincereUtilities]
        #self.strategicUtilities = self.sincereUtilities

    def calculateStrategicUtilities(self, passedCandidates, passedElectors, MIN_UTIL, iteration):
        electorID = self.ID
        nCandidates = len(passedCandidates)
        self.allVotes = GlobalFuncs.countVoteIntentions(passedElectors,        \
                                                    passedCandidates,iteration)
        self.chosenCandidate = self.chooseCandidate(passedCandidates, iteration)
        self.othersVotes = self.allVotes
        self.othersVotes[self.chosenCandidate.ID] =                            \
                                   self.othersVotes[self.chosenCandidate.ID] - 1
        for rowIndex in range(0,nCandidates):
            for colIndex in range(0,nCandidates):
                if rowIndex == colIndex:
                    self.tieProbs[rowIndex,colIndex] = 1
                    self.pivotalityProbs[rowIndex,colIndex] = 1
                    self.winnerProbs[rowIndex,colIndex] = 1
                else:
                    skellamA = self.othersVotes[rowIndex]
                    skellamB = self.othersVotes[colIndex]
                    if skellamA == 0:
                        skellamA = 10**-100
                    if skellamB == 0:
                        skellamB = 10**-100
                    self.tieProbs[rowIndex,colIndex] = skellam.pmf(0,skellamA,skellamB)
                    self.pivotalityProbs[rowIndex,colIndex] = skellam.pmf(-1,skellamA,skellamB)
                    self.winnerProbs[rowIndex,colIndex] = 1 - skellam.cdf(-1,skellamA,skellamB)
        #UNCOMMENT ONLY IN CASE OF PROBLEMS WITH 0 ENTRIES###############
        #for rowIndex in range(0,nCandidates):
        #    for colIndex in range(0,nCandidates):
        #        if math.isnan(self.tieProbs[rowIndex,colIndex]):
        #            self.tieProbs[rowIndex,colIndex] = 0
        #        if math.isnan(self.pivotalityProbs[rowIndex,colIndex]):
        #            self.pivotalityProbs[rowIndex,colIndex] = 0
        #        if math.isnan(self.winnerProbs[rowIndex,colIndex]):
        #            self.winnerProbs[rowIndex,colIndex] = 0
        #################################################################
        for rowIndex in range(0,nCandidates):
            for colIndex in range(0,nCandidates):
                if rowIndex != colIndex:
                    probsWoutPair = np.delete(self.winnerProbs,rowIndex,0)
                    probsWOutPair = np.delete(probsWoutPair,colIndex,1)
                    probsProd = np.prod(probsWOutPair)
                    otherPivsSum = self.pivotalityProbs[rowIndex,colIndex] + self.winnerProbs[rowIndex,colIndex]
                    self.pivotalities[rowIndex,colIndex] = probsProd * otherPivsSum
        if iteration == 0:
            self.previousUtilities = self.sincereUtilities
        else:
            self.previousUtilities = self.strategicUtilities
        for cand in range(0,nCandidates):
            for otherCand in range(0,nCandidates):
                utilityDiff = self.previousUtilities[cand] - self.sincereUtilities[otherCand]
                self.newUtilDiff[otherCand] = utilityDiff * self.pivotalities[cand,otherCand]
            self.newUtilitySum[cand] = np.sum(self.newUtilDiff)
        self.newUtilitySum[np.argmin(self.sincereUtilities)] = MIN_UTIL
        self.strategicUtilities = self.newUtilitySum
        return self.strategicUtilities
        
    
    #calculate the strategic utility - that is, considering winning probabi-
    #lities - that this elector assigns for all candidates and stores them:   
    #def calculateStrategicUtilities(self, passedCandidate, nElectors):
    #    index = 0
    #    for cand in passedCandidate:
    #        self.strategicUtilities[index] = cand.winProbability(nElectors)   \
    #                                         * self.sincereUtilities[index]
    #        index += 1
    #    totalStrategicUtilities = sum(self.strategicUtilities) 
    #    self.strategicUtilities[:] = [x / totalStrategicUtilities             \
    #                                for x in self.strategicUtilities]
    
    #find who is the currently chosen candidate, considering current strategic
    #utility calculation:
    def chooseCandidate(self, passedCandidates, iteration):
        if iteration == 0:
            return passedCandidates[GlobalFuncs.argMax(self.sincereUtilities)]
        else:
            return passedCandidates[GlobalFuncs.argMax(self.strategicUtilities)]
    
    def findLastCand(self, passedCandidates):
        return passedCandidates[GlobalFuncs.argMin(self.sincereUtilities)]

    #function that prints 
    def printPreference(self, passedCandidates):
        print "Elec " + str(self.ID) \
              + ", preferedCand: " + str(self.chooseCandidate().ID) \
              + ", leastCand: " + str(self.findLastCand(passedCandidates).ID)
        if self.ID == nElectors - 1:
            print "\n"
