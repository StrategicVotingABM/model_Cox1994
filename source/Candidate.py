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
    def winProbability(self, nElectors):
        if self.voteIntention == None:
            return 1
        else:
            return (float(self.voteIntention) / float(nElectors))
     
    #function that prints the candidates winning probability for debugging:
    def printWinProb(self, nElectors):
        print "Cand " + str(self.ID) + "'s winprob: "                         \
                      + str(self.winProbability(nElectors))