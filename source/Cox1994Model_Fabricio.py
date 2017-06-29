
#-----------------------------------------------------------------------------#
#
# Strategic voting (Cox 1994)
#
# Authors: Fabricio Vasselai & Samuel Baltz
#
# Purpose: To replicate Cox 1994 SNTV as an ABM
#
# First created: 30 May 2017
# Last modified: 20 June 2017
#
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
# Import libraries:
#-----------------------------------------------------------------------------#
import random 


#-----------------------------------------------------------------------------#
# Environmental or global variables
#-----------------------------------------------------------------------------#

#Initialize parameters
nIterations = 100
nElectors = 100 #Number of electors
nCandidates = 5 #Number of candidates
magnitude = 1 #Number of seats the candidates compete for

minPreference = 0 #min value of 1-D preference of electors and candidates
maxPreference = 100000 #max value of 1-D preference of electors and candidates
prefRange = maxPreference - minPreference

electors = [None] * nElectors #list that stores the electors
candidates = [None] * nCandidates #list that stores the candidates
candExpecPerformance = [None] * nCandidates 

intentionChanges = nElectors


#-----------------------------------------------------------------------------#
# Global functions:
#-----------------------------------------------------------------------------#

#Wrapper function to generalize the generation of random preferences. Later,
#we can simply alter its implementation to handle different randomization of
#each preference dimension without having to change the rest of the code:
def randPreference(minPreference, maxPreference):
    return random.randint(minPreference, maxPreference)


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
        self.sincereSupport = None
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
    def countVotes(self, allElectors):
        votes = 0
        for elector in allElectors:
            preferedCandidate = elector.rankedCandidates[0]
            if preferedCandidate.ID == self.ID:
                votes += 1 #increment number of votes gathered
        if self.sincereSupport == None:
           self.sincereSupport = votes
        self.voteIntention = votes

    def winProbability(self):
        if self.voteIntention == None:
            return 0
        else:
            return (float(self.voteIntention) / float(nElectors))

    #Candidate class printing functions to debug this class implementation:
    def printCandPrefs(self):
        print "Cand " + str(cand.ID) + "'s preference:" + str(self.preference)
    
    def printsincereSupport(self):
        print "Cand " +str(cand.ID) +" sincere votes: " +str(self.sincereSupport)

    def printvoteIntention(self):
        print "Cand " +str(cand.ID) + " votes: " + str(self.voteIntention)
    
    def printWinProb(self):
        print "Cand " + str(cand.ID) + "'s winprob: " \
                      + str(cand.winProbability())

                       
#-----------------------------------------------------------------------------#
# Elector-owned Variables:
#    ID: an unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    rankedCandidates: list of preference-ranked candidates                                                 #candidates
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
        self.rankedCandidates = [None] * nCandidates
        self.expectedValue = [None] * nCandidates
        self.chosenCandidate = None

    #Function for the elector to preference-rank candidates:
    def rankCandidates(self, inCandidates):
        distances = [None] * nCandidates
        index = 0
        for cand in inCandidates:
            #For now, we merely calculate distance between 1-D preferences from
            #this elector and the candidates:
            distance = abs(cand.preference - self.preference)
            distances[index] = distance * (1 - cand.winProbability())
            index += 1
        sortedDistance = sorted(zip(distances, inCandidates))
        self.rankedCandidates = [inCandidates for (distances, inCandidates) \
                                 in  sortedDistance]


    #Function that specifies how candidates make their strategic choices:
    def chooseCandidate(self):
        self.chosenCandidate = self.rankedCandidates[0]
        return 1
            
    #Elector-class printing functions to debug this class implementation:   
    def printRankedCandidates(self):
        print "elector ID: " + str(self.ID),
        print " preference: " + str(self.preference)
        for cand in candidates:
            print "candidate ID: " + str(cand.ID),
            print " preference: " + str(cand.preference),
            print " distance: " + str(abs(cand.preference - self.preference) \
                                       * (1 - cand.winProbability()))
        print "ranking: ",
        print self.rankedCandidates
        print "\n"


#-----------------------------------------------------------------------------#
# Populating the world:
#-----------------------------------------------------------------------------#
#random.seed(2282)

#Generate candidates:
for c in range(0, nCandidates):
    pref = randPreference(minPreference,maxPreference)
    cand = Candidate(c, pref)
    candidates[c] = cand

#Generate electors:
for e in range(0, nElectors):
    pref = randPreference(minPreference,maxPreference)
    elector = Elector(e, pref)
    electors[e] = elector
    

#-----------------------------------------------------------------------------#
# Main simulation loop:
#-----------------------------------------------------------------------------#

for iter in range(0, nIterations):

    #Update electoral choice (at iter == 0, it's the sincere preference,
    #while after that is always strategic voting intention):
    for elector in electors:
        elector.rankCandidates(candidates)
        elector.chooseCandidate()

    #Count current votes of candidates:
    for cand in candidates:
        cand.countVotes(electors)
        #Show vote intention in the first and last iterations:
        if iter == 0 or iter == nIterations - 1:
            cand.printWinProb()

    if iter == 0 or iter == nIterations - 1:
        print "\n"
