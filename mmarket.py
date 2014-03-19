import sys
import random
import math
import numpy

def printf(format, *args): 
    sys.stdout.write(format % args)
#prints out info on data set
whoProposes = "men"
preference = "empirical-edu"
searchCosts = "off"
populationComposition = "2010-National"
acceptabilityThreshold = 50
numWomen = 2000
numMen = 2000
numTotal = numWomen + numMen

class agent( ):
    def __init__(self): 
    # placeholders for agent attributes
        self.sex = ""
        self.age = 0
        self.income = 0 
        self.race = ""
        self.edu = 0 
        self.neverMarried = 0 
        self.preferenceList = []
        self.linkedTo = []
        self.linkedFrom = []
        self.matched = 0  
        self.coll_m = 0
        self.hs_m = 0
        self.somecoll_m = 0
        self.grad_m = 0 
        self.coll = 0
        self.hs = 0
        self.somecoll = 0
        self.grad = 0
        self.acceptabilityThreshold = 0;
        self.b_m = 0 
        self.w_m = 0 
        self.h_m = 0 
        self.a_m = 0 
        self.b = 0   
        self.w = 0   
        self.h = 0   
        self.a = 0   
        self.id = 0  

    def computePreferences(self, model):    
        for agent in model.agentList:
            #matching different agents 
            if ( agent.sex != self.sex ): 
                self.preferenceList.append(agent)
                #add agents of opposite sex in preference list
        if preference == "random":                
        #shuffle the preference list for some additional randomness
        #this is probably unnecessary...
            random.shuffle(self.preferenceList) 

        elif preference == "competition-edu":
        #sort by decreasing education
            self.preferenceList.sort(key=lambda x: x.edu, reverse=True)

        elif preference == "matching-edu":
            self.absList = []
            for agent in self.preferenceList:
                self.absVal = abs( float(self.edu) - float(agent.edu) )
                self.absList.append(self.absVal)                    
            #sort by matching education (lowest to highest)
            inds = numpy.argsort(self.absList)
            self.preferenceList = numpy.take(self.preferenceList, inds)
            #convert the numpy array back to a list            
            self.preferenceList = self.preferenceList.tolist()

        elif preference == "empirical-edu":
            print "------- "
            print 'for agent {0} computePreferences by={1}'.format( self.id, preference )
            self.utilityMatchList = []
            del self.utilityMatchList[:]
            for agent in self.preferenceList:
                self.hs_m = 0 
                self.somecoll_m = 0 
                self.coll_m = 0
                self.grad_m = 0
                if int(agent.edu) <= 12:
                    self.hs_m = 1
                elif int(agent.edu) > 12 and int(agent.edu) < 16:
                    self.somecoll_m = 1 
                else: 
                    self.coll_m = 1
                    self.grad_m = 1                
                self.utMatch = 0 
                if self.sex == "male":
                    # calculating male utility from education 
                    self.utMatch = math.exp( self.coll * self.grad_m * -.2629087 + self.coll * self.somecoll_m * -.3641229 +
                        self.coll * self.hs_m * -.554391 + self.grad * self.coll_m * .0723642 + self.grad * 
                        self.somecoll_m * -.2395778 + self.grad * self.hs_m * -.4518461 + self.somecoll * 
                        self.coll_m * .0840205 + self.somecoll * self.grad_m * -.1141412 + self.somecoll * 
                        self.hs_m * -.1891053 + self.hs * self.coll_m * .0379579 + self.hs * self.grad_m * 
                        -.2498789 + self.hs * self.somecoll_m * -.0563838)
                else:
                    # calculating female utilty from education 
                    self.utMatch = math.exp( self.coll * self.grad_m * -.269892 + self.coll * self.somecoll_m * -.5563806 + 
                        self.coll * self.hs_m *  -1.013533 + self.grad * self.coll_m * -.0600776 + self.grad * self.somecoll_m *  
                        -.472227 + self.grad * self.hs_m * -.8916428 + self.somecoll * self.coll_m * .0710273 + self.somecoll * 
                        self.grad_m * -.0545339 + self.somecoll * self.hs_m * -.4597544 + self.hs * self.coll_m * .2146009 + 
                        self.hs * self.grad_m * .0507349 + self.hs * self.somecoll_m * .1953815)
                self.utMatch += random.normalvariate(  0.0, 0.01 )
                print 'self.id={0},agent={1},utmatch={2}'.format( self.id, agent.id, self.utMatch )
                self.utilityMatchList.append(self.utMatch)
            print "unsorted  uts: ",
            for u in self.utilityMatchList:
                print '{0} '.format( u ),
            print " "
            #sorted in decreasing order
            self.utilityMatchList = numpy.array(self.utilityMatchList)
            self.tmpSorted = self.utilityMatchList.argsort()[::-1]
            print "sorted  inds: ",
            for u in inds:
                print '{0} '.format( u ),
            print " "
            self.preferenceList = numpy.take(self.preferenceList,self.tmpSorted)
            self.preferenceList = list(self.preferenceList)
            print 'id={0}, sex={1}: '.format( self.id,self.sex ),
            for match in self.preferenceList:
                print '{0} '.format( match.id ),
