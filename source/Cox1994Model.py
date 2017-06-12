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


#-----------------------------------------------------------------------------#
#Environmental or global variables:
#    A number of seats that candidates are competing for.
#    An initial number of candidates.
#    After voting, a vote total, producing a set of winners.
#-----------------------------------------------------------------------------#

#Initialize parameters
nElectors = 1 #Number of electors
nCandidates = 5 #Number of candidates
nSeats = 1 #Number of seats the candidates compete for

minPreference = 0
maxPreference = 10

electors = [None] * nElectors
candidates = [None] * nCandidates


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
 
    def printCandPrefs(self):
        print self.preference
    
#-----------------------------------------------------------------------------#
#Elector-owned Variables:
#    preference: 1-D Preference which naively represents some generic position.
#    expectation: a vector with the elector's expectation for each candidate
#        winning the election
#-----------------------------------------------------------------------------#

class Elector:
    #Initialize elector variables and matrices
    preference = 0
    expectation = [None] * nCandidates
    distances = [None] * nCandidates
    candIDs = [None] * nCandidates
    rankedCandidates = [None] * nCandidates
    orderedCands = [None] * nCandidates
    
    #Define all elector-owned functions
    def __init__(self, inPreference):
        self.preference = inPreference
        
    def setExpectation(self, inExpectation):
        self.expectation = inExpectation
    
    def rankCandidates(self, inCandidates):
        for c in range(0, nCandidates):
            cand = inCandidates[c]
            cand.findDistance(cand.preference, self.preference)
            self.distances[c] = cand.distance
            self.candIDs[c] = cand.ID
            self.orderedCands[c] = cand
        self.IDAndDist = zip(elec.distances, elec.candIDs, elec.orderedCands)
        self.IDAndDist.sort()
        for c in range(0, nCandidates):
            self.rankedCandidates[c] = self.IDAndDist[c][2]

         
    def printRankedCandidates(self):
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
        
#-----------------------------------------------------------------------------#
#Populate the world:
#-----------------------------------------------------------------------------#

#Randomize one-dimensional preference:
for c in range(0, nCandidates):
    pref = randPreference(minPreference,maxPreference)
    cand = Candidate(c, pref)
    candidates[c] = cand

print  "\n"

for e in range(0, nElectors):
    pref = randPreference(minPreference,maxPreference)
    elec = Elector(pref)
    elec.rankCandidates(candidates)
    electors[e] = elec
    
print  "\n"

for e in range(0, nElectors):    
    elec = electors[e]
    elec.printRankedCandidates()

#TO-DO:
#solve the problem of sorting candidates for ranking
#calculate original expectation of votes for each candidates by looping over
#    each elector
#implement random generation of preferences that are not uniform
#update the strategic choice of each voter












