'''
Created on 10/11/2014

@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

Functions related to the alignment
and voting process
'''
from Alignment import FastAlignmentArrays
from SymbolConversion import SymbolConversion
from Functions import FilesFunctions
import numpy as np
from Clustering import Clustering
import math
from Alignment import NWunsch


class PipelineAlignment:
    def alignGround(self,OMRs,part):
        '''
        Returns one part and the ground aligned. The first array value of OMRs 
        should be the ground and the second the omr to align
        '''
        sc=SymbolConversion()
        OMRs_symbols=[]
        omr_symbolsAlign=[]
        for omr in OMRs:
            omr_symbols=sc.filterOMR(omr,part)[1]
            OMRs_symbols.append(omr_symbols)
            omr_symbolsAlign.append([])
        
        faa=FastAlignmentArrays()
        out=faa.needleman_wunsch(OMRs_symbols[0], OMRs_symbols[1])[0]

             
        return out
    
    def getDistances(self,OMRs_symbols):
        '''
        Returns the distance matrix from several omr
        in symbols, using the first symbol only
        [u'N:E-4_0.25', 0.25, '', 2.75, 3.0, None] y
        [u'N:E-4_0.25', 0.33, '', 2.50, 2.75, None]
        
        are equals
        
        Returns a triangular matrix
        [[ 0.          0.17647058  0.19141912]
         [ 0.          0.          0.17647058]
         [ 0.          0.          0.        ]]
        
        Uses the algorithm implemented in C for increasing the speed 
        Alignment/C_Libraries/NWunsch
        '''
        ls=len(OMRs_symbols)
        dimension= (ls,ls)
        distances=np.zeros(dimension)   
        for i in range(len(OMRs_symbols)):  
            for j in range(i+1,len(OMRs_symbols)):
                print i,j
                align1=[]
                align2=[]
                for s in OMRs_symbols[i]:
                    align1.append(s[0])
                for s in OMRs_symbols[j]:
                    align2.append(s[0])
                #Algorithm implemented in C
                if len(align1)==0 or len(align2)==0:
                    score=0
                else:
                    print"-------------------------"  
                    
                    score=NWunsch.NWunsch_getSimilarity(align1,align2)
                    print"-------------------------"  
                if math.isnan(score):
                    score=0
                distances[i][j]=1-score      
        return distances
    
    def getDistanceLength(self,OMRs_symbols):
        '''
        Similar to getDistance, but based on the length
        of the omrs. Testing purposes
        '''
        ls=len(OMRs_symbols)
        dimension= (ls,ls)
        distances=np.zeros(dimension)       
        for i in range(len(OMRs_symbols)):       
            for j in range(i+1,len(OMRs_symbols)):
                print i,j
                len_i=len(OMRs_symbols[i])
                len_j=len(OMRs_symbols[j])
                maxLen=len_j
                if len_i>=len_j:
                    maxLen=len_i
                
                score=(len_i-len_j)*1.0/maxLen
                if score<0:
                    score=score*-1
                distances[i][j]=score        
        return distances
    
    def __getMinimum(self,distance):
        '''
        Returns the minimum value and the x,y position
        in the distance matrix
        '''
        minim=1000
        iMin=0
        jMin=0
        for i in range(len(distance[0])):         
            for j in range(i+1,len(distance[0])):
                dist=distance[i][j]
                if isinstance(dist,list):
                    dist=dist[0]
                if dist<minim:
                    minim=dist
                    iMin=i
                    jMin=j
                    
        return minim,iMin,jMin
    
    
    def __recalculeDistances(self,distance,iMin,jMin):
        '''
        Removes the rows and the column in the distance matrix
        and calculates the new matrix 
        '''
        for i in range(len(distance[0])):         
            for j in range(i+1,len(distance[0])):       
                if j==iMin:
                    dist=distance[i][j]
                    dist2=distance[i][jMin]
                    distance[i][j]=(dist+dist2)/2
        distance=np.delete(distance, jMin, 0)
        distance=np.delete(distance, jMin, 1)     
        return distance
    
    
    def __getPairingReal(self,iMin,jMin,removedArray):
        '''
        Returns the real omr position in the original matrix 
        based on the actual position and the elements removed
        
        usage:
        self._getPairingReal(0,1,[1])
        returns
        0,2
        '''
        iMinReal=iMin
        jMinReal=jMin
        removedArray.sort()
        for removedItem in removedArray:
            if iMinReal>=removedItem:
                iMinReal+=1
            if jMinReal>=removedItem:
                jMinReal+=1
        return iMinReal,jMinReal
    
    def selectBetterOMRs(self,OMRs_symbols):
        '''
        Based on Philogenetic trees, this function
        takes the best omrs based on the distances between them
        '''
        distanceSimple=self.getDistances(OMRs_symbols)  
        clustering=Clustering()
        distances=clustering.getCompleteMatrix(distanceSimple)  
        species = []
        for i in range(len(OMRs_symbols)):
            species.append(i)
        clu = clustering.make_clusters(species)    
        tree = clustering.regroup(clu, distances)

        #at least 3 leafs in the tree
        maintree=tree
        for i in range(3,len(OMRs_symbols)):
            maintree=clustering.getBetterTree(tree,i)
            if len(clustering.getLeafs(maintree))>=3:
                break
           
            
        betterOmrIds= clustering.getLeafs(maintree) 
        
        #Graphic representation
        strTree=clustering.getStringTree(tree,tree.height,"")
        print strTree
        clustering.showTree(strTree)
        strMainTree=clustering.getStringTree(maintree,maintree.height,"")
        print strMainTree
        clustering.showTree(strMainTree)

        newOMRs=[]
        for i in betterOmrIds:
            newOMRs.append(OMRs_symbols[i])

        return newOMRs,betterOmrIds
    
