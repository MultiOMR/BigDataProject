'''
Created on 10/11/2014

@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

Functions related to the full score alignment.
It takes the n parts and align with the best omr full score
for the missing rest measuress
'''
from music21 import converter
from music21 import stream
from Functions import HashFunctions
from Functions import FilesFunctions


class FullScoreAlignment:
    '''
    Class for the full score alignment
    
    usage:
    
    fsa=FullScoreAlignment()   
    idCompleteScoreBetter=fsa.getIdBetterOMRFullScore(fsOMRs,partsNumber)
    finalScore=fsa.runSynchronisingMeasuresNJ(subdirnameFullScore,subdirnameParts,fsOMRs[idCompleteScoreBetter])  
    finalScore.write("musicxml", dirGeneral+'/finalScore.xml')   
        
    '''
    def runSynchronisingMeasuresNJ(self,subdirnameParts,completeScore):
        '''
        This function takes the different result.S2.xml files to construct
        the final output.
        
        Example:
        fsa=FullScoreAlignment()   
        idCompleteScoreBetter=fsa.getIdBetterOMRFullScore(fsOMRs,partsNumber)
        finalScore=fsa.runSynchronisingMeasuresNJ(subdirnameFullScore,subdirnameParts,fsOMRs[idCompleteScoreBetter])  
        finalScore.write("musicxml", dirGeneral+'/finalScore.xml')   
        '''

        gapOMRs=[]
        parts=[]
        completeScoreParts=[]
        
        # Convert to Hash the better full score
        hf=HashFunctions()
        for p in completeScore.getElementsByClass(stream.Part):
            sc=stream.Score()
            sc.append(p)
            completeScoreParts.append(sc)
        completeScoreHash=hf.getHash(completeScoreParts)

        # Convert to hash the parts
        for dirname in sorted(subdirnameParts):
            print "--- ",dirname
            path = dirname+"/XML/"
            partId=int(dirname.split('\\')[-1])
            print partId
            resultS2File=path+ "result.S2.xml"
            resultS2=converter.parse(resultS2File,forceSource=False)
            parts.append(resultS2)
        partsHash=hf.getHash(parts)   


        for partHash in partsHash:
            index=partsHash.index(partHash)
            h=[]
            h.append(partHash)
            h.append(completeScoreHash[index])
            hf.alignHash(h)
            partsHash[index]=h[0]
            completeScoreHash[index]=h[1]

            gaps=hf.getGapsFromHashArray(h)
            gapOMRs.append(gaps)
            if(index<len(partsHash)-1):
                nextPart=completeScoreHash[index+1]
                for gap in gaps[1]:
                    nextPart.insert(gap,"*")

        print "--------------trace back-----------"
        print gapOMRs
        sc=stream.Score() 
        gaps=gapOMRs[len(partsHash)-1][1]
        for i in range(len(partsHash)-1):
            completeScoreHash[i]=hf.removeHashGaps(completeScoreHash[i])
            completeScoreHash[i]=hf.addHashGaps(completeScoreHash[i],gaps)
            partsHash[i]=hf.removeHashGaps(partsHash[i])
            h=[]
            h.append(partsHash[i])
            h.append(completeScoreHash[i])
            
            h=hf.alignHash(h)
            partsHash[i]=h[0]
            completeScoreHash[i]=h[1]
             
        print "--------------reconstruct scores-----------" 
         
        streams,gaps=hf.reconstructHash(parts,partsHash)
        for s in streams:
            part=s.getElementsByClass(stream.Part)[0]
            sc.append(part)
        return sc
        
                              
    
    def getIdBetterOMRFullScore(self,fsOMRs_files,partsNumber):
        '''
        Tries to obtain the best full omr score
        based on the parts and the length.
        
        Omrs increase the part numbers and add new rest measures
        to synchronize
        
        usage:
        # fsOMRs is an array with the  full score omrs
        # for string quartet, 4 parts
        idCompleteScoreBetter=fsa.getIdBetterOMRFullScore(fsOMRs,4)
        
        
        '''
        print "---------Calculating better OMR for alignment------------"
        ff=FilesFunctions()
        measuresLengthBetter=1000000 #maximum
        partsLengthBetter=1000 #maximum
        idCompleteScoreBetter=1000 #maximum
        for cs_file in fsOMRs_files:
            cs=ff.getOMR(cs_file)
            if cs!=[]:
                try: 
                    isEqualParts=False
                    isLessMeasures=False
                    isBetterOMR=False
                    idCompleteScore=fsOMRs_files.index(cs_file)
                    measuresLength=len(cs.getElementsByClass(stream.Part)[0].getElementsByClass(stream.Measure))
                    partsLength=len(cs.getElementsByClass(stream.Part))
                    print idCompleteScore,measuresLength,partsLength
        
                    if(partsLength==partsNumber):
                        isEqualParts=True
                    if(measuresLength<measuresLengthBetter):
                        isLessMeasures=True
        
                    if isLessMeasures and isEqualParts:
                        isBetterOMR=True
                    if isBetterOMR:
                        idCompleteScoreBetter=idCompleteScore
                        measuresLengthBetter=measuresLength
                        partsLengthBetter=partsLength
                except:
                    print "error OMR"
        print idCompleteScoreBetter,measuresLengthBetter,partsLengthBetter
        return idCompleteScoreBetter
    

                 
                  
                