#Import
from pymobility.models.mobility import reference_point_group
import rsa
import matplotlib.pyplot as plt
import math
import random
import rsa
import hashlib

latencyRecord = list()

#Class which encapsulates any messages

class networkMessage:
        def __init__(self,content,privkey,verification,pubkey):
                self.encryptedContent = rsa.encrypt(content, pubkey)
                self.senderInfo = rsa.sign(verification, privkey, 'MD5')
                m = hashlib.sha224()
                m.update(self.encryptedContent)
                self.hash = m.digest()  #May contain non-ASCII characters
        def getContent(self, privKey):
                return rsa.decrypt(self.encryptedContent, privKey)
        def verifySender(self, usrVer, pubkey):
                return rsa.verify(usrVer, self.senderInfo, pubkey)
        def getHash(self):
                return self.hash

#Class for virtual network devices being simulated

class networkDevice:
        def __init__(self, friendlyName, verification):
                self.friendlyName = friendlyName
                self.ver = verification
                print self.friendlyName
                self.setKeys()              #This takes more processing
                self.wirelessOff()
                self.randstep = random.randrange(3)
                self.randcounter = 0
                self.counter = 0
                self.wirelessRestPeriod = 4
                self.wirelessOnPeriod = 2
                self.firstToggle = False
                self.messageQueue = []

                self.wireless = False
                self.neighbors = []
                self.location = (0,0)
                self.addressBook = dict()
                self.postboxStatus = False
                self.subscriptions = []
                self.postboxMessages = []
                self.personalMessages = []
                self.msearches = 2
                
                #raw_input("MAILBOX SEARCHES VAR HAS BEEN RESET!!!!!!")

        def next_step(self):
                #Print out whether node is a mailbox
##                print "Device", self.getName(), "has mailbox status", self.postboxStatus
                
                #Print out personal messages
##                print "Messages for device", self.getName()
                pmsgs = self.personalMessages
##                for i in pmsgs:
##                    print i.getContent(self.priv)
                

                #Print out mailbox messages
                if self.postboxStatus:
##                    print "Mailbox messages by hash for device", self.getName()
                    mailbox = self.getPostboxMessages()
##                    for i in mailbox:
##                        print i.getHash()

                #Print out message queue
##                print "Message queue for device", self.getName()
                mqueue = self.messageQueue
##                for i in mqueue:
##                    print i.getHash()

                #Print out subscriptions
##                print "Subscriptions for device", self.getName()
                subs = self.getSubscriptions()
##                for i in subs:
##                        print i.getName()

##                print " __________ "
##                raw_input("Press Enter to Continue")

                #--------------------------------------------------------------------------
            
                if self.postboxStatus:
                    if self.wireless == False:
                        self.wirelessOn()
                elif self.randcounter == self.randstep and self.firstToggle == False:
                    self.wirelessOn()
                    self.firstToggle = True
                elif self.wireless:
                    self.counter += 1
                    if self.counter % self.wirelessOnPeriod == 0:
                        self.wirelessOff()
                        self.counter = 0
                elif self.randcounter != self.randstep and self.firstToggle == False:
                    self.randcounter += 1
                    #print str(self.randcounter) + "/" + str(self.randstep)
                    #raw_input("PETC")
                else:
                    self.counter += 1
                    if self.counter == self.wirelessRestPeriod:
                        self.wirelessOn()
                        
        def wirelessOn(self):
##                1. Set wireless flag to True
##                2. searchSurrounding()
##                3. updateSubscriptions()
##                4. pollSubscriptions()
##                5. Post messages in message queue
##                6. Reset message queue
##                7. mailbox -> updatePostbox()

##                print "Mailbox search var:", self.mailboxSearches
    
                self.wireless = True

                self.searchSurrounding()
                self.updateSubscriptions()
                self.pollSubscriptions()

                m = self.getMsgQueue()
                if len(self.getSubscriptions()) > 0:
                        for i in m:
                                for j in self.getSubscriptions():
                                        j.addToPostbox(i)

                        #Reset message queue
                        self.messageQueue = []
