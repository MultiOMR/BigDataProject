'''
Created on 10/11/2014

@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

Functions related to convert music21 output
to symbols for aligning and voting
'''
from music21 import note
from music21 import chord
from music21 import meter
from music21 import key
from music21 import stream
from music21 import tie
from music21 import bar
from music21 import harmony
from music21 import clef
class SymbolConversion:
    
    
    def __getSymbolMesure(self,symbol):
        '''
        Detects if it is a barline symbol and gets the first element
        '''
        if isinstance(symbol,list):
            if symbol[0].find('!')!=-1: 
                return symbol
                
    def convertM21(self,symbolArray):
        '''
        Converts one Array of symbols to music21
        
        usage:
        
        outVote=vote.vote(omr_symbolsAlign)
        #apply voices if it is needed
        
        outVote=sc.setVoices(outVote)
        #convert to music21
        resultS2=sc.convertM21(outVote)
        
        '''
        
        sOut=stream.Score()
        sPart=stream.Part()
        measureIndex=1
        measure=stream.Measure()
        measure.number=measureIndex
        voicesLength=8
        for v in range(voicesLength):
            voice=stream.Voice()
            voice.id=v
            measure.append(voice)
        indexS=0
       
        for symbol in symbolArray:
            mytie=""
            realDuration=None
            s=symbol
                            
            if isinstance(s,list):
                s=s[0]             
            if s.find('TS:')!=-1:
                ts=meter.TimeSignature(s[3:])
               
                measure.append(ts)
            if s.find('KS:')!=-1:
                k=key.KeySignature(int(s[3:]))
                
                measure.append(k)
            if s.find('CL:')!=-1:
                c=clef.clefFromString(str(s[3:]))
                
                measure.append(c)
            if s.find('N:')!=-1: 
                try:  
                    if isinstance(symbol,list):
                        realDuration=symbol[1]
                        mytie=symbol[2]
                        
                    sep=s.index("_")
                    duration=s[sep+1:]
                    #*************************************
                    #duration vs realDuration for triplets
                    if realDuration!=None:
                        duration=realDuration
                    #*************************************    
                    if(float(duration)>0):
                        n=note.Note(s[2:sep],quarterLength=float(duration))
                        if symbol[5]!=None:
                            n.color=symbol[5]                     
                        if mytie!="":
                            n.tie=tie.Tie(mytie)
                        if len(symbol)>6:#voices
                            measure.voices[symbol[6]].append(n)
                        else:
                            measure.append(n)
                except:
                    print "error"+s
                    
            if s.find('R:')!=-1: 
                try:
                    if isinstance(symbol,list):
                        realDuration=symbol[1]
                        mytie=symbol[2]
                    duration=s[2:]
                    #*************************************
                    #duration vs realDuration for triplets
                    if realDuration!=None:
                        duration=realDuration
                    #*************************************
                    n=note.Rest(quarterLength=float(duration))
                    if symbol[5]!=None:
                        n.color=symbol[5]   
                    if len(symbol)>6:#voices
                        measure.voices[symbol[6]].append(n)
                    else:
                        measure.append(n)
                except:
                    print "error"+s
                
            if s.find('C:')!=-1: 
                notes=s.split("[:")
                cPitch=[]
                for n in notes:
                    if n!='C:':
                        sep=n.index("_")
                        duration=n[sep+1:]
                        pitch= n[0:sep]
                        cPitch.append(pitch)
                c=chord.Chord(cPitch)
                c.duration.quarterLength=float(duration)
                if symbol[5]!=None:
                    c.color=symbol[5]
                if mytie!="":
                    c.tie=tie.Tie(mytie)
                
                if len(symbol)>6:#voices
                    measure.voices[symbol[6]].append(c)
                else:
                    measure.append(c)
   
            if s.find('!')!=-1:
                if isinstance(symbol,list):
                    barType= symbol[1]
                    barRepeat= symbol[2]
                    if barType!="":
                        try:
                            mybartype=bar.styleToMusicXMLBarStyle(barType)
                            myBar=bar.Barline(style=mybartype)
                            measure.rightBarline=myBar
                        except:
                            print "error barline"
    
                    if barRepeat!="":
                        try:
                            myBar=bar.Repeat(direction=barRepeat)
                            if barRepeat=="start":
                                measure.leftBarline=myBar
                            if barRepeat=="end":
                                measure.rightBarline=myBar
                        except:
                            print "error barline"
                sPart.append(measure)
                measureIndex+=1
                measure=stream.Measure()
                measure.number=measureIndex
                for v in range(voicesLength):
                    voice=stream.Voice()
                    voice.id=v
                    measure.append(voice)
                    
            indexS+=1        
        
        sOut.append(sPart)  
        return sOut
                
            
        

    def __orderChord(self,mychord):
        '''
        Private function that returns a chord ordered
        in a string from lower to higher
        '''
        midi=[]
        midi2=[]
        orderC=[]
        for n in mychord:
            if isinstance(n,note.Note):
                midi.append(n.midi)
                midi2.append(n.midi)
            
        while len(midi)>0:
            indexMin=midi2.index(min(midi))
            indexPop=midi.index(min(midi))
            orderC.append(mychord[indexMin])
            midi.pop(indexPop)
            
        myOrderChord=chord.Chord(orderC)
        myOrderChord.duration.quarterLength=mychord.duration.quarterLength
        return myOrderChord
        
        
    def __getKeyOffset(self,item):
        '''
        Private function that returns the offset of one item
        '''
        return item['offset']
    
    def __removeDuplicates(self,input_raw):
        '''
        Private function to remove duplicates in the string input
        '''
        seen = set()
        new_l = []
        for d in input_raw:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_l.append(d)

        return new_l
    
    
    def getElementsFromMeasureOrderByOffset(self,measure):
        '''
        Returns the symbols of a measure ordered by offset
        '''
        offset=measure.flat.offsetMap
        offset_n=self.__removeDuplicates(offset)
        sorted_offset=sorted(offset_n,key=self.__getKeyOffset)
        return sorted_offset
    
    def __swapSymbols(self,s1,s2):
        '''
        Swap the s1,s2 symbols
        '''
        inter=s1
        s1=s2
        s2=inter
        return s1,s2
    
    def orderSymbolsByPitch(self,symbols):
        '''
        Orders the symbol string from lower to high if they have
        the same offset
        '''
        for i in range(len(symbols)-1):   
            for j in range(i,i+2):
                pitch_i=0
                pitch_j=0
                if(symbols[i]['offset']==symbols[j]['offset']):
                    if isinstance(symbols[i]['element'],note.Note):
                        pitch_i=symbols[i]['element'].pitch.midi
                    if isinstance(symbols[j]['element'],note.Note):
                        pitch_j=symbols[j]['element'].pitch.midi
                        
                    if pitch_j>pitch_i:#higher pitch first
                        symbols[i],symbols[j]=self.__swapSymbols(symbols[i],symbols[j])
                        
                    if pitch_j==pitch_i and pitch_j>0:#longest first if equal pitch
                        if symbols[i]['element'].duration<symbols[j]['element'].duration:
                            symbols[i],symbols[j]=self.__swapSymbols(symbols[i],symbols[j])
                            
                    if isinstance(symbols[j]['element'],note.Rest):#rest first
                            symbols[i],symbols[j]=self.__swapSymbols(symbols[i],symbols[j])
                            
        return symbols
                
    def getRepetitionMarks(self,measure):
        '''
        Returns the repetition marks symbol from a measure
        '''
        symbols=[]
        for barline in measure.getElementsByClass(bar.Barline):
            symbol={'voiceIndex': None, 'element': barline, 'endTime': 0.0, 'offset': barline.offset}
            symbols.append(symbol)
        return symbols
    
    def getTS(self,measure):
        '''
        Returns the time signature symbol from a measure
        '''
        symbols=[]
        for ts in measure.getElementsByClass(meter.TimeSignature):
            symbol={'voiceIndex': None, 'element': ts, 'endTime': 0.0, 'offset': ts.offset}
            symbols.append(symbol)
        return symbols
    
    def removeTS(self,symbols):
        '''
        Removes the time signature from the symbols array
        '''
        for symbol in symbols:
            s=symbol['element']
            if 'TimeSignature' in s.classes:
                symbols.pop(symbols.index(symbol))
                break
        return symbols   
                        
    def filterOMR(self,omr,idPart):
        '''
        Removes elements from the music21 input as text, slurs and expressions (p, mp, f...)
        
        Returns the omr filtered and the symbols array converted
        
        '''
        omr_filtered=stream.Stream()
        omr_symbols=[]
        #for single parts
        print "Partes=",len(omr.parts)
        if len(omr.parts)==1:
            idPart=0
        if len(omr.parts)==0:
            idPart=0
            mypart=omr
        if len(omr.parts)>=1:
            if(int(idPart)>=len(omr.parts)):
                print "error in OMR"
                return [],[]
            mypart=omr.parts[int(idPart)]


        
        isFirstClef=True
        indexMes=0
        print idPart
        for measure in mypart.getElementsByClass(stream.Measure):
            indexMes+=1
            symbols=self.getElementsFromMeasureOrderByOffset(measure.semiFlat)#key signature time signature and clef are missing if not flat
            symbols=self.orderSymbolsByPitch(symbols)
            symbolsRepetition=self.getRepetitionMarks(measure)
            symbolsTS=self.getTS(measure)
            symbols=self.removeTS(symbols)
            symbols=symbolsTS+symbols+symbolsRepetition
            
            newMeasure=stream.Measure()
            styleBarline=""
            directionRepeat=""
            strClef=""
           
            for symbol in symbols:
                #symbol={'voiceIndex': 0, 'element': <music21.note.Note C>, 'endTime': 1.0, 'offset': 0.0}
                s=symbol['element']
                if 'TimeSignature' in s.classes:
                    newMeasure.append(s)
                    str0="TS:"+str(s.numerator)+"/"+str(s.denominator)
                    omr_symbols.append([str0,None,None,symbol['offset'],symbol['endTime'],None])
                    
                elif 'KeySignature' in s.classes:
                    newMeasure.append(s)
                    str0="KS:"+str(s.sharps)
                    omr_symbols.append([str0,None,None,symbol['offset'],symbol['endTime'],None])
                    
                elif 'Clef' in s.classes:
                    newMeasure.append(s)
                    strClef="CL:"+str(s.sign)
                    if isFirstClef:
                        omr_symbols.append([strClef,None,None,symbol['offset'],symbol['endTime'],None])
                        strClef=""
                        isFirstClef=False

                elif 'Note' in s.classes:
                    newMeasure.append(s)
                    mytype=s.duration.type
                    duration=note.duration.convertTypeToQuarterLength(mytype)
                    realDuration=s.duration.quarterLength
                    if realDuration==duration+duration/2: #dot case
                        duration=realDuration
                    n="N:"+s.pitch.nameWithOctave+"_"+str(duration)
                    # Ties case
                    mytie=""
                    if s.tie!=None:
                        mytie=s.tie.type
                        
                    if float(realDuration)>0:
                        omr_symbols.append([n,realDuration,mytie,symbol['offset'],symbol['endTime'],s.color] )

                elif 'Rest' in s.classes:
                    newMeasure.append(s)
                    mytype=s.duration.type
                    if mytype!="complex":
                        duration=note.duration.convertTypeToQuarterLength(mytype)
                    else:
                        duration=s.duration.quarterLength
                    realDuration=s.duration.quarterLength
                    if realDuration==duration+duration/2: #dot case
                        duration=realDuration    
                    n="R:"+str(duration)