#            print " 
            
            
        elif preference == "empirical-race":
            self.utilityMatchList = []
            del self.utilityMatchList[:]
            for agent in self.preferenceList:
                # reset all matches to 0 
                self.w_m = 0 
                self.b_m = 0
                self.h_m = 0
                self.a_m = 0
                if agent.race == '"white"': 
                    self.w_m = 1 
                elif agent.race == '"black"':
                    self.b_m = 1
                elif agent.race == '"hisp"':
                    self.h_m = 1
                else:
                    self.a_m = 1
                # calculate male/female utility from race
                if self.sex == "male":
                    utMatch = math.exp( -1.222833 * self.w * self.b_m + -.4127498 * self.w * self.h_m + -.4278895 * self.w * self.a_m +
                        -.2533814 * self.b * self.w_m + .0306185  * self.b * self.h_m + -.2026997 * self.b * self.a_m +
                        -.1799893 * self.h * self.w_m + -1.126189 * self.h * self.b_m + -.4095694 * self.h * self.a_m +
                        -.2638534 * self.a * self.w_m + -1.847398 * self.a * self.b_m + -.5392805 * self.a * self.h_m )
                else:
                    utMatch = math.exp( -1.037125 * self.w * self.b_m + -.7493691 * self.w * self.h_m + -1.317746 * self.w * self.a_m +
                        -1.695424 * self.b * self.w_m + -1.543998 * self.b * self.h_m + -1.815644 * self.b * self.a_m +
                        .2259415 * self.h * self.w_m + -.9436832 * self.h * self.b_m + -.674258 * self.h * self.a_m +
                        -.1182428  * self.a * self.w_m + -1.19147  * self.a * self.b_m + -.7880089 * self.a * self.h_m)
                self.utMatch += random.normalvariate(  0.0, 0.01 )
                self.utilityMatchList.append(utMatch)
            #sort by highest to lowest
            self.utilityMatchList = numpy.array(self.utilityMatchList)
            self.tmpSorted = self.utilityMatchList.argsort()[::-1]
            self.preferenceList = numpy.take(self.preferenceList,self.tmpSorted)
            self.preferenceList = list(self.preferenceList)

        elif preference == "empirical-all":
            self.utilityMatchList = []
            del self.utilityMatchList[:]
            for agent in self.preferenceList:
                if agent.edu <= 12:
                    self.hs_m = 1
                elif agent.edu > 12 and agent.edu < 16:
                    self.somecoll_m = 1 
                else: 
                    self.coll_m = 1
                    self.grad_m = 1
                if agent.race == '"white"': 
                    self.w_m = 1 
                elif agent.race == '"black"':
                    self.b_m = 1
                elif agent.race == '"hisp"':
                    self.h_m = 1
                else:
                    self.a_m = 1
                
            if self.sex == "male": 
                    utMatch = math.exp(self.coll * self.grad_m * -.2629087 + self.coll * self.somecoll_m *
                         -.3641229 + self.coll * self.hs_m * -.554391 + self.grad * self.coll_m * .0723642 + 
                         self.grad * self.somecoll_m * -.2395778 + self.grad * self.hs_m * -.4518461 + 
                         self.somecoll * self.coll_m * .0840205 + self.somecoll * self.grad_m * -.1141412 + 
                         self.somecoll * self.hs_m * -.1891053 + self.hs * self.coll_m * .0379579 + self.hs * 
                         self.grad_m * -.2498789 + self.hs * self.somecoll_m * -.0563838 + -1.222833 * self.w * 
                         self.b_m + -.4127498 * self.w * self.h_m + -.4278895 * self.w * self.a_m +  -.2533814 * 
                         self.b * self.w_m + .0306185  * self.b * self.h_m + -.2026997 * self.b * self.a_m + 
                         -.1799893 * self.h * self.w_m + -1.126189 * self.h * self.b_m + -.4095694 * self.h * 
                         self.a_m + -.2638534 * self.a * self.w_m + -1.847398 * self.a * self.b_m + -.5392805 * 
                         self.a * self.h_m )
            else:
                    utMatch = math.exp(self.coll * self.grad_m * -.269892 + self.coll * self.somecoll_m * -.5563806 + self.coll * self.hs_m *  

                                    -1.013533 + self.grad * self.coll_m * -.0600776 + self.grad * self.somecoll_m *  -.472227 + self.grad * 
                                    self.hs_m * -.8916428 + self.somecoll * self.coll_m * .0710273 + self.somecoll * self.grad_m * -.0545339 + 

                                    self.somecoll * self.hs_m * -.4597544 + self.hs * self.coll_m * .2146009 + self.hs * self.grad_m * .0507349
 + 
                                    self.hs * self.somecoll_m * .1953815  + -1.037125 * self.w * self.b_m + -.7493691 * self.w * self.h_m + -1.317746 * 
                                    self.w * self.a_m +  -1.695424 * self.b * self.w_m + -1.543998 * self.b * self.h_m + -1.815644 * self.b * self.a_m + 
                                    .2259415 * self.h * self.w_m + -.9436832 * self.h * self.b_m + -.674258 * self.h * self.a_m + -.1182428  * 

                                    self.a * self.w_m + -1.19147  * self.a * self.b_m + -.7880089 * self.a * self.h_m)
                    self.utMatch += random.normalvariate(  0.0, 0.01 )
                    self.utilityMatchList.append(utMatch)
            #sort by highest to lowest
            self.utilityMatchList = numpy.array(self.utilityMatchList)
            self.tmpSorted = self.utilityMatchList.argsort()[::-1]
            self.preferenceList = numpy.take(self.preferenceList,self.tmpSorted)
            self.preferenceList = list(self.preferenceList)
            
    def makeProposals(self):
        self.linkedTo.append(self.preferenceList[0])
        # append self to your potential's linked from list
        self.preferenceList[0].linkedFrom.append(self)
        
    def turnDownProposals(self, model):
        #keep the most attractive suitor (sort linkedFrom as preferences is sorted)
        self.tmpList = []         
        #create a new list that stores the indicies of each item in linkedFrom
        for agent in self.linkedFrom:
            #where in the preferenceList is this agent?
            self.tmpList.append(self.preferenceList.index(agent))
            #sort tmpList by preferenceList
       # print self.tmpList
        self.tmpList=sorted(self.tmpList)
       # print self.tmpList
        #remove myself from my rejected suitors' preference list
        for x in self.tmpList[1:]:
            self.preferenceList[x].preferenceList.remove(self)
            #reset suitor's linkedTo to nobody
            self.preferenceList[x].linkedTo = []
        #set linked from to be the most attractive agent if the suitor
        #passes the acceptability threshold
        if self.tmpList[0] <= model.acceptabilityCutoff:
            # keep the suitor
            self.linkedFrom = [self.preferenceList[self.tmpList[0]]]
        else:
            # get rid of the suitor
            self.preferenceList[self.tmpList[0]].preferenceList.remove(self)
            self.preferenceList[self.tmpList[0]].linkedTo = []
            self.linkedFrom = []
            
