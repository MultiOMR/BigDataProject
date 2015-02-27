'''
Created on 24/09/2014

@author: victor

Class for adding and joining measures
(It is under development)
'''
import os
from music21 import stream
from music21 import converter
from music21 import meter
from music21 import key
from music21 import clef
from music21 import note
from music21 import interval

class AddingXMLSingleMeasures:
    def getAllFiles(self,path):
        omr_files=[]
        dir_content = os.listdir(path)
        dir_content.sort()
        for myfile in dir_content:
            directory = os.path.join(path,myfile)
            omr_files.append(os.path.abspath(directory))
        print omr_files
        return omr_files
    
    def runViewJoinXML(self,dirname):
        path = dirname
        files=self.getAllFiles(path)
        filesM21=self.getFilesM21(files,path)
        part=stream.Part()
        ks_array=[]
        for f in filesM21:
            measure=f.parts[0].getElementsByClass(stream.Measure)[0]
            if len(part)==0:
                ks_array=self.getKeySignatureArray(measure)
                
            if len(part)>0:
                measure=self.removeTimeSignature(measure)
                measure=self.removeKeySignature(measure)
                measure=self.removeClef(measure)
#                 measure=self.transpose(measure,-10)
            part.append(measure)
#         part=self.correctKeySignature(part,["C "])  
        # the correct key signature
        part=self.correctKeySignature(part,ks_array)       
        part.show()
    def transpose(self,measure,semitones):
        newMeasure=stream.Measure()
        for element in measure:
                if isinstance(element,note.Note):  
                    element=element.transpose(interval.Interval(semitones))
                newMeasure.append(element)
        return newMeasure
    def getKeySignatureArray(self,measure):
        ks_array=[]
        for element in measure:
            if isinstance(element,key.KeySignature):
                for p in element.alteredPitches:
                    ks_array.append(str(p))
                return ks_array                
    def correctKeySignature(self,part,altered):
        newPart=stream.Part()
        for measure in part.getElementsByClass(stream.Measure):
            newMeasure=stream.Measure()
            for element in measure:
                if isinstance(element,note.Note):
                    for alter in altered:
                        print element.pitch.name,alter
                        if element.pitch.name[0:1]==alter[0:1] and alter[1:2]=="#":
                            element.accidental=1
                        if element.pitch.name[0:1]==alter[0:1] and alter[1:2]=="-":
                            element.accidental=-1
                        if element.pitch.name[0:1]==alter[0:1] and alter[1:2]==" ":
                            element.accidental=0
                newMeasure.append(element)
            newPart.append(newMeasure)
        return newPart
        
    def removeTimeSignature(self,measure):
        newmeasure=stream.Measure()
        for element in measure:
            if not isinstance(element,meter.TimeSignature):
                newmeasure.append(element)
        return newmeasure       
    def removeKeySignature(self,measure):
        newmeasure=stream.Measure()
        for element in measure:
            if not isinstance(element,key.KeySignature):
                newmeasure.append(element)
        return newmeasure   
    def removeClef(self,measure):
        newmeasure=stream.Measure()
        for element in measure:
            if not isinstance(element,clef.GClef) and not isinstance(element,clef.NoClef) :
                newmeasure.append(element)
        return newmeasure                          
            
      
        
            
    def getFilesM21(self,files,path):
        filesM21=[]
        print "---Converting Files---"
        for i in range(len(files)):
            f=path+"\M"+str(i+1)+".xml"
            f_m21=converter.parse(f)
            filesM21.append(f_m21)
        return filesM21