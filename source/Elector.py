#-----------------------------------------------------------------------------#
# Elector-owned Variables:
#    ID: an unique identification number for each candidate
#    preference: 1-D preference which represents a generic policy position
#    strategicUtilities: a list with the elector's sincere expectation for each
#                        candidate
#-----------------------------------------------------------------------------#

import GlobalFuncs

class Elector:
    
    #overload of class constructor, that initializes elector-owned variables
    def __init__(self, passedID, nCandidates):
        self.ID = passedID
        self.strategicUtilities = [None] * nCandidates
        self.sincereUtilities = [None] * nCandidates
    
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
        
    #calculate the strategic utility - that is, considering winning probabi-
    #lities - that this elector assigns for all candidates and stores them:   
    def calculateStrategicUtilities(self, passedCandidate, nElectors):
        index = 0
        for cand in passedCandidate:
            self.strategicUtilities[index] = cand.winProbability(nElectors)   \
                                             * self.sincereUtilities[index]
            index += 1
        totalStrategicUtilities = sum(self.strategicUtilities) 
        self.strategicUtilities[:] = [x / totalStrategicUtilities             \
                                    for x in self.strategicUtilities]
    
    #find who is the currently chosen candidate, considering current strategic
    #utility calculation:
    def chooseCandidate(self, passedCandidates):
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