#     def alignNJ(self,idPart,fsOMRs,partOMRs):
#         '''
#         Main function for aligning the different OMRs
#         
#         Returns:
#             omr_symbolsAligned. OMR array of symbols aligned (only the best)
#             betterOmrIds. Id array of better OMRs (for writing the log file)
#         
#         usage:
#             pa=PipelineAlignment()
#             omr_symbolsAligned,betterOmrIds=pa.alignNJ(idPart,fsOMRs,partOMRs)
#         '''
#         
# 
#         OMRs_symbols=[]
#         sc=SymbolConversion()
#         print "2---converting to symbols---"
#         for omr in OMRs:
#             if omr!=[]:
#                 omr_symbols=sc.filterOMR(omr,idPart)[1]
#                 OMRs_symbols.append(omr_symbols)
#             else:
#                 OMRs_symbols.append([])
#             
#         print "3---removing worst OMR---"  
# #         betterOmrIds=[]
#         OMRs_symbols,betterOmrIds=self.selectBetterOMRs(OMRs_symbols)
# 
#         print "4---calculating distances---"
#         distances=self.getDistances(OMRs_symbols)
#         
#         print "5---aligning symbols---"
#                
#         omr_symbolsAligned=self.setOMRSymbolsAligned(OMRs_symbols,distances)
#         
#         return omr_symbolsAligned,betterOmrIds
    
    def alignNJ_files(self,idPart,fsOMRs_files,partOMRs_files):
        '''
        Main function for aligning the different OMRs
        
        Returns:
            omr_symbolsAligned. OMR array of symbols aligned (only the best)
            betterOmrIds. Id array of better OMRs (for writing the log file)
        
        usage:
            pa=PipelineAlignment()
            omr_symbolsAligned,betterOmrIds=pa.alignNJ(idPart,fsOMRs,partOMRs)
        '''
        
               
        ff=FilesFunctions()
        OMRs_files=partOMRs_files+fsOMRs_files
        OMRs_symbols=[]
        sc=SymbolConversion()
        print "2---converting to symbols---"
        for omr_file in OMRs_files:
            omr=ff.getOMR(omr_file)
            if omr!=[]:
                omr_symbols=sc.filterOMR(omr,idPart)[1]
                OMRs_symbols.append(omr_symbols)
            else:
                OMRs_symbols.append([])
            
        print "3---removing worst OMR---"  
#         betterOmrIds=[]

        
        OMRs_symbols,betterOmrIds=self.selectBetterOMRs(OMRs_symbols)

        print "4---calculating distances---"
        distances=self.getDistances(OMRs_symbols)
        
        print "5---aligning symbols---"
               
        omr_symbolsAligned=self.setOMRSymbolsAligned(OMRs_symbols,distances)
        
        return omr_symbolsAligned,betterOmrIds
    def __setVoidArray(self,length):
        '''
        private function to create a void array
        '''
        arrayOut=[]
        for _ in range(length):
            arrayOut.append([])

        return arrayOut
            
    def setOMRSymbolsAligned(self,OMRs_symbols,distances):   
        '''
        returns the OMRs symbols aligned from OMR symbols and 
        the distances matrix
        ''' 
        pairings=[]
        pairingsReal=[]
        gapArray=[]
        removedArray=[]
        omr_symbolsAlign=self.__setVoidArray(len(OMRs_symbols))
        faa=FastAlignmentArrays()
        while len(distances[0])>1:
            minim,iMin,jMin=self.__getMinimum(distances)
            print distances,minim,iMin,jMin
            pairings.append([iMin,jMin])
            iMinReal,jMinReal=self.__getPairingReal(iMin,jMin,removedArray)
            
            pairingsReal.append([iMinReal,jMinReal])
            if len(omr_symbolsAlign[iMinReal])==0:
                omr_symbolsAlign[iMinReal]=OMRs_symbols[iMin]
            if len(omr_symbolsAlign[jMinReal])==0:
                omr_symbolsAlign[jMinReal]=OMRs_symbols[jMin]
                
            out=faa.needleman_wunsch(omr_symbolsAlign[iMinReal], omr_symbolsAlign[jMinReal])[0]
            omr_symbolsAlign[iMinReal]=out[0]
            omr_symbolsAlign[jMinReal]=out[1]
            gap1=out[2]
            gap2=out[3]
            gapArray.append([gap1,gap2])
            

            OMRs_symbols.pop(jMin)
            removedArray.append(jMinReal)
            
            distances=self.__recalculeDistances(distances,iMin,jMin)
            
                
        omr_symbolsAlign=self.__fillingGaps(omr_symbolsAlign,gapArray,pairingsReal)


        return omr_symbolsAlign
    
    def __fillingGaps(self,omr_symbolsAlign,gapArray,pairingsReal):
        '''
        private function to complete gaps based on the gap matrix 
        and the pairs stablished
        '''
        for p in range(len(pairingsReal)-1,0,-1):
            for i in range(2):
                for j in range(2):
                    for t in range(1,p+1):
                        if(pairingsReal[p][i]==pairingsReal[p-t][j]):
                            if j==0:
                                s=1
                            if j==1:
                                s=0
                            omrIndex=pairingsReal[p-t][s]
                            newGap=[]
                            for gap in gapArray[p][i]:
                                omr_symbolsAlign[omrIndex].insert(gap,"*")   
                                newGap.append(gap)
                            gapArray[p-t][s]=gapArray[p-t][s]+newGap
                                

        return omr_symbolsAlign



                    
                

    
    
    
    
                    
                
             

        
        
        