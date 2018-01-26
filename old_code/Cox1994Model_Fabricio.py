#-----------------------------------------------------------------------------#
#
# Strategic voting (Cox 1994)
#
# Authors: Fabricio Vasselai & Samuel Baltz
#
# Purpose: To replicate Cox 1994 SNTV as an ABM
#
# First created: 30 May 2017
# Last modified: 20 July 2017
#
# Commit comment: The updating still does not converge to Cox's results;
# needs to improve on how to relate preference distance between electors and
# candidates and candidates' expected vote shares
#
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
# Import libraries:
#-----------------------------------------------------------------------------#
import random 
#random.seed(2282) #set a specific pseudo-rng seed for reprocability


#-----------------------------------------------------------------------------#
# Environmental or global variables
#-----------------------------------------------------------------------------#

#Initialize parameters
nIterations = 100
nElectors = 1000 #Number of electors
nCandidates = 5 #Number of candidates
#magnitude = 1 #Number of seats the candidates compete for

minPreference = 0 #min value of 1-D preference of electors and candidates
maxPreference = 1 #max value of 1-D preference of electors and candidates
prefRange = maxPreference - minPreference
electors = [None] * nElectors #list that stores the electors
candidates = [None] * nCandidates #list that stores the candidates


#-----------------------------------------------------------------------------#
# Global functions:
#-----------------------------------------------------------------------------#

#Wrapper function to generalize the generation of random preferences. Late
#we can simply alter its implementation to handle different randomization of
#each preference dimension without having to change the rest of the code:
def randPreference(minPreference, maxPreference):
    return random.uniform(minPreference, maxPreference)

def argMax(inArray):
    argIndex = 0
    current = inArray[argIndex]
    for i in range(len(inArray)):
        if current < inArray[i]:
            current = inArray[i]
            argIndex = i
    return argIndex

def argMin(inArray):
    argIndex = 0
    current = inArray[argIndex]
    for i in range(len(inArray)):
        if current > inArray[i]:
            current = inArray[i]
            argIndex = i
    return argIndex

def countVoteIntentions(allCandidates, allElectors):
    for candidate in allCandidates:
        candidate.voteIntention = 0
    for elector in allElectors:
        allCandidates[elector.chooseCandidate()].voteIntention += 1


#-----------------------------------------------------------------------------#
# Candidate-owned Variables:
#    ID: an unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    sincereSupport: sincere votes the candidate would receive if no strategic
#                  considerations were made by electors
#    voteIntention: effective votes the candidate would currently receive if
#                the election was held at the given iteration (starts at 0)
#-----------------------------------------------------------------------------#

class Candidate:
            
    #overload of class constructor, that initializes candidate-owned variables
    def __init__(self, passedID, passedPreference):
        self.ID = passedID
        self.preference = passedPreference
        self.voteIntention = None
    
    #overload of the equality check operator (==) for this class, in order to
    #specify what does it mean for two candidates to be equal/different
    def __eq__(self, another):
        return self.ID == another.ID #equalness means having the same ID

    #overloads the REPRESENTATION function, to specify what does it mean to
    #print an instance of this class
    def __repr__(self):
        return str(self.ID) #printing a candidate will mean printing her ID
    
    #Function that counts how many sincere votes a given candidate would gather
    #if there were no strategic behavior by the electors, that is, if only the
    #original distance between electors  and candidate's preferences were to
    #determinte the voting:
    def winProbability(self):
        if self.voteIntention == None:
            return 1
        else:
            return (float(self.voteIntention) / float(nElectors))
     
    def printWinProb(self):
        print "Cand " + str(cand.ID) + "'s winprob: " \
                      + str(cand.winProbability())
            
            
#-----------------------------------------------------------------------------#
# Elector-owned Variables:
#    ID: an unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    rankedCandidates: list of preference-ranked candidates
#    expectedValue: a vector with the elector's expectation for each candidate
#                   winning the election
#    chosenCandidate: candidate for which this elector would currently
#                     cast her vote
#-----------------------------------------------------------------------------#

class Elector:
    
    #overload of class constructor, that initializes elector-owned variables
    def __init__(self, inID, inPreference):
        self.ID = inID
        self.preference = inPreference
        self.sincereUtility = [None] * nCandidates
                                  
    def utilityFunction(self, inCand):
        return maxPreference - abs(self.preference - inCand.preference)
        
    def calculateSincereUtility(self, inCandidates):
        index = 0
        for cand in inCandidates:
            self.sincereUtility[index] = self.utilityFunction(cand)
            index += 1
        self.sincereUtility[argMin(self.sincereUtility)] = 0
        self.sincereUtility[:] = [x / sum(self.sincereUtility) for x in self.sincereUtility]
            
    def calculateStrategicUtility(self, inCandidates):
        index = 0
        for cand in inCandidates:
            self.sincereUtility[index] *= cand.winProbability()
            index += 1
        self.sincereUtility[:] = [x / sum(self.sincereUtility) for x in self.sincereUtility]
    
    def chooseCandidate(self):
        return argMax(self.sincereUtility)
        
    
#-----------------------------------------------------------------------------#
# Populating the world:
#-----------------------------------------------------------------------------#

#Generate candidates:
for c in range(0, nCandidates):
    pref = randPreference(minPreference,maxPreference)
    cand = Candidate(c, pref)
    candidates[c] = cand

#Generate electors:
for e in range(0, nElectors):
    pref = randPreference(minPreference,maxPreference)
    elector = Elector(e, pref)
    elector.calculateSincereUtility(candidates)
    electors[e] = elector
    

#-----------------------------------------------------------------------------#
# Main simulation loop:
#-----------------------------------------------------------------------------#

for iter in range(0, nIterations):

    #Update electoral choice (at iter == 0, it's the sincere preference,
    #while after that is always strategic voting intention):
    for elector in electors:
        elector.calculateStrategicUtility(candidates)

    countVoteIntentions(candidates, electors)            
    
    #Show vote intention in the first and last iterations:
    if iter == 0 or iter == nIterations - 1:
        for cand in candidates:
            cand.printWinProb()
        print "\n"
        

#-----------------------------------------------------------------------------#
# End of file
#-----------------------------------------------------------------------------#    
    
    
    
    
    

