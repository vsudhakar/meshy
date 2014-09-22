#Import
from pymobility.models.mobility import reference_point_group
import rsa
import matplotlib.pyplot as plt
import math
import random

#Class which encapsulates any messages

class networkMessage:
        def __init__(self,content,privkey,verification,pubkey):
                self.encryptedContent = rsa.encrypt(content, privkey)
                self.senderInfo = rsa.sign(verification, privkey, 'MD5')
        def getContent(self, privKey):
                return rsa.decrypt(self.encryptedContent, privKey)
        def verifySender(self, usrVer, pubkey):
                return rsa.verify(usrVer, self.senderInfo, pubkey)

#Class for virtual network devices being simulated

class networkDevice:
        def __init__(self, friendlyName, verification):
                self.friendlyName = friendlyName
                self.ver = verification
                print self.friendlyName
                self.setKeys()              #This takes more processing
        def setKeys(self):
                (pub, priv) = rsa.newkeys(512)
                self.pub = pub
                self.priv = priv
        def getPublicKey(self):
                return self.pub
        def generateMessage(self, content, friendly):
                newMsg = networkMessage(content, self.priv, self.ver, addressBook[friendly])
                self.messageQueue.append(newMsg)
        def getMsgQueue(self):
                return self.messageQueue
        def addToAddress(friendly, key):
            if friendly in addressBook:
                return False
            else:
                self.messageQueue.update({friendly : key})
                return True
        def elevateDevice(self):
            self.postBoxStatus = True
        def setLocation(self, location):
                #Location provided as a tuple from network class
                self.location = location
        def getPostboxStatus(self):
                return self.postboxStatus
        def getSubscriptions(self):
                return self.subscriptions
        def getLocation(self):
                return self.location
        def getSurroundingDevices(self):
                return self.neighbors
        def updateSurroundingDevices(self, l):
                self.neighbors = l
        def getName(self):
                return self.friendlyName
        def searchSurrounding(self):
                #Look through list to see if anyone has postboxStatus as True
                available = list()
                for i in neighbors:
                        if i.getPostboxStatus():
                                available.append(i)

                if available == []:
                        #There are no neighboring mailboxes available
                        #You should check if other neighbors are subscribed to things
                        #If they are, then htu (hit them up) & get them to be a man in the middle mailbox
                        for i in neighbors:
                                if i.getSubscriptions() != []:
                                        i.requestMailbox()
                        
                else:
                        #There are neighboring mailboxes available
                        #You should subscribe
                        for i in available:
                                self.subscriptions.append(i)
        def requestMailbox(self):
                # Become a mailbox (50/50 chance)
                rand = random.randrange(1)
                if rand == 0:
                        self.postboxStatus = True
                
        def updateSubscriptions(self):
                for i in range(len(self.subscriptions)):
                        if self.subscriptions[i] not in self.neighbors:
                                self.subscriptions.pop(i)
        neighbors = list()
        location = (0,0)
        messageQueue = list()
        addressBook = dict()
        postboxStatus = False
        subscriptions = list()

#Class for network sandbox

class network:
        def __init__(self, name, numNodes, dim):
                self.name = name
                self.numNodes = numNodes
                self.mobility = reference_point_group(numNodes, dimensions=dim, velocity=(0.1, 1.0))
                pos = next(self.mobility)
                self.devices = list()
                for i in range(numNodes):
                        self.devices.append(networkDevice(i, "Roger"))
                        self.devices[i].setLocation(pos[i])
        def next_step(self, q):
                pos = next(self.mobility)
                for i in range(self.numNodes):
                        self.devices[i].setLocation(pos[i])
                #self.print_locations()
                self.plot_locations(q)

                #Find and update neighbors of each device
#               self.cluster1()
                
        def print_locations(self):
                for i in range(self.numNodes):
                        print self.devices[i].getLocation()
        def plot_locations(self, b):
                x = list()
                y = list()
                for i in range(self.numNodes):
                        node_pos = self.devices[i].getLocation()
                        x.append(node_pos[0])
                        y.append(node_pos[1])
                #print x
                #print y
                plt.plot(x,y,'ro')
                #plt.show()

                plt.savefig(str(b)+'.png')

                plt.clf()

                #raw_input()

        def cluster1(self):
                #Cluster mode 1
                #Wifi-Direct 656 Feet - 199 Meters
                for i in self.devices:
                        l = list()
                        print "//" + i.getName()
                        for j in self.devices:
                                print "*" + j.getName()
                                if j != i:
                                        jloc = j.getLocation()
                                        iloc = i.getLocation()
                                        #print math.sqrt(math.pow((jloc[0]-iloc[0]),2)+math.pow((jloc[1]-iloc[1]),2))
                                        if math.sqrt(math.pow((jloc[0]-iloc[0]),2)+math.pow((jloc[1]-iloc[1]),2)) < 199:
                                                l.append(j)
                        i.updateSurroundingDevices(l)
                #All clusters added
                #Do something now
                for i in self.devices:
                       print "Device", i.getName()
                       for n in i.getSurroundingDevices():
                               print n.getName()
                       print "----------"
                       raw_input("Press enter for next device.")

                                                
                        
def test():
        net = network("Test", 20, (70, 70))

        for i in range(10):
                net.next_step(i)                

def hackensack1():
        net = network("Net", 9462, (3379.62,3379.2))

        for i in range(10):
                net.next_step(i)
                print "Next", i
                
def main():
        print "1. Test\n2. Hackensack1"
        select = raw_input("Enter network to simulate")
        if select == '1':
                raw_input("Test")
                test()
        elif select == '2':
                raw_input("Hackensack1")
                hackensack1()

main()

raw_input()
