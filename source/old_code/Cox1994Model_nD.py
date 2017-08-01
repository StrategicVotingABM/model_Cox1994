#-----------------------------------------------------------------------------#
#
# Strategic voting (Cox 1994)
#
# Authors: Fabricio Vasselai & Samuel Baltz
#
# Purpose: To replicate Cox 1994 SNTV as an ABM
#
# Last modified: 24 July 2017
#
# Commit comment: The updating now converges to Cox's results most of the time
# but not always. And without pre-cooking with distributions of preferences.
# Still have to check which cases, and why, it fails.
#
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
# Import libraries:
#-----------------------------------------------------------------------------#
import random
import numpy as np
#random.seed(2282) #set a specific pseudo-rng seed for reprocability


#-----------------------------------------------------------------------------#
# Environmental or global variables
#-----------------------------------------------------------------------------#

#Initialize parameters:
nIterations = 1000
nElectors = 10 #Number of electors
nCandidates = 5 #Number of candidates
minPreference = 0 #min value of 1-D preference of electors and candidates
maxPreference = 1 #max value of 1-D preference of electors and candidates
allElectors = [None] * nElectors #list that stores the electors
allCandidates = [None] * nCandidates #list that stores the candidates
nPreferences = nCandidates + 1 #set the dimensionality of preferences
pref = [None] * nPreferences #initialize the preference vector

#-----------------------------------------------------------------------------#
# Global functions:
#-----------------------------------------------------------------------------#

#Wrapper function to generalize the generation of random preferences. Later
#we can simply alter its implementation to handle different randomization of
#each preference dimension without having to change the rest of the code:
def randPreference(minPreference, maxPreference):
    return random.uniform(minPreference, maxPreference)

#Function to identify which list's element has the maximum value in the list:
def argMax(inArray):
    argIndex = 0
    current = inArray[argIndex]
    for i in range(len(inArray)):
        if current < inArray[i]:
            current = inArray[i]
            argIndex = i
    return argIndex

#Function to identify which list's element has the minimum value in the list:
def argMin(inArray):
    argIndex = 0
    current = inArray[argIndex]
    for i in range(len(inArray)):
        if current > inArray[i]:
            current = inArray[i]
            argIndex = i
    return argIndex

#Function that counts vote intention of all candidates in the current moment.
#The reason why it is a global function instead of a member function of either
#Candidates or Electors classes is for performance: then we don't have to make
#nCandidates x nElectors calculations:
def countVoteIntentions(passedElectors, passedCandidates):
    for candidate in passedCandidates:
        candidate.voteIntention = 0
    for elector in passedElectors:
        chosenCandidate = elector.chooseCandidate()
        lastCandidate = elector.chooseLastCand()
        chosenCandidate.voteIntention += 1


#-----------------------------------------------------------------------------#
# Candidate-owned Variables:
#    ID: a unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    voteIntention: effective votes the candidate would currently receive if
#                the election was held at the given iteration (starts at 0)
#-----------------------------------------------------------------------------#

class Candidate:
            
    #overload of class constructor, that initializes candidate-owned variables
    def __init__(self, passedID, passedPreference):
        self.ID = passedID
        self.preference = passedPreference
        self.voteIntention = None
    
    #Function that counts how many sincere votes a given candidate would gather
    #if there were no strategic behavior by the electors, that is, if only the
    #original distance between electors and candidate's preferences were to
    #determinte the voting:
    def winProbability(self):
        if self.voteIntention == None:
            return 1
        else:
            return (float(self.voteIntention) / float(nElectors))
     
    #function that prints the candidates winning probability for debugging:
    def printWinProb(self):
        print "Cand " + str(cand.ID) + "'s winprob: " \
                      + str(cand.winProbability())

    #def printCandInfo(self):
    #    roundedPref = str(round(self.preference, 2))
    #    print "Cand " + str(self.ID) + "'s preference: " + roundedPref
    #    if self.ID == nCandidates - 1:
    #        print "\n"
            
