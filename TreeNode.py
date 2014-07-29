
# coding: utf-8

# In[1]:

class TreeNode(object):
    lstWord = []# static variable, store the sentence word by word
    lstLevel = [] 
    
    # the treenode is defined upon a list of words(lstW), here we only store the indx of the word of this treenode. 
    # each treenode has one father and a list of sons, which all stored as indx upon a list of words
    def __init__(self, indx, father, sons):
        self.indx = indx
        self.father = father
        self.sons = sons
        self.POS 
    def addChild(self,indx_newsons):
        #check if there is duplicate,                    
        
        if indx_newsons in self.sons:
            return 0 # there is this son already\n",
        else:
            self.sons.append(indx_newsons)
            return 1 # append successfully\n",
    def removeChild(self,indx_delsons):
        try:
            self.sons.remove(indx_delsons)                
        except :
            print "there is no such indx to be deleted\n",
    def getData(self):
        try:
            return TreeNode.lstWord[self.indx] # return the real word\n",
        except IndexError:
            print "there is no such indx in lstWord"
    

# tn = TreeNode(1,1,[2])
# TreeNode.lstWord = [2,3,4]
# tn.removeChild(3)
# print tn.getData(-1)
# print tn.sons
# print "keep doing"


# In[7]:

import sys

class DepGram:
    # the father class of hwc, and ff
    lstWord = []# static variable, store the sentence word by word
    lstLevel = [] # static variable, store the level of each word ( index)
    lstPOSTag = []
    lstStanfordDepTag =[]
    
    def __init__(self,positions,DepGramType):
        
        #positions is a list of list ( there might be a lot of occurance of these words) 
        #...which stored the position of each appearance of the words 
        #...( it should be sorted, so each elements(list) should be unique)
        self.key = ' '.join([DepGram.lstWord[i] for i in positions]) #  join the words by a space, used as the dictionary key
        
        self.HWCcount = 0
        self.FIXcount = 0
        self.FLOATcount = 0
        self.Totalcount = 0
        self.positions = []
        self.levels = []
        self.POSTags = []
        self.StanfordDepTags = []
        
        self.addOne(positions, DepGramType)#increase the according counter
         
    def addOne(self,newIndxSeq,DepGramType):
        #DepGramType is a link type: Headwordchain or Fixed or Floating
        ALLTYPES = ['HWC','FIX','FLT']
        if DepGramType == 'HWC':
            self.HWCcount += 1 # how many times this link occurs
        elif DepGramType == 'FIX':
            self.FIXcount += 1
        elif DepGramType == 'FLT':
            self.FLOATcount += 1
        
        self.positions.append(newIndxSeq)
        self.levels.append([DepGram.lstLevel[i] for i in newIndxSeq])
        self.POSTags.append([DepGram.lstPOSTag[i] for i in newIndxSeq])
        self.StanfordDepTags.append([DepGram.StanfordDepTags[i] for i in newIndxSeq])
        self.Totalcount += 1
        
