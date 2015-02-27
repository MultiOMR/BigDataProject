'''
@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

Functions to manipulate measures


'''

from music21 import stream
from music21 import note
from music21 import meter
from music21 import omr
from music21 import spanner
from music21 import chord
import copy


class MeasureFunctions:
    
    def getDuration(self,bar):
        '''
        Returns the duration of a single measure
        '''
        duration=0
        try:
            for event in bar:
                try:
                    if(event.isNote):
                        duration+=event.duration.quarterLength
                    if(event.isRest):
                        duration+=event.duration.quarterLength
                except:
                    pass
        except:
            pass
        return str(duration)
    
    def correctIncorrectMeasuresArray(self,omr,incorrectMeasures):
        '''
        Iteractive method that detects if some measures have been wrong flagged as an error.
        It is under development
        '''
        measures=omr.parts[0].getElementsByClass(stream.Measure)
        if 0 in incorrectMeasures:
            incorrectMeasures.remove(0)#Anacrusis
            
        for barNumber in incorrectMeasures:
            if barNumber<len(measures)-1:
                measure=measures[barNumber]
                measureNext=measures[barNumber+1]
                duration=self.getDuration(measure)
                
                if(float(duration)<=0):
                    incorrectMeasures.remove(barNumber)
                    self.correctIncorrectMeasuresArray(omr,incorrectMeasures)
                    
                if(measureNext!=None):
                    durationNext=self.getDuration(measureNext)
                    if(float(duration)+float(durationNext)==4):
                        try:
                            incorrectMeasures.remove(barNumber)
                            incorrectMeasures.remove(barNumber+1)
                        except:
                            pass
                        self.correctIncorrectMeasuresArray(omr,incorrectMeasures)
        return incorrectMeasures
    
    
    def filterExtraMeasures(self,omr):
        '''
        Function that removes empty measures
        '''
        sco=stream.Score()
        s=stream.Part()
        for measure in omr.parts[0].getElementsByClass(stream.Measure):
            if measure.flat.duration.quarterLength>0:
                s.append(measure)
        sco.append(s)
        return sco
    
    
    def getIncorrectMeasureIndices(self,omr):
        '''
        Method that detect wrong measures using transitions
        '''
        arrChunks= self.getTransitions(omr)
        measures=omr.parts[0].getElementsByClass(stream.Measure)
        indexBar=0
        FlagErrors=[]
        barFrom=0
        barTo=0
        for chunk in arrChunks:
            indexC=arrChunks.index(chunk)
            chunkBefore=arrChunks[indexC-1]
            if(indexC==0):
                barFrom=0
            else:
                barFrom+=chunkBefore[1]  
            barTo=chunk[1]+barFrom       
            chunkMeasures=measures[barFrom:barTo]
            quarterChunk=round(chunk[0]/2)
            for measure in chunkMeasures:              
                if measure.duration.quarterLength!=quarterChunk:
                    FlagErrors.append(indexBar)
                indexBar+=1
        return FlagErrors
    
    def _filterTransitions(self,arrMeasureIndex):
        '''
        Inner method that removes false transitions in measures for detecting missing time signatures
        '''
        arrMeasureIndex2=[]
        arrMeasureIndex.insert(0,0)
        arrMeasureIndex.append(-1) 
        for mes in arrMeasureIndex:
            indexM=arrMeasureIndex.index(mes)
            if indexM>0:
                bars=arrMeasureIndex[indexM]-arrMeasureIndex[indexM-1]
                if (bars>9):
                    arrMeasureIndex2.append(mes)
        arrMeasureIndex2.insert(0,0)
        arrMeasureIndex2.append(-1) 
        return arrMeasureIndex2
   
    def getTransitions(self,omr):
        '''
        Returns transitions in a omr
        '''
        MeasuresLength=[]
        arrMeasureIndex_before=self._getTransitionBar(omr)
        
        arrMeasureIndex=self._filterTransitions(arrMeasureIndex_before)
        for i in range(len(arrMeasureIndex)-1):
            arrMeasureslength= self._getAverageQuavers(omr,arrMeasureIndex[i],arrMeasureIndex[i+1],False)
            MeasuresLength.append(arrMeasureslength)

        return MeasuresLength
        
    def _getTransitionBar(self,omr):
        '''
        Inner function for getting transitions
        '''
        arrOut=[]
        measures=omr.parts[0].getElementsByClass(stream.Measure)
        barsNumber=len(measures)
        for barIndex in range(5,barsNumber):
            averageBefore=self._getAverageQuavers(omr,barIndex-4,barIndex,isUntilTS=False)
            averageAfter=self._getAverageQuavers(omr,barIndex,barIndex+2,isUntilTS=False)
            if(abs(averageBefore[0]-averageAfter[0])>1.5):
                if(measures[barIndex].duration.quarterLength<averageBefore[0]*2):#rest bars or missing bars
                    arrOut.append(barIndex)
        return arrOut
        
    def _getAverageQuavers(self,myStream,measureIndex,measureIndexEnd,isUntilTS):
        '''
        Inner function for getting the average quavers per measure in a group of measures
        '''
        quavers=0
        barNumbers=0
        averageQuavers=0
        measures=myStream.parts[0].getElementsByClass(stream.Measure)
        for bar in measures[measureIndex:measureIndexEnd]:
            duration=bar.duration.quarterLength*2
            barNumbers+=1
            if(duration>0 and duration<10):
                quavers+=duration
                if isUntilTS:
                    if (len(bar.getElementsByClass(meter.TimeSignature))>0):
                        break
        if barNumbers>0:   
            averageQuavers=quavers/barNumbers
        return averageQuavers,barNumbers
    