#-----------------------------------------------------------------------------#
# Elector-owned Variables:
#    ID: an unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    strategicUtilities: a list with the elector's sincere expectation for each
#                        candidate
#-----------------------------------------------------------------------------#

class Elector:
    
    #overload of class constructor, that initializes elector-owned variables
    def __init__(self, passedID, passedPreference):
        self.ID = passedID
        self.preference = passedPreference
        self.strategicUtilities = [None] * nCandidates
                              
    #function that finds the sincere utility that this elector assigns
    #for the passed candidate, i.e. without/before strategic considerations:                         
    def utilityFunction(self, passedCandidate):
        cand = passedCandidate
        sumPrefs = 0
        for p in range(0,nPreferences):
            sumPrefs = sumPrefs + (self.preference[p] - cand.preference[p])**2
        utility = np.sqrt((maxPreference - minPreference)**2 \
            * nPreferences) - np.sqrt(sumPrefs)
        return utility
        
    #calculate the sincere utility - that is, without/before strategic conside-
    #rations - that this elector assigns for all candidates and stores them:
    def calculatestrategicUtilities(self, passedCandidate):
        index = 0
        for cand in passedCandidate:
            self.strategicUtilities[index] = self.utilityFunction(cand)
            index += 1
        self.strategicUtilities[argMin(self.strategicUtilities)] = 0
        self.strategicUtilities[:] = [x / sum(self.strategicUtilities)  \
                                  for x in self.strategicUtilities]
        print "elector" + str(self.ID) + "'s last candidate " +         \
                                    str(argMin(self.strategicUtilities))
        if elector.ID == nElectors - 1:
            print "\n"
                   
    #calculate the strategic utility - that is, considering winning probabi-
    #lities - that this elector assigns for all candidates and stores them:   
    def calculateStrategicUtility(self, passedCandidate):
        index = 0
        for cand in passedCandidate:
            self.strategicUtilities[index] *= cand.winProbability()
            index += 1
        self.strategicUtilities[:] = [x / sum(self.strategicUtilities)  \
                                  for x in self.strategicUtilities]
    
    #find who is the currently chosen candidate, considering current strategic
    #utility calculation:
    def chooseCandidate(self):
        return allCandidates[argMax(self.strategicUtilities)]

    def chooseLastCand(self):
        return allCandidates[argMin(self.strategicUtilities)]        
                        
#-----------------------------------------------------------------------------#
# Populating the world:
#-----------------------------------------------------------------------------#

#Generate candidates:
for c in range(0, nCandidates):
    pref = [None] * nPreferences
    for i in range(0,nPreferences):
        pref[i] = randPreference(minPreference,maxPreference)
    cand = Candidate(c, pref)
    allCandidates[c] = cand

#for candidate in allCandidates:
#    print candidate.preference

#Generate electors:
for e in range(0, nElectors):
    pref = [None] * nPreferences
    for c in range(0, nPreferences):
        pref[c] = randPreference(minPreference,maxPreference)
    elector = Elector(e, pref)
    elector.calculatestrategicUtilities(allCandidates)
    allElectors[e] = elector

#for elector in allElectors:
#    print elector.preference

#-----------------------------------------------------------------------------#
# Main simulation loop:
#-----------------------------------------------------------------------------#

for iter in range(0, nIterations):

    #Update strategic utility considerations of electors, given the current
    #winning probabilities of candidates:
    for elector in allElectors:
        elector.calculateStrategicUtility(allCandidates)

    #count the vote intention of all electors towards all candidates for the
    #current iterations:
    countVoteIntentions(allElectors, allCandidates)            
    
    #Show vote intentions in the first and last iterations:
    if iter == 0 or iter == nIterations - 1:
        for cand in allCandidates:
            cand.printWinProb()
        print "\n"
        

#-----------------------------------------------------------------------------#
# End of file
#-----------------------------------------------------------------------------#