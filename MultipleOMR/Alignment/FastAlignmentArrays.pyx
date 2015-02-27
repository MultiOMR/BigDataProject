'''
@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

Contains an implementation of the Needleman Wunsch algorithm.
for two dimension arrays. It is a Cython file and should be 
compiled using the file setupCython.py

python setupCython.py build

The output will be in the build folder
MultipleOMR\\build\\lib.win32-2.7\\MultipleOMR

# if isFast==False, calculate the difference between the strings using the Needlemann Wunsch in C. 
#           The score value will be between +1 to -1
# if isFast==True, just compare the strings if they are equals (score=1) or different (score=-1)

# 'isFast=true' means that the differences between foo00 and foo000 is -1
# alignment are the sequences aligned
# finalValue is the last value of the matrix
# finalScore is the similarity of both sequences

usage:

seq1=["foo00","abc","123"]
seq2=["foo000","abc","1234"]

faa=FastAlignmentArray()
alignment,finalValue,finalScore=faa.needleman_wunsch(seq1, seq2,isFast=True)
# finalScore=-0.333333343267
alignment,finalValue,finalScore=faa.needleman_wunsch(seq1, seq2,isFast=False)
# finalScore=0.722222208977

'''

import numpy as np
cimport numpy as np

import NWunsch

# -*- coding: utf-8 -*-

from cpython cimport bool
 
# the three directions you can go in the traceback:
cdef int DIAG = 0 
cdef int UP = 1 
cdef int LEFT = 2
cdef float score=0

class FastAlignmentArrays:  
    
    def __needleman_wunsch_matrix(self,seq1,seq2,isFast):
        """
        fill in the DP matrix according to the Needleman-Wunsch algorithm.
        Returns the matrix of scores and the matrix of pointers
        
        if isFast==False, calculate the difference between the strings using the Needlemann Wunsch in C. 
                The score value will be between +1 to -1
        if isFast==True, just compare the strings if they are equals (score=1) or different (score=-1)
        """
     
        indel = -1 # indel penalty
     
        cdef int n = len(seq1)
        cdef int m = len(seq2)
    
        cdef np.ndarray s = np.zeros( (n+1, m+1) ) # DP matrix
        cdef np.ndarray ptr = np.zeros( (n+1, m+1), dtype=int  ) # matrix of pointers
     
        ##### INITIALIZE SCORING MATRIX (base case) #####
     
        cdef int i
        cdef int j
        for i in range(1, n+1) :
            s[i,0] = indel * i
        for j in range(1, m+1):
            s[0,j] = indel * j
     
        ########## INITIALIZE TRACEBACK MATRIX ##########
     
        # Tag first row by LEFT, indicating initial "-"s
        ptr[0,1:] = LEFT
     
        # Tag first column by UP, indicating initial "-"s
        ptr[1:,0] = UP
     
        #####################################################
     
    
        cdef int p
        cdef int q
        diagonalRange=350
        for i in range(1,n+1):
            p=i-diagonalRange
            q=i+diagonalRange
            if(p<1):
                p=1
            if(q>m+1):
                q=m+1
            for j in range(p,q): 
                # match
                myseq1=seq1[i-1]
                myseq2=seq2[j-1]
                if isinstance(myseq1,list):
                    myseq1=myseq1[0]
                if isinstance(myseq2,list):
                    myseq2=myseq2[0]
                
                    
                if(myseq1== myseq2):
                    score=1
                else:
                    score=-1
                
                if len(myseq1)==0 or len(myseq2)==0:
                    score=0
                
                #####For double alignment###
                if isFast==False:
                    if len(myseq1)==0 or len(myseq2)==0:
                        score=0
                    else:
                        score=NWunsch.NWunsch_getSimilarity(myseq1,myseq2)
                ############################
    
                s[i,j] = s[i-1,j-1]+ score
                
    
                # indel penalty
                if s[i-1,j] + indel > s[i,j] :
                    s[i,j] = s[i-1,j] + indel
                    ptr[i,j] = UP
                # indel penalty
                if s[i, j-1] + indel > s[i,j]:
                    s[i,j] = s[i, j-1] + indel
                    ptr[i,j] = LEFT
    
        return s, ptr
     
    def __needleman_wunsch_trace(self,seq1, seq2,np.ndarray s, np.ndarray ptr) :
        """
        Function that traces back the best path to get alignment 
        
        """
        #### TRACE BEST PATH TO GET ALIGNMENT ####
        align1 = []
        align2 = []
        align1_gap = []
        align2_gap = []
        gap1=[]
        gap2=[]
        
        cdef int n,m
        n, m = (len(seq1), len(seq2))
        cdef int i,j,curr
        i = n
        j = m
        curr = ptr[i, j]
        while (i > 0 or j > 0):        
            ptr[i,j] += 3
            if curr == DIAG :            
                align1.append(seq1[i-1]) 
                align2.append(seq2[j-1]) 
                align1_gap.append(seq1[i-1]) 
                align2_gap.append(seq2[j-1]) 
                i -= 1
                j -= 1            
            elif curr == LEFT:
                align1.append("*") 
                align2.append(seq2[j-1]) 
                align1_gap.append("[GAP]") 
                align2_gap.append(seq2[j-1]) 
                j -= 1            
            elif curr == UP:
                align1.append(seq1[i-1]) 
                align2.append("*") 
                align1_gap.append(seq1[i-1]) 
                align2_gap.append("[GAP]") 
                i -= 1
     
            curr = ptr[i,j]
            
        align1.reverse()
        align2.reverse() 
        align1_gap.reverse()
        align2_gap.reverse() 
        #gaps
        for index in range(len(align1_gap)):
            if(align1_gap[index])=="[GAP]":
                gap1.append(index)
        
        for index in range(len(align2_gap)):
            if(align2_gap[index])=="[GAP]":
                gap2.append(index)
    
          
        return align1, align2,gap1,gap2
    
        
    def needleman_wunsch(self,seq1, seq2,isFast=True) :
        """
        Computes an optimal global alignment of two sequences using the Needleman-Wunsch
        algorithm
        returns the alignment and its score
        
        # if isFast==False, calculate the difference between the strings using the Needlemann Wunsch in C. 
        #           The score value will be between +1 to -1
        # if isFast==True, just compare the strings if they are equals (score=1) or different (score=-1)
        
        # 'isFast=true' means that the differences between foo00 and foo000 is -1
        # alignment are the sequences aligned
        # finalValue is the last value of the matrix
        # finalScore is the similarity of both sequences
        
        usage:
        
        seq1=["foo00","abc","123"]
        seq2=["foo000","abc","1234"]
        
        faa=FastAlignmentArray()
        alignment,finalValue,finalScore=faa.needleman_wunsch(seq1, seq2,isFast=True)
        # finalScore=-0.333333343267
        alignment,finalValue,finalScore=faa.needleman_wunsch(seq1, seq2,isFast=False)
        # finalScore=0.722222208977

        """
        s,ptr = self.__needleman_wunsch_matrix(seq1, seq2,isFast)
        alignment = self.__needleman_wunsch_trace(seq1, seq2, s, ptr)
        cdef int maxlen=len(seq1)
        if len(seq2)>len(seq1):
            maxlen=len(seq2)
        cdef float finalscore=s[len(seq1), len(seq2)]/maxlen
        return alignment, s[len(seq1), len(seq2)],finalscore
    
    
