'''
Created on 12/12/2014

@author: victor
'''
class Voting:
    
    def __getIndicesFromValue(self,value, qlist):
        '''
        Return the index in the matrix with that value
        '''
        indices = []
        idx = -1
        while True:
            try:
                idx = qlist.index(value, idx+1)
                indices.append(idx)
            except ValueError:
                break
        return indices
    
    def vote(self,omr_symbolsAlign):  
        '''
        main function for voting the omr symbol array
        
        '''
        voteArr=self.getArrayVotation(omr_symbolsAlign)  
        outArr=self.getVoteResult(omr_symbolsAlign,voteArr)
        return outArr
    
    def getArrayVotation(self,omr_symbolsAlign):
        '''
        Returns a matrix with the number of votes of each symbol.
        Each symbol is voted individually
        
        '''
        voteArr=[] 
        for i in range(len(omr_symbolsAlign[0])):
            voteArr.append([])
            
            for j in range(len(omr_symbolsAlign)):
                vote=[]
                for n in range(5):
                    vote.append(0)
                voteArr[i].append([])

                for k in range(len(omr_symbolsAlign)):
                    symbol1=omr_symbolsAlign[j][i] 
                    symbol2=omr_symbolsAlign[k][i]
                    for n in range(5):
                        if isinstance(symbol1,list) and isinstance(symbol2,list):
                            if(symbol1[n]==symbol2[n]):
                                vote[n]+=1.0    

                voteArr[i][j].append(vote) 
        return voteArr
#  

    
    def _getNValueArray(self,array,n):
        '''
        Takes one slide in the aligned array
        '''
        values=[]
        for o in array:
            value=o[0][n] 
            values.append(value)
        return values
    
    def __getBetterIndexSymbol(self,a0,a1,a2):
        '''
        returns the best symbol based on the first three parameters
        [[D5_0.25,0.33,'start'....]
        note,realDuration, tie
        '''
        symbol_count=[]
        for i0 in a0:
            s=0
            if i0 in a1:
                s=s+10
            if i0 in a2:
                s=s+1    
            symbol_count.append(s)
        better=symbol_count.index(max(symbol_count))
        index=a0[better]
        return index
    
    def getBetterGeneralSymbol(self,omr_symbolsAlign,indexPosition,a):
        '''
        reconstruct the symbol using the best 5 parameters 
        '''
        s=omr_symbolsAlign[a[0][0]][indexPosition]
        if isinstance(s,list):
            try:
                for n in range(5):
                    s[n]=omr_symbolsAlign[a[n][0]][indexPosition][n]
                return s
            except:
                return s 
        else:
            return s
            
    def getVoteResult(self,omr_symbolsAlign,voteArr):#voteArr[i][j].append([vote,vote_1,vote_2])  
        '''
        Using the symbols aligned and the matrix with the votes.
        
        One symbol in three omr has this structure
        [[[3.0, 2.0, 3.0, 2.0, 2.0]],
         [[3.0, 1.0, 3.0, 1.0, 1.0]], 
         [[3.0, 2.0, 3.0, 2.0, 2.0]]]
         
        returns the better output
        '''
        outArr=[]
        for i in range(len(voteArr)):
            vote=[]
            indexMax_array=[]
            for n in range(5):
                vote.append([])
                vote[n]=self._getNValueArray(voteArr[i],n)  
                indexMax_array.append([])         
                indexMax_array[n]=self.__getIndicesFromValue(max(vote[n]),vote[n])

            betterIndex=self.__getBetterIndexSymbol(indexMax_array[0],indexMax_array[1],indexMax_array[2])
            sBetterGeneral=self.getBetterGeneralSymbol(omr_symbolsAlign,i,indexMax_array)
            perc=vote[0][betterIndex]/len(vote[0])

            if perc>=0.5:
                outArr.append(sBetterGeneral)
        return outArr
    
    