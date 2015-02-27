'''
@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

Functions to manipulate and convert to Hash array
the scores. 

It is useful for aligning measures (not single notes)

'''
from music21 import stream
from music21 import note
from music21 import omr
# FastAlignmentArrays is a Cython library
from Alignment import FastAlignmentArrays
from MeasureFunctions import MeasureFunctions

class HashFunctions:
    
    def alignHash(self,hashArray):
        '''
        Returns two hash arrays aligned
        
        Uses the needleman-wunsh algorithm evaluating the differences between measures
        '''
        faa=FastAlignmentArrays()
        hashOrdered=faa.needleman_wunsch(hashArray[0], hashArray[1],False)[0]
        hashArray[0]=hashOrdered[0]
        hashArray[1]=hashOrdered[1]
        return hashArray
    
    def getHash(self,OMR):
        '''
        Returns hash from a group of OMR parts
        '''
        print "...Obtaining Hash of measures..."
        hashArray=[]
        for i in range(len(OMR)):
            hashArray.append(self.getHashArrayFromPart(OMR[i].parts[0]))
        return hashArray
    
    def getGapsFromHashArray(self,hashArray):
        '''
        Returns the gap index array from a group of hash parts
        '''
        gapsArrays=[]
        for i in range(len(hashArray)):
            gapsArray=[]
            for j in range(len(hashArray[i])):
                symbol=hashArray[i][j]
                if symbol=="*":
                    gapsArray.append(j)
            
            gapsArrays.append(gapsArray)   
        return gapsArrays
    
         
 
        
    def reconstructHash(self,OMR,hashArray):  
        '''
        Returns a group of single parts ordered by hashArray (gaps)
        '''
        scores=[]
        gapsArr=[]
        mf=MeasureFunctions()
        for i in range(len(OMR)):
            print len(hashArray[i])
            partReconstruct,gaps=mf.reconstructScore(OMR[i].parts[0], hashArray[i])
            sc=stream.Score()
            sc.append(partReconstruct)
            scores.append(sc)
            gapsArr.append(gaps)
        return scores,gapsArr
        
    
      

    def removeHashGaps(self,partHash):
        '''
        Removes gaps in a part
        '''
        newHash=[]
        for i in range(len(partHash)):
            if(partHash[i]!="*"):
                newHash.append(partHash[i])
        return newHash
    
    def addHashGaps(self,partHash,gaps):
        '''
        Insert gaps in a part
        '''
        for gap in gaps:
            partHash.insert(gap,"")
        return partHash    
    
        
    def getHashArrayFromPart(self,part):
        '''
        get Hash string of a Part (music21)
        '''
        hashArray=[]
        lengthArray=len(part.getElementsByClass(stream.Measure))
        for i in range(lengthArray):
            measure=part.getElementsByClass(stream.Measure)[i]
            hashMeasure=self.getHashFromMeasure(measure)
            pitchArr=""
            for mynote in measure.flat.getElementsByClass(note.Note):
                pitchArr+=str(mynote.pitch.name)
            hashArray.append(pitchArr+"_"+hashMeasure)
        return hashArray
    
    def getHashFromMeasure(self,measure):
        '''
        get Hash string of a measure. Library correctors.py of Michael Scott Cuthbert. Project OMR
        '''
        mh=omr.correctors.MeasureHash(measure).getHashString()
        return mh
    