class Tree:
    "build tree, hwc link, ff ngram"
    def __init__(self,datablock):
        self.datablock = datablock # store the each line of the stanford dep tree as a string in a list
        self.tree = [] # list has to be initialized, each elements are treanode
        #build tree from datablock of stanford dep format
        self.nodenumber = len(self.datablock)
        # the original form of the tree (in the stanford dep tree format) was each word has a link to its father
        # ... we need to go through these word and reverse the link
        #... the self.tree is a list to store each TreeNode in the sentence order
        #... the following loop first initial the self.tree with empty father and sons
        
        TreeNode.lstWord = [] # the following four lines are important
        TreeNode.lstLevel = []
        
        DepGram.lstWord = []
        DepGram.lstLevel = [] 
        DepGram.lstPOSTag = []
        DepGram.lstStanfordDepTag = []
        
        
        for it in xrange(self.nodenumber):            
            
            self.tree.append(TreeNode(it,self.getFather(it))
            TreeNode.lstWord.append(self.getWord(it))
           
            DepGram.lstWord.append(self.getWord(it))
            DepGram.lstLevel.append(0)# initialize of the lstLevel
            DepGram.lstPOSTag.append(self.getPOS(it))
            DepGram.lstStanfordDepTag.append(self.getStanfordDep(it))
            
        # the following loop add the sons to each TreeNode
        for it in xrange(self.nodenumber):
            if self.getFather(it) == -1:#is it the root?
                self.rootindx = it
            else:
                self.tree[self.getFather(it)].addChild(it)
        
        self.treeroot = self.tree[self.rootindx]
        self.glob_link = [0]*self.nodenumber# set the maximum possible length of a link
        self.dicDepGram = {}
        
        self.preorderTraverse4Level(self.treeroot,0)# to add the level information
    
# the format is something like:  residents   NNS 4   PMOD       
    def getFather(self,it):
         # the indx of stanford is start at 1, the root is fathered by 0, so we need to minus it by 1
        return int(self.datablock[it].split("\t")[2]) - 1
    def getPOS(self,it):
        return elf.datablock[it].split("\t")[1]
    def getStanfordDep(self,it):
        return elf.datablock[it].split("\t")[3]
    def getWord(self,it):
        return self.datablock[it].split("\t")[0]
      
    def getFixedFloating(self,rootNode,DepGramLength,currentDepth):
        #return all the fixed structrue as a dictionary that use the DepGram.words as the key and DepGram as the value
        if rootNode == None : 
            return
        
        # get all the child of the current rootnode
        # find all the combination of 2 children of rootnode
        # make them the new Fixed/Floating/newFixed/newFloating link
 
        for sonindx1 in range(0,len(rootNode.sons)):
            subtree1 = self.getSubtree(self.tree[sonindx1])
           for sonindx2 in range(sonindx1, len(rootNode.sons)):
                subtree2 = self.getSubtree(self.tree[sonindx2])
                if canbeFixed(subtree1,subtree2):
                    self.makeDepGram(sorted([subtree1,subtree2,rootNode.indx]), 'FIX')
                if canbeFloating(subtree1,subtree2) :
                    self.makeDepGram(sorted([subtree1,subtree2]),'FLT')
            
        #new fixed and new floating are structures that does not use the whole subtrees
        # lol means a list of list
        lolAllSubSets = findAllSubsets(rootNode.sons)
        for size in range(1,DepGramLength+1) :
            for subset in lolAllSubSets :
                if len(subset) == size - 1 :
                    self.makeDepGram(sorted([subset,rootNode.indx]) , 'NFIX')
                if len(subset) == size:
                    self.makeDepGram(sorted([subset]),'NFLT')
       
       
        for sonNodeIndx in rootNode.sons :
            self.getFixed(self.tree[sonNodeIndx], DepGramLength, currentDepth+1)
        pass
    def getFloating(self):
        #return all the floating structrue as a dictionary that use the DepGram.words as the key and DepGram as the value
        pass
    def preorderTraverse4Level(self,rootNode,level):
        if rootNode == None :
            return
        
        #add the lstLevel 
        DepGram.lstLevel[rootNode.indx] = level
        if len(rootNode.sons) == 0:
            return
        for son in rootNode.sons :
            self.preorderTraverse4Level(self.tree[son],level+1)
        
    def mergeAllDepGram(self):
        #merge the tree dictionary(hwc, fixed, floating) and modify the DepGram.DepGramType
        pass
    def printTree(self, rootNode, prefix , istail):
        token = "└── " if istail else "├── "
        print prefix+token+rootNode.getData()
        if len(rootNode.sons) > 0 :
            for childindx in rootNode.sons[0:-1]: # all but the last one
                self.printTree(self.tree[childindx], prefix + ("    " if istail else "│   "),False)
            #if len(rootNode.sons)>=1:
            self.printTree(self.tree[rootNode.sons[-1]], prefix + ("    " if istail else "│   "), True)
    def getHeadWordChain(self,rootNode,HWCLength,currentDepth):
        "return all the hwc structrue as a dictionary that use the DepGram.key as the key and DepGram as the value"
        if rootNode == None : 
            return
        
        self.glob_link[currentDepth] =  rootNode.indx
        
        for l in range(0,min(HWCLength,currentDepth+1)) :#currentDepth is start from 0, so we need to add one here
            #start from current node and trace back 
            newIndxSeq = sorted(self.glob_link[currentDepth - l : currentDepth + 1 ])
            
            self.makeDepGram(newIndxSeq,'HWC')
       
        for sonNodeIndx in rootNode.sons :
            self.getHeadWordChain(self.tree[sonNodeIndx], HWCLength, currentDepth+1)
            
    def makeDepGram(self,newIndxSeq,DepGramType) :
        # add the new depgram into the dictionary with the type
        #get the key (the actuall word sequece)
        key = ' '.join([DepGram.lstWord[indx] for indx in newIndxSeq])
            #if this key is new, we should creat a term in our dictionary
        if self.dicDepGram.get(key) == None :
            self.dicDepGram[key] =  DepGram(newIndxSeq,DepGramType)
            #else we should increase the according 
        else:
            self.dicDepGram[key].addOne(newIndxSeq,DepGramType)
 
            
#test
f = open('test1.ref','r')

datablock = []
for line in f:
    #sys.stdout.write(line)    
    line = line[0:-1]
    #print line
    
    if line != "":# whenever see an empty line, start building a tree, the last line of the file is an empty line
        datablock.append(line)
    else:
        print ">>>>>>>>>>>>"
        t = Tree(datablock)
        t.printTree(t.treeroot,"",False)
        #t.preorderTraverse(t.treeroot)
        t.getHeadWordChain(t.treeroot,3,0)
        for key in sorted(t.dicDepGram):
            print "%s: %s: %s : %s" % (key, t.dicDepGram[key].Totalcount, t.dicDepGram[key].positions, t.dicDepGram[key].levels)
        datablock = [] 
    
    


# In[ ]:




# In[ ]:



