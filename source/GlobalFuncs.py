#-----------------------------------------------------------------------------#
# Global functions:
#-----------------------------------------------------------------------------#
import numpy as np
import matplotlib as plt
import scipy.stats

#Wrapper function to generalize the generation of random preferences. Later
#we can simply alter its implementation to handle different randomization of
#each preference dimension without having to change the rest of the code:
def randUtilities(minPreference, maxPreference, nCandidates, distribution):
    if distribution == "uniform":
        #Sample 1-D policy preference from an uniform distribution:
        return np.random.uniform(minPreference, maxPreference, nCandidates)
    elif distribution == "stdnormal":
        #Sample 1-D policy preference from a normal distribution:
        return  np.random.normal(0, 1, nCandidates)
    elif distribution == "1dirichlet":
        #Sample 1-d policy preference from one dirichlet distribution:
        return np.random.dirichlet((1,2,3,4), 1).transpose()
    elif distribution == "2dirichlets":
        #Sample 1-d policy preference from two dirichlet distributions:
        coin = np.random.randint(0,2)
        if coin == 0:
            return np.random.dirichlet((1,2,3,4), 1).transpose()
        else:
            return np.random.dirichlet((4,3,2,1), 1).transpose()
    elif distribution == "3dirichlets":
        #Sample 1-d policy preference from three dirichlet distributions:
        coin = np.random.randint(0,3)
        if coin == 0:
            return np.random.dirichlet((1,2,3,4), 1).transpose()
        elif coin == 1:
            return np.random.dirichlet((4,3,2,1), 1).transpose()
        else:
            return np.random.dirichlet((1,4,2,3), 1).transpose()
    elif distribution == "4dirichlets":
        #Sample 1-d policy preference from three dirichlet distributions:
        coin = np.random.randint(0,4)
        if coin == 0:
            return np.random.dirichlet((2,1,3,4), 1).transpose()
        elif coin == 1:
            return np.random.dirichlet((3,4,2,1), 1).transpose()
        elif coin == 2:
            return np.random.dirichlet((4,1,3,2), 1).transpose()
        elif coin == 3:
            return np.random.dirichlet((1,3,2,4), 1).transpose()
    elif distribution == "magicalBeta":
        return scipy.stats.beta(nCandidates,1,1)
    elif distribution == "powerlaw":
        return np.random.power(3,nCandidates)
            
#Function that efficiently checks whether two lists are identical:
def areIdentical(lhs, rhs):
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
def printElectResultsAsOfNow(passedCandidates, nElectors):
    for cand in passedCandidates:
        cand.printWinProb(nElectors)
    print "\n"

#Function that counts vote intention of all candidates in the current moment.
#The reason why it is a global function instead of a member function of either
#Candidates or Electors classes if for performance: then we don't have to make
#nCandidates x nElectors calculations:
def countVoteIntentions(passedElectors, passedCandidates, iteration):
    nCandidates = len(passedCandidates)
    for candidate in passedCandidates:
        candidate.voteIntention = 0
    for elector in passedElectors:
        chosenCandidate = elector.chooseCandidate(passedCandidates, iteration)
        chosenCandidate.voteIntention += 1
    newVoteIntentions = [None] * nCandidates
    index = 0
    for candidate in passedCandidates:
        newVoteIntentions[index] = candidate.voteIntention
        index += 1
    return newVoteIntentions

def plotLeastCandidates(leastCandidates, passedElectors, passedCandidates):
    nCandidates = len(passedCandidates)
    for elector in passedElectors:
        index = elector.findLastCand(passedCandidates).ID
        leastCandidates[index] += 1
    #for elector in passedElectors:
    #    leastCandidates.append(elector.chooseLastCand().ID)
    #plt.pyplot.bar(list(range(nCandidates)), leastCandidates,                 \
    #               align='center', alpha=0.5)
    print leastCandidates