##                else:
##                        print "No available mailboxes"

                if self.postboxStatus:
                        self.updatePostbox()

        def wirelessOff(self):
                self.wireless = False

        def setKeys(self):
                (pub, priv) = rsa.newkeys(512)
                self.pub = pub
                self.priv = priv
        def getPublicKey(self):
                return self.pub
        def generateMessage(self, content, friendly):
                #__init__(self,content,privkey,verification,pubkey)
                newMsg = networkMessage(content, self.priv, self.ver, self.addressBook[friendly])
                self.messageQueue.append(newMsg)
                return newMsg
        def getMsgQueue(self):
                return self.messageQueue
        def addToAddress(self, friendly, key):
            if friendly in self.addressBook:
                return False
            else:
                self.addressBook.update({friendly : key})
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
                for i in self.neighbors:
                        if i.getPostboxStatus():
                                available.append(i)
                mimCount = 0

                if available == []:
                        #There are no neighboring mailboxes available
                        #You should check if other neighbors are subscribed to things
                        #If they are, then htu (hit them up) & get them to be a man in the middle mailbox
                        for i in self.neighbors:
                                if i.getWireless():
                                        if i.getSubscriptions() != []:
                                                i.requestMailbox()
##                                                raw_input("Requsted a mailbox!")
                                                mimCount += 1
                                                networkDevice.mailboxSearches = 0

                        if mimCount == 0:
                            #print "Mailbox Searches: ", str(self.mailboxSearches)
                            #There are no man in the middle opportunities, you should become a mailbox
                            if self.mailboxSearches == 3:
                                self.postboxStatus = True
                                #raw_input("Became a mailbox!")
                                networkDevice.mailboxSearches = 0
                            else:
##                                print "Previous mailboxvar", str(self.mailboxSearches)
                                #networkDevice.mailboxSearches += 1
                                networkDevice.mailboxSearches += 1
##                                self.msearches = self.msearches + 1
##                                print "Mailbox incremented to", str(self.mailboxSearches)
##                                print "Other var is", str(self.msearches)
                            #print "Mailbox is", str(self.mailboxSearches)

                        else:
                            networkDevice.mailboxSearches = 0
                            #print "WHY DONT UUUUUU???"
                            #raw_input()

                else:
                        #There are neighboring mailboxes available
                        #You should subscribe
                        networkDevice.mailboxSearches = 0
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

        def pollSubscriptions(self):
                #Gets messages from subscribed devices
                #Checks if messages can be opened
                #Delete if not yours
                for i in self.subscriptions:
                        #Get postbox messages
                        full = i.getPostboxMessages()
                        #Sort them
                        personal = list()
                        for j in full:
                                try:
                                        j.getContent(self.priv)
                                        personal.append(j)
                                except:
                                        pass
                        #Delete the old list
                        full = []

                        pmsgs = self.personalMessages
                        pmsgsHashes = []
                        for n in pmsgs:
                                pmsgsHashes.append(n.getHash)
                        for n in personal:
                                if n.getHash not in pmsgsHashes:
                                        self.personalMessages.append(n)
                                            
                #If you are a mailbox grab from your own
                personal = []
                for i in self.postboxMessages:
                    try:
                        i.getContent(self.priv)
                        personal.append(i)
                    except:
                        pass

                for n in personal:
                    self.personalMessages.append(n)
                    

        def updatePostbox(self):
                #If you are a postbox then sync with other postboxes
                self.updateHashList()
                for i in self.subscriptions:
                        full = i.getPostBoxMessages()
                        for j in full:
                                if j.getHash() not in self.hashes:
                                        #Not a duplicate
                                        self.postboxMessages.append(j)

        def addToPostbox(self, msg):
                self.updateHashList()
                if msg.getHash() not in self.hashes:
                        self.postboxMessages.append(msg)


        def getPostboxMessages(self):
                return self.postboxMessages

        def updateHashList(self):
                #Update list with hashes from messages to determine duplicates
                self.hashes = []
                msgs = self.getPostboxMessages()
                for i in msgs:
                        self.hashes.append(i.getHash())

        def getWireless(self):
                return self.wireless

        def checkTestMessage(self, content):
            pmsgs = self.personalMessages
            for i in pmsgs:
                #Check for the test message content
