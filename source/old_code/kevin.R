rm(list=ls())
library(MCMCpack)

maxNumIterations <- 1000
nElectors <- 10000
nCand <- 4

electors  <- matrix(ncol = nCand , nrow = nElectors)
electors <- rdirichlet(5000,c(1,2,2,4))
electorsBuffer <- rdirichlet(5000,c(4,3,3,1))
electors <- rbind(electors,electorsBuffer)


for(i in 1:nElectors){
  #electors[i,] <- rnorm(nCand, 0, 1)
  temp <- electors[i,]
  temp[which.min(temp)] <- 0
  temp <- temp/sum(temp)
  electors[i,] <- temp
}

party.prob <- matrix(ncol = nCand , nrow = nElectors)
iter <- 0
prop.votes <- last.prop.votes <- rep(0,nCand)
while((last.prop.votes != prop.votes || iter == 0) ){
  iter <- iter + 1
  last.prop.votes = prop.votes
  which.votes <- apply(electors,1,which.max)
  for(j in 1:nCand ){
    prop.votes[j] <- length(which.votes[which.votes == j])
  }
  prop.votes <- prop.votes/nElectors
  for(i in 1:nElectors){
    bb <- electors[i,]*prop.votes
    bb <- bb/sum(bb)
    electors[i,] <- bb
  }
  print(prop.votes)
}
print(prop.votes)