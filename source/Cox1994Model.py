#-----------------------------------------------------------------------------#
#
# Strategic voting (Cox 1994)
#
# Authors: Fabricio Vasselai & Samuel Baltz
#
# Purpose: To replicate Cox 1994 SNTV as an ABM
#
# Last modified: 31 July 2017
#
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
# Import libraries:
#-----------------------------------------------------------------------------#
#import sys
import numpy as np
import matplotlib as plt
import random 
#seed = random.randrange(sys.maxsize)
seed = random.randint(0,10000)
#seed = 7605
#seed = 5330
#seed = 6675
#seed = 5895 #Good one
#seed = 7145 #Third force becomes second
#Debugging seeds:
#seed= 4549 #nE=20, nC =3
#seed= 8690 #nE=20, nC =3
#seed= 2166 #nE=20, nC =2
#seed= 3993 #nE=20, nC =2
print "Seed: " + str(seed) + "\n"
random.seed(seed)
#random.seed(2282) #set a specific pseudo-rng seed for reprocability


#-----------------------------------------------------------------------------#
# Environmental or global variables
#-----------------------------------------------------------------------------#

#Initialize parameters:
nElectors = 1000 #Number of electors
nCandidates = 4 #Number of candidates
minPreference = 0 #min value of 1-D preference of electors and candidates
maxPreference = 100 #max value of 1-D preference of electors and candidates
allElectors = [None] * nElectors #list that stores the electors
allCandidates = [None] * nCandidates #list that stores the candidates
leastCandidates = [0] * nCandidates

#-----------------------------------------------------------------------------#
# Global functions:
#-----------------------------------------------------------------------------#

#Wrapper function to generalize the generation of random preferences. Later
#we can simply alter its implementation to handle different randomization of
#each preference dimension without having to change the rest of the code:
def randUtilities(minPreference, maxPreference):
    #Sample 1-D policy preference from an uniform distribution:
    #return np.random.uniform(minPreference, maxPreference, nCandidates)
    #Sample 1-D policy preference from a normal distribution:
    return  np.random.normal(0, 1, nCandidates)
    #Sample 1-d policy preference from one dirichlet distribution:
    #return np.random.dirichlet((1,2,3,4), 1).transpose()
    #Sample 1-d policy preference from two dirichlet distributions:
    #coin = random.randint(0, 1)
    #if coin == 0:
    #    return np.random.dirichlet((1,2,3,4), 1).transpose()
    #else:
    #   return np.random.dirichlet((4,3,2,1), 1).transpose()
    #Sample 1-d policy preference from three dirichlet distributions:
    #coin = random.randint(0, 2)
    #if coin == 0:
    #    return np.random.dirichlet((1,2,3,4), 1).transpose()
    #elif coin == 1:
    #   return np.random.dirichlet((4,3,2,1), 1).transpose()
    #else:
    #   return np.random.dirichlet((1,4,2,3), 1).transpose()
    
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

def plotLeastCandidates(passedElectors):
    for elector in passedElectors:
        index = elector.findLastCand().ID
        leastCandidates[index] += 1
    #for elector in passedElectors:
    #    leastCandidates.append(elector.chooseLastCand().ID)
    plt.pyplot.bar(list(range(nCandidates)), leastCandidates, align='center', alpha=0.5)
    print leastCandidates
    
    
#-----------------------------------------------------------------------------#
# Candidate-owned Variables:
#    ID: an unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    voteIntention: effective votes the candidate would currently receive if
#                the election was held at the given iteration (starts at 0)
#-----------------------------------------------------------------------------#

class Candidate:
            
    #overload of class constructor, that initializes candidate-owned variables
    def __init__(self, passedID):
        self.ID = passedID
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
            
#-----------------------------------------------------------------------------#
# Elector-owned Variables:
#    ID: an unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    strategicUtilities: a list with the elector's sincere expectation for each
#                        candidate
#-----------------------------------------------------------------------------#

class Elector:
    
    #overload of class constructor, that initializes elector-owned variables
    def __init__(self, passedID):
        self.ID = passedID
        self.strategicUtilities = [None] * nCandidates
        self.sincereUtilities = [None] * nCandidates
    
    #calculate the sincere utility - that is, without/before strategic conside-
    #rations - that this elector assigns for all candidates and stores them:
    def calculateSincereUtilities(self, passedCandidate):
        self.sincereUtilities = randUtilities(minPreference, maxPreference)
        self.sincereUtilities[argMin(self.sincereUtilities)] = 0
        self.sincereUtilities[:] = [x / sum(self.sincereUtilities)        \
                                  for x in self.sincereUtilities]
        #self.strategicUtilities = self.sincereUtilities
        
    #calculate the strategic utility - that is, considering winning probabi-
    #lities - that this elector assigns for all candidates and stores them:   
    def calculateStrategicUtilities(self, passedCandidate):
        index = 0
        for cand in passedCandidate:
            self.strategicUtilities[index] = cand.winProbability()            \
                                             * self.sincereUtilities[index]
            index += 1
        self.strategicUtilities[:] = [x / sum(self.strategicUtilities)            \
                                    for x in self.strategicUtilities]
    
    #find who is the currently chosen candidate, considering current strategic
    #utility calculation:
    def chooseCandidate(self):
        return allCandidates[argMax(self.strategicUtilities)]
    
    def findLastCand(self):
        return allCandidates[argMin(self.sincereUtilities)]

    #function that prints 
    def printPreference(self):
        print "Elec " + str(self.ID) \
              + ", preferedCand: " + str(self.chooseCandidate().ID) \
              + ", leastCand: " + str(self.findLastCand().ID)
        if self.ID == nElectors - 1:
            print "\n"
        
    
#-----------------------------------------------------------------------------#
# Populating the world:
#-----------------------------------------------------------------------------#

#Generate candidates:
for c in range(0, nCandidates):
    cand = Candidate(c)
    allCandidates[c] = cand

#Generate electors:
for e in range(0, nElectors):
    elector = Elector(e)
    elector.calculateSincereUtilities(allCandidates)
    allElectors[e] = elector
    
plotLeastCandidates(allElectors)

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
        #if iter == 0:
         #   elector.printPreference()

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