#-----------------------------------------------------------------------------#
#
# Strategic voting (Cox 1994)
#
# Authors: Fabricio Vasselai & Samuel Baltz
#
# Purpose: To replicate Cox 1994 SNTV as an ABM
#
# First created: 30 May 2017
# Last modified: 12 June 2017
#
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
#Import libraries:
#-----------------------------------------------------------------------------#

from random import randint 
import numpy as np


#-----------------------------------------------------------------------------#
#Environmental or global variables:
#    A number of seats that candidates are competing for.
#    An initial number of candidates.
#    After voting, a vote total, producing a set of winners.
#-----------------------------------------------------------------------------#

#Initialize parameters
nElectors = 10 #Number of electors
nCandidates = 5 #Number of candidates
nSeats = 1 #Number of seats the candidates compete for

minPreference = 0
maxPreference = 10

electors = [None] * nElectors
candidates = [None] * nCandidates
candPrefs = [None] * nCandidates
allRankedCands = []


#-----------------------------------------------------------------------------#
#Global functions:
#-----------------------------------------------------------------------------#
def randPreference(minPreference, maxPreference):
    return randint(minPreference, maxPreference)


#-----------------------------------------------------------------------------#
#Candidate-owned Variables:
#    preference: 1-D Preference which naively represents some generic position.
#-----------------------------------------------------------------------------#

class Candidate:
    ID = 0
    preference = 0
    rank = 0
    sincereVotes = 0
    winProb = 0.0
    
    def __init__(self, inID, inPreference):
        self.ID = inID
        self.preference = inPreference
        
    def __eq__(self, another):
        return self.distance == another.distance
    
    def __lt__(self, another):
        return self.distance < another.distance
    
    def __gt__(self, another):
        return self.distance > another.distance
    
    def findDistance(self, candPreference, elecPreference):
        self.distance = abs(candPreference - elecPreference)
    
    def setRank(self, inRank):
        self.rank = inRank
 
    def countSincereVotes(self, inElectors):
        for e in range(0, nElectors):
            elec = inElectors[e]
            if elec.IDAndDist[0][1] == self.ID:
                self.sincereVotes = self.sincereVotes + 1

    def countSincereVotes(self, inElectors):
        for e in range(0, nElectors):
            elec = inElectors[e]
            if elec.IDAndDist[0][1] == self.ID:
                self.sincereVotes = self.sincereVotes + 1
        self.winProb = float(self.sincereVotes) / float(nElectors)
    
    def countStratVotes(self, inElectors):
        for e in range(0, nElectors):
            elec = inElectors[e]

    #def voteStrategically(self, inCandidates):
    #    self.maxUtility = max(elec.expectedUtility)
    #    self.nMaxSinCands = self.expectedUtility.count(self.maxUtility)
    #    for c in range(0, nCandidates):
    #        if self.nMaxSinCands == 1:
    #        
    #        if self.nMaxSinCands > 1:            

    #Printing functions
    def printCandPrefs(self):
        print "Cand " + str(cand.ID) + "'s preference:" + str(self.preference)
    
    def printSincereVotes(self):
        print "Cand " +str(cand.ID) +" sincere votes: " +str(self.sincereVotes)
        print "Cand " + str(cand.ID) + " win prob: " + str(self.winProb)
                                
#-----------------------------------------------------------------------------#
#Elector-owned Variables:
#    preference: 1-D Preference which naively represents some generic position.
#    expectation: a vector with the elector's expectation for each candidate
#        winning the election
#-----------------------------------------------------------------------------#

class Elector:
    #Initialize elector variables and matrices
    ID = 0
    preference = 0
    distances = [None] * nCandidates
    candIDs = [None] * nCandidates
    rankedCandidates = [None] * nCandidates
    unorderedCands = [None] * nCandidates
    candUtility = [None] * nCandidates
    expectedUtility = [None] * nCandidates
            
    #Define all elector-owned functions
    def __init__(self, inID, inPreference):
        self.ID = inID
        self.preference = inPreference
    
    def rankCandidates(self, inCandidates):
        for c in range(0, nCandidates):
            cand = inCandidates[c]
            cand.findDistance(cand.preference, self.preference)
            self.distances[c] = cand.distance
            self.candIDs[c] = cand.ID
            self.unorderedCands[c] = cand
        self.IDAndDist = zip(elec.distances, elec.candIDs, elec.unorderedCands)
        self.IDAndDist.sort()
        for c in range(0, nCandidates):
            self.rankedCandidates[c] = self.IDAndDist[c][2]

    def expectUtility(self, inCandidates):
        for c in range(0, nCandidates):
            cand = inCandidates[c]
            self.candUtility[c] = abs(self.preference - cand.preference)
            self.expectedUtility[c] = cand.winProb * self.candUtility[c]                
            
    #Printing functions         
    def printRankedCandidates(self):
        print "elector: " + str(self.ID)
        print "\n"
        for c in range(0, nCandidates):
            cand = self.rankedCandidates[c]
            print "candidate ID: " + str(cand.ID)
            print "elector preference: " + str(self.preference)
            print "candidate preference: " + str(cand.preference)
            print "distance: " + str(cand.distance)
            print "\n"
        print "ranking: "
        for c in range(0, nCandidates):
            cand = self.rankedCandidates[c]
            print elec.rankedCandidates[c].ID
        print "\n \n"

    def printExpectedU(self):
        print "elector " + str(elec.ID) + "' s EU: " +str(self.expectedUtility)
                                        
#-----------------------------------------------------------------------------#
#Populate the world:
#-----------------------------------------------------------------------------#

#Randomize one-dimensional preference:
for c in range(0, nCandidates):
    pref = randPreference(minPreference,maxPreference)
    cand = Candidate(c, pref)
    candidates[c] = cand
    candPrefs[c] = pref

for e in range(0, nElectors):
    pref = randPreference(minPreference,maxPreference)
    elec = Elector(e, pref)
    electors[e] = elec
    elec.rankCandidates(candidates)

for c in range(0, nCandidates):
    cand = candidates[c]
    cand.countSincereVotes(electors)
    cand.printSincereVotes()
    
for e in range(0, nElectors):
    elec = electors[e]
    elec.expectUtility(candidates)
    elec.printExpectedU()

#TO-DO:
#calculate original expectation of votes for each candidates by looping over
#    each elector
#implement random generation of preferences that are not uniform
#update the strategic choice of each voter












