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
# Commit comment: The updating now converges to Cox's results (without 
# pre-cooking with distributions of preferences) most of the time. But not
# always: often there are cases when electors converge 100% to one candidate.
#
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
# Import libraries:
#-----------------------------------------------------------------------------#
#import sys
import random 
#seed = random.randrange(sys.maxsize)
seed = random.randint(0,10000)
#seed = 5330
#seed = 6675
#seed = 5895 #Good one
#seed = 7145 #Third force becomes second
print "Seed: " + str(seed) + "\n"
random.seed(seed)
#random.seed(2282) #set a specific pseudo-rng seed for reprocability


#-----------------------------------------------------------------------------#
# Environmental or global variables
#-----------------------------------------------------------------------------#

#Initialize parameters:
nElectors = 1000 #Number of electors
nCandidates = 5 #Number of candidates
minPreference = 0 #min value of 1-D preference of electors and candidates
maxPreference = 100 #max value of 1-D preference of electors and candidates
allElectors = [None] * nElectors #list that stores the electors
allCandidates = [None] * nCandidates #list that stores the candidates


#-----------------------------------------------------------------------------#
# Global functions:
#-----------------------------------------------------------------------------#

#Wrapper function to generalize the generation of random preferences. Later
#we can simply alter its implementation to handle different randomization of
#each preference dimension without having to change the rest of the code:
def randPreference(minPreference, maxPreference):
    #Sample 1-D policy preference from an uniform distribution:
    return random.uniform(minPreference, maxPreference)
    #Sample 1-D policy preference from a normal distribution:
    #return  random.normalvariate(0,1)
    
#Function that efficiently checks whether two lists are identical:
def areListsIdentical(lhs, rhs):
    result = True
    if len(lhs) != len(rhs):
        result = False
    else:
        i = 0
        while result == True and i < len(lhs):
            if lhs[i] != rhs[i]:
                result = False
            i += 1
    return result

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

#Print the electoral results in case elections were held at the given moment:
def printElectResultsAsOfNow(passedCandidates):
    for cand in passedCandidates:
        cand.printWinProb()
    print "\n"

#Function that counts vote intention of all candidates in the current moment.
#The reason why it is a global function instead of a member function of either
#Candidates or Electors classes if for performance: then we don't have to make
#nCandidates x nElectors calculations:
def countVoteIntentions(passedElectors, passedCandidates):
    for candidate in passedCandidates:
        candidate.voteIntention = 0
    for elector in passedElectors:
        chosenCandidate = elector.chooseCandidate()
        chosenCandidate.voteIntention += 1
    newVoteIntentions = [None] * nCandidates
    index = 0
    for candidate in passedCandidates:
        newVoteIntentions[index] = candidate.voteIntention
        index += 1
    return newVoteIntentions


#-----------------------------------------------------------------------------#
# Candidate-owned Variables:
#    ID: an unique identification number for each candidate
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
    #original distance between electors  and candidate's preferences were to
    #determinte the voting:
    def winProbability(self):
        if self.voteIntention == None:
            return 1
        else:
            return (float(self.voteIntention) / float(nElectors))
     
    #function that prints the candidates winning probability for debugging:
    def printWinProb(self):
        print "Cand " + str(self.ID) + "'s winprob: "                         \
                      + str(self.winProbability())
            
    #function that prints 
    def printPreference(self):
        roundedPref = str(round(self.preference, 2))
        print "Cand " + str(self.ID) + "'s preference: " + roundedPref
        if self.ID == nCandidates - 1:
            print "\n"
            
            
#-----------------------------------------------------------------------------#
# Elector-owned Variables:
#    ID: an unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    expectedUtilities: a list with the elector's sincere expectation for each
#                        candidate
#-----------------------------------------------------------------------------#

class Elector:
    
    #overload of class constructor, that initializes elector-owned variables
    def __init__(self, passedID, passedPreference):
        self.ID = passedID
        self.preference = passedPreference
        self.expectedUtilities = [None] * nCandidates
                              
    #function that finds the sincere utility that this elector assigns
    #for the passed candidate, i.e. without/before strategic considerations:                         
    def utilityFunction(self, passedCandidate):
        return maxPreference - minPreference                                  \
               - abs(self.preference-passedCandidate.preference)
        
    #calculate the sincere utility - that is, without/before strategic conside-
    #rations - that this elector assigns for all candidates and stores them:
    def calculateSincereUtilities(self, passedCandidate):
        index = 0
        for cand in passedCandidate:
            self.expectedUtilities[index] = self.utilityFunction(cand)
            index += 1
        self.expectedUtilities[argMin(self.expectedUtilities)] = 0
        self.expectedUtilities[:] = [x / sum(self.expectedUtilities)        \
                                  for x in self.expectedUtilities]
            
    #calculate the strategic utility - that is, considering winning probabi-
    #lities - that this elector assigns for all candidates and stores them:   
    def calculateStrategicUtilities(self, passedCandidate):
        index = 0
        for cand in passedCandidate:
            self.expectedUtilities[index] *= cand.winProbability()
            index += 1
        self.expectedUtilities[:] = [x / sum(self.expectedUtilities)        \
                                  for x in self.expectedUtilities]
    
    #find who is the currently chosen candidate, considering current strategic
    #utility calculation:
    def chooseCandidate(self):
        return allCandidates[argMax(self.expectedUtilities)]
        
    
#-----------------------------------------------------------------------------#
# Populating the world:
#-----------------------------------------------------------------------------#

#Generate candidates:
for c in range(0, nCandidates):
    pref = randPreference(minPreference,maxPreference)
    cand = Candidate(c, pref)
    allCandidates[c] = cand
    cand.printPreference()

#Generate electors:
for e in range(0, nElectors):
    pref = randPreference(minPreference,maxPreference)
    elector = Elector(e, pref)
    elector.calculateSincereUtilities(allCandidates)
    allElectors[e] = elector
    

#-----------------------------------------------------------------------------#
# Main simulation loop:
#-----------------------------------------------------------------------------#

lastVoteIntentions = [None] * nCandidates
currentVoteIntentions = [None] * nCandidates
iter = 0 #iteration counter

#Loop until convergence is met, i.e. in this simplistic version = when nothing
#changes from one iteration to the next:
while not areListsIdentical(lastVoteIntentions, currentVoteIntentions)        \
      or iter <= 1:

    lastVoteIntentions = currentVoteIntentions
    
    #Update strategic utility considerations of electors, given the current
    #winning probabilities of candidates:
    for elector in allElectors:
        elector.calculateStrategicUtilities(allCandidates)

    #count the vote intention of all electors towards all candidates for the
    #current iterations:
    currentVoteIntentions = countVoteIntentions(allElectors, allCandidates)            

    #Show vote intention shares in the first iteration:
    if iter == 0:
        printElectResultsAsOfNow(allCandidates)
    
    iter += 1
   
#Show vote intention shares after convergence:
printElectResultsAsOfNow(allCandidates)
        
print "Converged after " + str(iter - 1) + " iterations."

                              
#-----------------------------------------------------------------------------#
# End of file
#-----------------------------------------------------------------------------#