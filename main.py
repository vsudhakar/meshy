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
		(pub, priv) = rsa.newkeys(512)
		self.pub = pub
		self.priv = priv
		self.ver = verification
		print self.friendlyName
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
        messageQueue = list()
        addressBook = dict()
        postboxStatus = False