##                print "Checking for content match"
##                print i.getContent(self.priv)
                #raw_input("!!!!!!!")
                if i.getContent(self.priv) == content:
                    return True
            return False

        mailboxSearches = 0

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
                        self.devices[i].next_step()
                #self.print_locations()
                self.plot_locations(q)

                #Find and update neighbors of each device
                self.cluster1()

                self.latencyCheck()
        
        def print_locations(self):
                for i in range(self.numNodes):
                        print self.devices[i].getLocation()
        def plot_locations(self, b):
                postbox_x = []
                postbox_y = []

                wireless_x = []
                wireless_y = []
        
                other_x = []
                other_y = []

                for i in range(self.numNodes):
                    if self.devices[i].getPostboxStatus():
                        node_pos = self.devices[i].getLocation()
                        postbox_x.append(node_pos[0])
                        postbox_y.append(node_pos[1])
                    elif self.devices[i].wireless == True:
                        node_pos = self.devices[i].getLocation()
                        wireless_x.append(node_pos[0])
                        wireless_y.append(node_pos[1])
                    else:
                        node_pos = self.devices[i].getLocation()
                        other_x.append(node_pos[0])
                        other_y.append(node_pos[1])
                        
                plt.plot(postbox_x, postbox_y, 'ro', color='b')

                plt.plot(other_x, other_y, 'ro', color='g')

                plt.plot(wireless_x, wireless_y, 'ro', color='r')

                #plt.show()

                #print "Wireless"

                #for i in wireless_x:
                #   print i


                #raw_input("Press enter to continue")

                plt.savefig(str(b)+'.png')

                plt.clf()

                #raw_input()

        def testMessaging(self):
                #Start counter
                self.latencyCounter = 0
            
                #Associating two nodes
                r1 = random.randrange(len(self.devices))
                r2 = random.randrange(len(self.devices))
                
                while r2 == r1:
                    r2 = random.randrange(len(self.devices))
                d1 = self.devices[r1]
                d2 = self.devices[r2]
                d1.addToAddress(d2.getName(), d2.getPublicKey())
                d2.addToAddress(d1.getName(), d1.getPublicKey())

                #Initating message send from d1 to d2

##                print "ASSOCIATING NODES!!"
                self.randcontent = str(random.randrange(10000))
                msg = d1.generateMessage(self.randcontent, d2.getName())
                #raw_input("Acknowledge to continue")

                #Save devices
                self.tD1 = d1
                self.tD2 = d2

##                print "Generated message hash:", msg.getHash()


        def latencyCheck(self):
            #Check if D2 has recieved the message
            #raw_input("LATENCY CHECK!")
##            print "Device name:", self.tD2.getName()
##            print "Origin device name:", self.tD1.getName()
            if self.tD2.checkTestMessage(self.randcontent) == False:
                self.latencyCounter += 1
##                print "Didn't get it yet"
            else:
                print "Message recieved!"
                for n in range(10):
                        print "!!!!!!!!!!!!!"
                print self.latencyCounter, " counts"
                mailboxnum = 0
                for i in self.devices:
                        if i.postboxStatus:
                                mailboxnum += 1
                latencyRecord.append([self.latencyCounter, mailboxnum])
                self.latencyCounter = 0
                self.tD2.personalMessages = []
                #raw_input("Press enter to continue")
                self.testMessaging()
            #raw_input("End latency check")
                
        def cluster1(self):
                #Cluster mode 1
                #Wifi-Direct 656 Feet - 199 Meters
                for i in self.devices:
                        #only update surrounding devices for devices with wireless turned on
                        if i.getWireless():
                                l = list()
                                #print "//" + str(i.getName())
                                for j in self.devices:
                                        #print "*" + str(j.getName())
                                        if j != i:
                                                jloc = j.getLocation()
                                                iloc = i.getLocation()
                                                #print math.sqrt(math.pow((jloc[0]-iloc[0]),2)+math.pow((jloc[1]-iloc[1]),2))
                                                if math.sqrt(math.pow((jloc[0]-iloc[0]),2)+math.pow((jloc[1]-iloc[1]),2)) < 199 and j.getWireless():
                                                        l.append(j)
                                i.updateSurroundingDevices(l)
                #All clusters added
                #Do something now
                #for i in self.devices:
                       #print "Device", i.getName()
                       #for n in i.getSurroundingDevices():
                               #print n.getName()
                       #print "----------"
                       #raw_input("Press enter for next device.")

        latencyCounter = 0
        tD1 = 0
        tD2 = 0

def supertest():
    net = network("Supertest", 5, (10,10))
    net.testMessaging() 
    for i in range(30):
        net.next_step(i)
    print "Latency Record"
    for i in latencyRecord:
            print i

def test():
        net = network("Test", 20, (70, 70))
        net.testMessaging()
        for i in range(100):
                print i
                net.next_step(i)
        print "Latency Record"
        for i in latencyRecord:
                print i

def hackensack1():
        net = network("Net", 9462, (3379.62,3379.2))
        net.testMessaging()
        for i in range(10):
                net.next_step(i)
                print "Next", i

def main():
        print "1. Test\n2. Hackensack1\n3. Supertest"
        select = raw_input("Enter network to simulate")
        if select == '1':
                raw_input("Test")
                test()
        elif select == '2':
                raw_input("Hackensack1")
                hackensack1()
        elif select == '3':
                raw_input("Super Test")
                supertest()

main()

raw_input()
