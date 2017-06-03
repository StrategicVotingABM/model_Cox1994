#-----------------------------------------------------------------------------#
#
# Strategic voting - replicating Cox (1994)
#
# Authors: Fabricio Vasselai & Samuel Baltz
#
# Purpose: To replicate Cox 1994 SNTV as an ABM
#
# First created: 30 May 2017
# Last modified: 31 May 2017
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
        self.preference = inPreference
        
    def __eq__(self, another):
        return self.rank == another.rank
    
    def __lt__(self, another):
        return self.rank < another.rank
    
    def __gt__(self, another):
        return self.rank > another.rank
    
    def setRank(self, inRank):
        self.rank = inRank
        
    
#-----------------------------------------------------------------------------#
#Elector-owned Variables:
#    preference: 1-D Preference which naively represents some generic position.
#    expectation: a vector with the elector's expectation for each candidate
#        winning the election
#-----------------------------------------------------------------------------#

class Elector:
    preference = 0
    expectation = [None] * nCandidates
    rankedCandidates = [None] * nCandidates
    
    def __init__(self, inPreference):
        self.preference = inPreference
        
    def setExpectation(self, inExpectation):
        self.expectation = inExpectation
    
    def rankCandidates(self, inCandidates):
        for c in range(0, nCandidates):
            cand = inCandidates[c]
            
            print candidates[c].rank
            
            cand.setRank(self.preference - cand.preference)
            
            print cand.rank
            
            #print"Candidate " + str(c) + ": "  + str(self.preference - cand.preference)
            
            self.rankedCandidates[c] = cand
            
            #print"Candidate " + str(c) + ": "  + str(self.rankedCandidates[c].rank)
            
        #print self.rankedCandidates[0].rank
        self.rankedCandidates.sort(reverse = True)
        #print self.rankedCandidates[0].preference
        
    def printRankedCandidates(self):
        cand = self.rankedCandidates[0]
        print cand.preference
 
        
#-----------------------------------------------------------------------------#
#Populate the world:
#-----------------------------------------------------------------------------#

#Randomize one-dimensional preference:
for c in range(0, nCandidates):
    pref = randPreference(minPreference,maxPreference)
    cand = Candidate(c, pref)
    candidates[c] = cand
    #print cand.preference

print  "\n"

for e in range(0, nElectors):
    pref = randPreference(minPreference,maxPreference)
    elec = Elector(pref)
    elec.rankCandidates(candidates)
    electors[e] = elec
    #print elec.preference
    
print  "\n"

for e in range(0, nElectors):    
    elec = electors[e]
    elec.printRankedCandidates()
    
    


print "\nI compiled! :D\n"


#TO-DO:
#solve the problem of sorting candidates for ranking
#calculate original expectation of votes for each candidates by looping over
#    each elector
#implement random generation of preferences that are not uniform
#update the strategic choice of each voter












