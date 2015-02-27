

'''
Created on 13/06/2014

@author: victor
'''

from Process import PipelineAlignment
from Process import SymbolConversion
from Functions import MeasureFunctions

class ProcessGroundS2:
            
    def getSimilarity(self,omrs,part):
        '''
        main function to get the similarity vs the ground
        
        return:
            result=percentage of similarity
            errors= array with errors to write in xml
            scoreWithErrors= score to write with colors
        '''
        pa=PipelineAlignment()
        mf=MeasureFunctions()
        for omr in omrs:
            try:
                omr=mf.convertVoicesToChord(omr)
            except:
                pass
            
        omr_symbolsAlign=pa.alignGround(omrs,part)
        
        omr_ground=omr_symbolsAlign[0]
        omr_part=omr_symbolsAlign[1] 
        
        count=0
        symbolsLength=0
        Errors=[]
        arrErrors=[]
        for i in range(len(omr_ground)):
            
            sGround=omr_ground[i]
            sOMR=omr_part[i]
            if isinstance(sGround,list):
                sGroundSimple=sGround[0]
            else:
                sGroundSimple=sGround
            if isinstance(sOMR,list):
                sOMRSimple=sOMR[0]
            else:
                sOMRSimple=sOMR
            
            #Removing grace notes
            if(self.isGraceNote(sGround) or self.isGraceNote(sOMR)):
                continue 
            
            if(self.isBarline(sGroundSimple) or self.isBarline(sOMRSimple)):
                continue 
            #Removing Time Signatures. PS introduce a lot extra time signatures   
#             if(self.isKeySignature(sGroundSimple) or self.isKeySignature(sOMRSimple)):
#                 continue  
            #Removing clef errors
            if(self.isClef(sGroundSimple) or self.isClef(sOMRSimple)):
                continue  
            if(self.isRest(sGroundSimple) or self.isRest(sOMRSimple)):
                continue  
            #Removing extra rest due to voices
#             if self.isRest(sOMRSimple):
#                 if sGroundSimple=="*":
#                     continue  
              
            if (sGroundSimple==sOMRSimple):
                if sGround[0]==sOMR[0] and sGround[1]==sOMR[1]:#not counting ties
                #if sGround[0]==sOMR[0]:
                    count+=1
                else:
                    Errors.append([sGround,sOMR,i])
                    arrErrors.append(i)
                               
            else:
                Errors.append([sGround,sOMR,i])
                arrErrors.append(i)
                if sOMRSimple=="*":
                    try:
                        omr_part[i]=omr_ground[i]
                        omr_part[i][5]="#00ff00" #note missing
                    except:
                        print "error",omr_part[i]
                elif sGroundSimple=="*":
                    try:
                        omr_part[i][5]="#0000ff" #extra note
                    except:
                        print "error",omr_part[i]
                else:
                    try:
                        omr_part[i]=omr_ground[i]
                        omr_part[i][5]="#ff0000" #mistake in note
                    except:
                        print "error",omr_part[i]

                
            symbolsLength+=1
            
        result=(float(count)/symbolsLength)*100    
        sc=SymbolConversion()   
        omr_part=sc.setVoices(omr_part)
        scoreWithErrors=sc.convertM21(omr_part)
        return result,Errors,scoreWithErrors
    
    def isGraceNote(self,s):
        '''
        Returns true if the symbol is a grace note
        '''
        if isinstance(s,list):
            if s[0].find('N:')!=-1: 
                duration=s[1]
                if float(duration)==0:
                    return True
           
        return False
    
    def isKeySignature(self,s):
        '''
        Returns true if the symbol is a key signature
        '''
        if s.find('KS:')!=-1: 
                return True
        return False
    
    def isRest(self,s):
        '''
        Returns true if the symbol is a rest
        '''
        if s.find('R:')!=-1: 
                return True
        return False
    
    def isBarline(self,s):
        '''
        Returns true if the symbol is a barline
        '''
        if s.find('!')!=-1: 
                return True
        return False
    
    def isClef(self,s):
        '''
        Returns true if the symbol is a clef
        '''
        if s.find('CL:')!=-1: 
                return True
        return False
               