#                     realDuration=s.duration.quarterLength
                    omr_symbols.append([n,realDuration,False,symbol['offset'],symbol['endTime'],s.color])
                    
                elif 'Chord' in s.classes:
                    if type(s) is not harmony.ChordSymbol:
                        newMeasure.append(s)  
                        mytype=s.duration.type
                        duration=note.duration.convertTypeToQuarterLength(mytype)
                        realDuration=s.duration.quarterLength
                        if realDuration==duration+duration/2: #dot case
                            duration=realDuration
                        chord="C:"
                        sOrder=self.__orderChord(s)
                        for n in sOrder:
                            chord+="[:"+n.pitch.nameWithOctave+"_"+str(duration)
                        
                        

                        # Ties case
                        mytie=""
                        if s.tie!=None:
                            mytie=s.tie.type
                        omr_symbols.append([chord,realDuration,mytie,symbol['offset'],symbol['endTime'],s.color])
                        
                elif 'Barline' in s.classes:
                    styleBarline=s.style
                    try:
                        directionRepeat=s.direction
                    except:
                        directionRepeat=""

           
            omr_symbols.append(['!',styleBarline,directionRepeat,symbol['offset'],symbol['endTime'],None])
            if strClef!="":
                omr_symbols.append([strClef,None,None,0,0,None])
            omr_filtered.append(newMeasure)
        return omr_filtered,omr_symbols
    
    def removeExtraTies(self,arraySymbols):
        '''
        Removes the non logical ties from the symbol array 
        
        '''
        for s in arraySymbols:
            if isinstance(s,list):
                mainSymbol=s[0]
                if mainSymbol.find('N:')!=-1: 
                    tie1=s[2]
                    if arraySymbols.index(s)<len(arraySymbols):
                        sNext=arraySymbols[arraySymbols.index(s)+1]
                        if isinstance(sNext,list):
                            mainSymbol2=sNext[0]
                            if mainSymbol2.find('N:')!=-1: 
                                tie2=sNext[2]
                                if tie1=='start' and tie2!='end':
                                    s[2]=''

        return arraySymbols
     

    def setVoices(self,strSymbols):
        '''
        Divides each measure in voices, if it is necessary.
        
        The output is the symbol string using voices
        
        '''
        quarters=self.__getTimeSignatureQuarters(strSymbols)
        measures=self.__chopMeasures(strSymbols)
        newString=[]
        for measure in measures:
            newMeasure=self.divideMeasureinVoices(measure,quarters)
            for s in newMeasure:
                newString.append(s)
        return newString
    
    def __getTimeSignatureQuarters(self,strSymbols):
        '''
        returns the number of quarters of the first time signature found
        '''
        quarters=4 #4/4 by default
        for s in strSymbols:
            if isinstance(s,list):
                s=s[0]
            if s.find('TS:')!=-1:
                ts=s[3:]
                timeSig=ts.split("/")
                num=int(timeSig[0])
                den=int(timeSig[1])
                quarters=(4/den)*num
        return quarters
    
    def __chopMeasures(self,strSymbols):
        '''
        Divides the symbol string in measures
        '''
        strMeasures=[]
        strMeasure=[]
        for s in strSymbols:
            strMeasure.append(s) 
            bar=self.__getSymbolMesure(s)
            if bar!=None:
                strMeasures.append(strMeasure)
                strMeasure=[]
        return strMeasures
    
    
    def isNoteRest(self,symbol):
        '''
        Returns true if the symbol is note, rest or chord
        '''
        s=symbol
        if isinstance(s,list):
            if s[0].find('N:')!=-1:   
                return True
            if s[0].find('R:')!=-1:   
                return True
            if s[0].find('C:')!=-1:   
                return True
            return False
        return False
        
    def divideMeasureinVoices(self,strMeasure,quarters):
        '''
        If the length of each measure in the string is higher than quarters,
        adjusting to voices
        
        '''
        newMeasure=[]
        duration=0
        #if duration is higher than time signatura
        for s in strMeasure:
                if self.isNoteRest(s):
                    if s[1]!=None:
                        try:
                            duration+=s[1]
                        except:
                            pass
        # voices only if needed
        if duration<=quarters:
            return strMeasure
        
        
        for s in strMeasure:
            if not self.isNoteRest(s):
                if self.__getSymbolMesure(s)==None: 
                    newMeasure.append(s)
        voiceslength=8          
        for v in range(voiceslength-1):
            offset=0.0
            firstNote=False
            for s in strMeasure:
                if self.isNoteRest(s):
                    if len(s)<7:#not voice yet
                        offsetNote=s[3]
                        if firstNote==False:
                            offset=offsetNote 
                            firstNote=True
                            if offsetNote>0:
                                rest=[]
                                rest.append("R:"+str(offsetNote))
                                rest.append(offsetNote)
                                rest.append(False)
                                rest.append(0)
                                rest.append(offsetNote)
                                rest.append(None)
                                rest.append(v)
                                newMeasure.append(rest)
                        if(offset==offsetNote):
                            s.append(v)
                            newMeasure.append(s)
                            offset=s[4]
                    
        
        for s in strMeasure:
            if self.__getSymbolMesure(s)!=None: 
                newMeasure.append(s)
                

        return newMeasure        