#**************************************************
    def getPossibleBeamsErrors(self,omr):   
        '''
        Function that returns measure errors based on non conventional beaming
        '''
        arrErrors=[] 
        measures=omr.parts[0].getElementsByClass(stream.Measure)
        barsNumber=len(measures)
        for i in range(barsNumber):
            notes=measures[i].getElementsByClass(note.Note)
            count=0
            state=0
            for n in notes:
                if n.duration.quarterLength==0.25:
                    bs=n.beams.getNumbers() 
                    if(len(bs)>0):
                        b=n.beams.getByNumber(bs[0])          
                        if b.type=='start':
                            count=1
                            state=1
                        if b.type=='continue':
                            if(state==1 or state==2):
                                count+=1
                                state=2
                        if b.type=='stop':
                            if(state==1 or state==2):
                                count+=1
                                if count==3:
                                    arrErrors.append(i)
        arrErrors=list(set(arrErrors))
        return arrErrors

    def getPossibleLastNoteErrors(self,omr):   
        '''
        Function that returns measure errors based on the last notes rhythm
        '''
        arrErrors=[] 
        measures=omr.parts[0].getElementsByClass(stream.Measure)
        barsNumber=len(measures)
        for i in range(barsNumber):
            notes=measures[i].getElementsByClass(note.GeneralNote)
            if(len(notes)>0):
                lastNote=notes[len(notes)-1]
                if lastNote.duration.quarterLength<=0.25:
                    if(lastNote.isRest):
                        arrErrors.append(i)
                    else:
                        bs=lastNote.beams.getNumbers() 
                        
                        if(len(bs)==0):
                            if(len(notes)>2):
                                noteBefore=notes[len(notes)-2]
                                if noteBefore.duration.quarterLength+lastNote.duration.quarterLength!=1:
                                    arrErrors.append(i)
               
            
        return arrErrors
    
    def flagIncorrectMeasures(self,omr2):
        '''
        flag the incorrect measures from a omr using different methods
        '''
        mf=MeasureFunctions()
        sc=omr.correctors.ScoreCorrector(omr2)
        part=sc.getSinglePart(0)
         
        arrErrors=[]
        im=part.getIncorrectMeasureIndices(runFast=False)
        
        im1= mf.getIncorrectMeasureIndices(omr2)
        
        im2= mf.getPossibleBeamsErrors(omr2)
        im3= mf.getPossibleLastNoteErrors(omr2)
       
         
        arrErrors.append(im)
        arrErrors.append(im1)
        arrErrors.append(im2)
        arrErrors.append(im3)
         
        if(len(im)>15):
            if(len(im1)<len(im)):
                im=im1
        imSum=list(set(im)|set(im2)|set(im3))
        imSum=sorted(imSum)
        imOK=mf.correctIncorrectMeasuresArray(omr2,imSum)  
        print im
        return imOK,arrErrors
    
    def getSlurs(self,part):
        '''
        Returns the slurs from one part
        '''
        slurs=part.flat.getElementsByClass(spanner.Spanner)
        return slurs
        
    def reconstructScore(self,part,hashPart): 
        '''
        This function include rest measures in one part based on the hash part aligned
        '''
        partReconstructed=stream.Part()
        barNumber=1
        gaps=[]
        for i in range(len(hashPart)): 
            if hashPart[i]!="*":
                m=part.getElementsByClass(stream.Measure)[barNumber-1]
                partReconstructed.append(m)
                barNumber+=1
            else:
                m=stream.Measure()
                partReconstructed.append(m)
                gaps.append(i)
        slurs=self.getSlurs(part)   
        partReconstructed.append(slurs)  
        myStream=self.reorderMeasures(partReconstructed)  
        return myStream,gaps
    
    def reorderMeasures(self,omr):
        '''
        Returns the correct measures number
        '''
        slurs=self.getSlurs(omr) 
        s=stream.Part()
        barNumber=1
        for measure in omr.getElementsByClass(stream.Measure):
            measure.number=barNumber
            s.append(measure)
            barNumber+=1
        s.append(slurs)
        return s      
    
    def getNoteByOffset(self,voice,offset):
        '''
        Returns one note in one voice according to the offset
        '''
        for n in voice.getElementsByClass(note.Note):
            if n.offset==offset:
                return n
        for n in voice.getElementsByClass(chord.Chord):
            if n.offset==offset:
                return n
    
    def convertVoicesToChord(self,omr):
        '''
        Function that converts voices with the same rhythm to chords
        '''
        for part in omr.getElementsByClass(stream.Part):
            for measure in part.getElementsByClass(stream.Measure):
                measure.show('text')
                voices=measure.getElementsByClass(stream.Voice)
                if len(voices)>=2:
                    for element1 in voices[0].getElementsByClass(note.GeneralNote):
                        offset1= element1.offset
                        for voice in voices:
                            if voice!=voices[0]:
                                element2=self.getNoteByOffset( voice, offset1)
                                if element2 is not None and element1.duration.quarterLength==element2.duration.quarterLength and not isinstance(element1,note.Rest):
                                    mychord=self.mergeChords(element1,element2)  
                                    mychord.duration.quarterLength=element1.quarterLength
                                    voices[0].replace(element1,mychord)
                                    myrest=note.Rest()
                                    myrest.duration.quarterLength=element1.quarterLength
                                    voice.replace(element2,myrest)

        omr=self.removeRestVoice(omr)
        return omr
    def removeRestVoice(self,omr):
        '''
        This option removes the rest voices (without notes) 
        '''
        for part in omr.getElementsByClass(stream.Part):
            for measure in part.getElementsByClass(stream.Measure):
                voices=measure.getElementsByClass(stream.Voice)
                for voice in voices:
                    myvoice = copy.deepcopy(voice)
                    myvoice.removeByClass('Rest')
                    if len(myvoice)==0:
                        measure.remove(voice)
        
        return omr
     
    def mergeChords(self,element1,element2): 
        '''
        Returns one chord made by two elements, notes or chords
        '''
        notes1=[]
        notes2=[]
        notes=[]
        if isinstance(element1,chord.Chord):
            notes1=element1.pitches
        else:
            notes1.append(element1.pitch)
        
        if isinstance(element2,chord.Chord):
            notes2=element2.pitches
        else:
            notes2.append(element2.pitch)
        
        for n in notes1:
            notes.append(n)
        for n in notes2:
            notes.append(n)

        mychord = chord.Chord(notes)
        return mychord
        
    
    def convertBeamsToTriplets(self,omr):  
        '''
        This option search for measures where the rhythm is bigger than the time signature
        and tries to convert 3 note beams in triplets
        '''
        tsDefault=omr.flat.getElementsByClass('TimeSignature')[0]
        idPart=0
        for part in omr.getElementsByClass(stream.Part):
            idPart+=1
            idMeasure=0
            for measure in part.getElementsByClass(stream.Measure):
                idMeasure+=1
                if self._IsMeasureHigherTS(idMeasure, part,tsDefault):
                    print idMeasure
                    measure=self.beamsToTriplets(measure)
        return omr
               
                    
    def _IsMeasureHigherTS(self,idMeasure,part,ts):
        '''
        Inner function that detects if one measure is bigger than the time signature
        '''
        idCountMeasure=0
        for measure in part.getElementsByClass(stream.Measure):
            idCountMeasure+=1
            newts=measure.flat.getElementsByClass('TimeSignature')
            if len(newts)>0:
                ts=newts[0]
            if idMeasure==idCountMeasure:
                voices=measure.getElementsByClass(stream.Voice)
                totalDuration=0
                if len(voices)>=1:
                    for voice in voices:
                        totalDuration=0
                        for element in voice.getElementsByClass(note.GeneralNote):
                            totalDuration+=element.duration.quarterLength;
                else:
                    for element in measure.getElementsByClass(note.GeneralNote):
                        totalDuration+=element.duration.quarterLength;
                quartersBymeasure=ts.numerator*(4.0/ts.denominator)
                if totalDuration>quartersBymeasure:
                    return True
                else:
                    return False
    def beamsToTriplets(self,measure):
        '''
        This function returns one measure changing 3 notes beamed by triplets
        '''
        voices=measure.getElementsByClass(stream.Voice)
        if len(voices)>=1:
            for voice in voices:
                notes=voice.getElementsByClass(note.NotRest)
                notes=self._notesToTriplets(notes)
               
        else:
            notes=measure.getElementsByClass(note.NotRest)
            notes=self._notesToTriplets(notes)
                
        return measure
    
    
    def _notesToTriplets(self,notes):
        '''
        Gets one note arrays and tries to convert to triplets
        '''

        for i in range(len(notes)):
            self._removeSlurs(notes[i])
            beams1=notes[i].beams.beamsList
            
            try:
                beams2=notes[i+1].beams.beamsList
                beams3=notes[i+2].beams.beamsList
                if len(beams1)>0 and len(beams2)>0 and len(beams3)>0:
                    if beams1[0].type=='start' and beams2[0].type=='continue' and beams3[0].type=='stop':
                        if notes[i].duration.quarterLength==notes[i+1].duration.quarterLength==notes[i+2].duration.quarterLength:
                            mytype=notes[i].duration.type
                            duration=note.duration.convertTypeToQuarterLength(mytype)
                            realDuration=duration*2.0/3.0
                            notes[i].duration.quarterLength=realDuration
                            notes[i+1].duration.quarterLength=realDuration
                            notes[i+2].duration.quarterLength=realDuration
            
            except:
                pass
        
        return notes
                            
    def _removeSlurs(self,n): 
        '''
        Removes the slur in one note
        '''
        for element in n.getSites():
            if isinstance(element,stream.SpannerStorage):
                for e in element.elements:
                    element.pop(0)   
    
    def removesEmptyVoices(self,omr):
        '''
        Removes empty voices (just rests)
        '''
        for part in omr.getElementsByClass(stream.Part):
            for measure in part.getElementsByClass(stream.Measure):
                print measure
                voices=measure.getElementsByClass(stream.Voice)
                if len(voices)>=1:
                    print len(voices)
                    for voice in voices:
                        notes=voice.getElementsByClass(note.NotRest)
                        if len(notes)==0:
                            index=measure.index(voice)
                            measure.pop(index)
                voices=measure.getElementsByClass(stream.Voice)
                if len(voices)==1:
                    measure.flattenUnnecessaryVoices()
        return omr
    
    def removesGaps(self,omr):
        '''
        This option changes gaps by rests in voices
        '''
        for part in omr.getElementsByClass(stream.Part):
            for measure in part.getElementsByClass(stream.Measure):
                voices=measure.getElementsByClass(stream.Voice)
                if len(voices)>=1:
                    for voice in voices:
                        v=voice.findGaps()
                        if v!=None:
                            nextOffset=1000
                            for element in voice.getElementsByClass(note.GeneralNote):
                                offset= element.offset
                                if offset>nextOffset:
                                    rest=note.Rest()
                                    rest.duration.quarterLength=offset-nextOffset
                                    voice.insert(nextOffset,rest)
                                    nextOffset=1000
                                else:
                                    duration=element.duration.quarterLength
                                    nextOffset=offset+duration
        return omr                    
                        