class marriageMarketModel():
    def __init__(self):        
        print "initializing marriage market model..."
        self.matchedAgentList = []
        self.allPrefTriedList = []        
        self.womenList = []        
        self.menList = []
        self.agentList = []
        self.stop = 0 
        self.time = 0 
        self.acceptabilityCutoff = self.cutPoint()                   
        self.createWomen()
        self.createMen()
        print "   computing preferences...preference=" + preference
        for item in self.agentList:
            item.computePreferences(self)
            
    def cutPoint (self):
        cutoff = acceptabilityThreshold * 0.01 
        #this is a direct translation from the netlogo code
        #num (or population) refers to count of only one sex (I think!)
        cutpoint = math.ceil(numWomen * cutoff)
        return cutpoint

    def createMen(self):
        print "   creating men..."
        if populationComposition == "2010-National":
            f=open('2010_men.txt')
            for x in xrange(numMen):
                file = f.readline()
                output = file.split(' ')
                self.createAgent("male", output[0], output[1], output[2], output[3], output[4])    
            f.close()
    
    def createWomen(self):
        print "   creating women..."
        if populationComposition == "2010-National":
            f=open('2010_women.txt')
            for x in xrange(numWomen):
                file = f.readline()
                output = file.split(' ')
                self.createAgent("female", output[0], output[1], output[2], output[3], output[4])    
            f.close()
    
    def createAgent(self, sex, age, income, race, edu, neverMarried):
        a = agent()
        a.sex = sex
        a.age = age
        a.income= income
        a.race = race
        a.edu = edu
        a.neverMarried = neverMarried
        if int(a.edu) <= 12:
            a.hs = 1
        elif int(a.edu) > 12 and a.edu < 16:
            a.somecoll = 1 
        else: 
            a.coll = 1
            a.grad = 1
        if a.race == '"white"': 
            a.w = 1 
        elif a.race == '"black"':
            a.b = 1
        elif a.race == '"hisp"':
            a.h = 1
        else:
            a.a = 1 
       #add new agent to lists        
        self.agentList.append(a)
        a.id = self.agentList.index(a)
        if a.sex == "male":
            self.menList.append(a)
        else:
            self.womenList.append(a)
            
    def step(self):
        self.time = self.time + 1
        if whoProposes == "men":
            if self.time % 2 == 0: 
                for agent in self.menList:
                    if ( len(agent.linkedTo) <= 0 and ( len(agent.preferenceList) > (numWomen - self.acceptabilityCutoff ) ) ):
                        agent.makeProposals()
            else: 
                for agent in self.womenList:
                   if len(agent.linkedFrom) > 0: 
                       agent.turnDownProposals(self)
        else:
            if self.time % 2 == 0:             
                for agent in self.womenList:
                    if (  len(agent.linkedTo ) <= 0 and ( len(agent.preferenceList) > (numWomen - self.acceptabilityCutoff ) ) ):
                        agent.makeProposals()
            else: 
                for agent in self.menList:
                    if ( len(agent.linkedFrom) > 0 ):
                        agent.turnDownProposals(self)
           
    def checkTime(self):
        #increment time and stop if everyone is married or all proposers have made
        #offers to all acceptable matches
        self.stop = 0
        self.lenPeople = len(self.womenList)
        del self.allPrefTriedList[:]
        del self.matchedAgentList[:]
        if whoProposes == "men":
            for woman in self.womenList:
                if ( len(woman.linkedFrom) > 0 ):
                    self.matchedAgentList.append(woman)
            for man in self.menList:  
                if ( ( len(man.preferenceList) <= numWomen - self.acceptabilityCutoff ) or len(man.linkedTo) > 0 ) :
                    self.allPrefTriedList.append(man)
           #women propose
        else:
            for man in self.menList:
                if len(man.linkedFrom) > 0 :
                    self.matchedAgentList.append(man)
            for woman in self.womenList:  
                if ( ( len(woman.preferenceList) <= numWomen - self.acceptabilityCutoff ) or len(woman.linkedTo) > 0 ) :
                    self.allPrefTriedList.append(woman)

        if len(self.allPrefTriedList) >= self.lenPeople:
            self.stop = 1
        elif len(self.matchedAgentList) >= self.lenPeople:
            self.stop = 1 
        print len(self.matchedAgentList)
        print len(self.allPrefTriedList)
    def writeOutput(self):
        filename = populationComposition + "-AcceptabilityThreshold=" + str(acceptabilityThreshold) + "-WhoProposes=" + whoProposes + "-Pref=" + preference    + ".txt"
        f = open(filename, 'w')
        f.write("sexR, raceR, eduR, posR, raceS, eduS, sexS, posS\n")
        if whoProposes == "men":
            for agent in self.womenList:
                if ( len(agent.linkedFrom) > 0 ):
                    posR = 1 + agent.preferenceList.index(agent.linkedFrom[0])
                    posS = numWomen - len(agent.linkedFrom[0].preferenceList) + 1 
                    prop = agent.linkedFrom[0]
                    #receiver writes out
                    f.write(agent.sex + ", " + agent.race + ", " + agent.edu + ", " + str(posR) + ", "+ prop.race + ", " + prop.edu + ", " + prop.sex + ", " + str(posS) + "\n")
                else: 
                    #forever alone :(
                    f.write(agent.sex + ", " + agent.race + ", " + agent.edu + "\n")
            for agent in self.menList:
                if len(agent.linkedTo) == 0:
                    f.write(agent.sex + ", " + agent.race + ", " + agent.edu + "\n")
        else:
            for agent in self.menList:
                if ( len(agent.linkedFrom) > 0 ):
                    posR = 1 + agent.preferenceList.index(agent.linkedFrom[0])
                    posS = numWomen - len(agent.linkedFrom[0].preferenceList) + 1 
                    prop = agent.linkedFrom[0]
                    #receiver writes out
                    f.write(agent.sex + ", " + agent.race + ", " + agent.edu + ", " + str(posR) + ", " + prop.race + ", " + prop.edu + ", " + prop.sex + ", " + str(posS) + "\n")
                else: 
                    #forever alone :(
                    f.write(agent.sex + ", " + agent.race + ", " + agent.edu + "\n")
            for agent in self.womenList:
                if len(agent.linkedTo) == 0:
                    f.write(agent.sex + ", " + agent.race + ", " + agent.edu + "\n")
        f.close()

if __name__=='__main__':
    myModel = marriageMarketModel()
    print "   running the model..."
    for x in xrange (0,20,1):
        while myModel.stop == 0: 
           myModel.step()
           if ( myModel.time % 2 == 1 ): 
               myModel.checkTime()
    myModel.writeOutput()
