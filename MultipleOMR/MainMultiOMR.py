'''
@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

The application can be run through command line (without windows interface) using 
MainMultiOMR library

'''
import logging
import time
import os
import gc
import sys
from subprocess import Popen
from music21 import stream
from music21 import converter
from Process import PipelineAlignment
from Process import Voting
from Process import SymbolConversion
from Process import FullScoreAlignment
from Automatism import BatchOMR
from Result import ProcessGroundS2
from Result import ExcellData
from Functions import FilesFunctions
from Functions import MeasureFunctions
from Alignment import NWunsch

from Preprocessing import ossia

class MainMultiOMR:
    '''
    main functions to run the Big Data Process. 
    They can be called without interface, from another program, for example
    ....
    # instance
    mmOMR=MainMultiOMR()
    
    # run the Big Data process once
    mmOMR.runBigData("C:\\Users\\victor\\Desktop\\data")
    
    # run the Big Data waiting for changes
    mmOMR.runDummyBigData("C:\\Users\\victor\\Desktop\\data")
    
     # run the Big Data Ground process once to get the results
    mmOMR.runBigDataGroung("C:\\Users\\victor\\Desktop\\data")
    
    # run the Big Data Ground waiting for changes
    mmOMR.runDummyBigData("C:\\Users\\victor\\Desktop\\data")
    '''
    
    def _loadNWunsch(self):
        '''
        Load Needlemann-Wunsch algorith library by default
        '''
        a=["foo00"]
        b=["foo000"]
        NWunsch.NWunsch_getSimilarity(a,b)
        #print "Default NWunsch......"
        
        
    def processOssia(self,rootDir):   
    ###############################################
    # @param dirGeneral root movement folder
        for dirname, dirnames, filenames in os.walk(rootDir):
            for f in filenames:
                fname_path = os.path.join(dirname, f)
                if f.endswith(".tif"):
                    print fname_path
                
                    ossia.process(fname_path, fname_path)
#                     rootApp=os.path.dirname(sys.argv[0])
#                     rootApp=rootApp.replace("\\","/")
#                     cwd="python.exe "+rootApp+"/Preprocessing/ossia.py "+fname_path+" "+fname_path
#                     
#                     print cwd
#                     p = Popen(cwd)
#                     p.wait()
#                     p.communicate()
#     
               
                    
    def processMovement(self,dirGeneral):
        '''
        Process just one movement. The structure should be
        ....
        \\movementName\\fullScore\\XML\\(the .xml files)
                      \\parts\\0\\
                             \\1\\
                             \\2\\XML\\(the .xml files)
                             
        the result is \\movementName\\finalScore.xml
        
        usage:
        mmOMR=MainMultiOMR()
        mmOMR.processMovement("C:\Users\victor\Desktop\data\k458\Process\m2")
        '''
       
        
        ff=FilesFunctions()
        subdirnameParts=ff.SubDirPath(dirGeneral+"\\Parts\\") 
        fsOMRs_files=ff.getFiles(dirGeneral+"\\fullScore\\XML\\")   
        for dirname in subdirnameParts:
            d=dirname+"/XML/"
            urlSplit=dirname.split("\\")
            part=int(urlSplit[-1])
            partOMRs_files=ff.getFiles(d) 
            print "---------S2------------"
            logging.warning("Part:"+str(part)+" "+d)
            self.setResultS2(d,part,fsOMRs_files,partOMRs_files)
        
        print "---------Synchronising scores and parts------------"
        logging.warning("---------Synchronising scores and parts------------:"+dirGeneral)
        #fsOMRs=ff.getOMRs(dirGeneral+"\\fullScore\\XML\\")   
        self.__runSynchroScoresAndParts(dirGeneral,fsOMRs_files)    
    
    ###############################################
    # @param path folder where the .xml files are 
    # @param idPart part number 
    # @param fsOMRs array with the full score files processed by music21
    # @param partOMRs array with the part files processed by music21
    def setResultS2(self,path,idPart,fsOMRs,partOMRs):
        '''
        Takes the fullScores (processing the idPart) and parts.
        It writes the result (result.S2.xml) in the dirname
        
        This function process each part independently
        
        usage:
        
        mmOMR=MainMultiOMR()
        ff=FilesFunctions()
        fsOMRs=ff.getOMRs("C:\\Users\\victor\\Desktop\\data\\k458_test\\Process\\m2\\fullScore\\XML")
        partOMRs=ff.getOMRs("C:\\Users\\victor\\Desktop\\data\\k458_test\\Process\\m2\\parts\\0\\XML")
        d="C:\\Users\\victor\\Desktop\\data\\k458_test\\Process\\m2\\parts\\0\\XML"
        mmOMR.setResultS2(d,0,fsOMRs,partOMRs)
        '''
        
        
        
        pa=PipelineAlignment()
        vote=Voting()
        sc=SymbolConversion()
        ff=FilesFunctions()
        omr_symbolsAlign,betterOmrIds=pa.alignNJ_files(idPart,fsOMRs,partOMRs)
        #The .txt with the OMRs involved (tree) 
        ff.writeText(path,betterOmrIds)
        #voting
        
        outVote=vote.vote(omr_symbolsAlign)
        #apply voices if it is needed
        
        outVote=sc.setVoices(outVote)
        #convert to music21
        resultS2=sc.convertM21(outVote)
        mf=MeasureFunctions()
        #remove blank measures due to the alignment
        resultS2_clean=mf.filterExtraMeasures(resultS2)
        resultS2_clean.write("musicxml", path+'/result.S2.xml')
        

    ###############################################
    # @param dirGeneral folder where is the root of the movement 
    # @param fsOMRs array with the full score files processed by music21    
    def __runSynchroScoresAndParts(self,dirGeneral,fsOMRs_files):
        '''
        Takes the fullScores and part files generated to align the final full score
        - dirGeneral is the movement URL
        - fsOMRs is an array with the full scores OMRs processed by music21
        '''
        ff=FilesFunctions()
        subdirnameParts=ff.SubDirPath(dirGeneral+"\\parts\\")
        partsNumber=len(subdirnameParts)
        fsa=FullScoreAlignment()   
        idCompleteScoreBetter=fsa.getIdBetterOMRFullScore(fsOMRs_files,partsNumber)
        betterFsOMR=ff.getOMR(fsOMRs_files[idCompleteScoreBetter])
        finalScore=fsa.runSynchronisingMeasuresNJ(subdirnameParts,betterFsOMR) 
        betterFsOMR=None 
        finalScore.write("musicxml", dirGeneral+'/finalScore.xml')   
        finalScore=None
        gc.collect()
        print "----"
        
        

    ###############################################
    # @param dirGeneral root movement folder
    def processMovementGround(self,dirGeneral):
        '''
        Process the result. Just one movement. It takes each OMR file and compare against the ground.
        The differences are written in .XML and .xls
        
         ....
        \\movementName\\fullScore\\XML\\(the .xml files)
                      \\parts\\0\\
                             \\1\\
                             \\2\\XML\\(the .xml files)
                             
        the file finalScore.xml should be in \\movementName\\finalScore.xml
        the file ground.xml should be in \\movementName\\ground.xml
        
        The final result is written in 
        \\movementName\\parts\\resultGeneral.xlsx
                             \\fullScore_errors.xml
        
        usage:
        mmOMR=MainMultiOMR()
        mmOMR.processMovementGround("C:\Users\victor\Desktop\data\k458\Process\m2")
        '''
        percentagesArray=[]
        betterOMRIds=[]
        ff=FilesFunctions()
        subdirname=ff.SubDirPath(dirGeneral+"\\parts\\")
        filesFull=ff.getFiles(dirGeneral+"\\fullScore\\XML\\") 
    
        ground=ff.getGround(dirGeneral)
        groundparsed=converter.parse(ground, forceSource=True)
        finalScore=ff.getFinalScore(dirGeneral)
        finalScoreparsed=converter.parse(finalScore, forceSource=True)
            
       
        for dirname in subdirname:
            d=dirname+"/XML/"
            urlSplit=dirname.split("\\")
            part=int(urlSplit[-1])
            filesPart=ff.getFiles(d)
            files=filesPart+filesFull

            print files
            pg=ProcessGroundS2()
            ErrorsMatrix=[]
            percentages=[]
    
            OMRs=[]
            OMRs.append(groundparsed)
            OMRs.append(finalScoreparsed)
           
           
    
            percentage,errors,scoreWithErrors= pg.getSimilarity(OMRs,part)       
            ErrorsMatrix.append(errors)
            percentages.append(percentage)
            if not os.path.exists(dirname+"\\Result"):
                os.makedirs(dirname+"\\Result")
          
            scoreWithErrors.write("musicxml", dirname+"\\Result\\result.S2.xml")
           
            for i in range(len(files)):
                try:
                    OMRs[1]=ff.getOMR(files[i])
                    percentage,errors,scoreWithErrors= pg.getSimilarity(OMRs,part)
                    ErrorsMatrix.append(errors)
                    percentages.append(percentage)
                    scoreWithErrors.write("musicxml", dirname+"\\Result\\"+os.path.basename(files[i]))
                except:
                    print "ERROR OMR READING"
                    ErrorsMatrix.append("ERROR OMR READING")
                    percentages.append(0)
        
               
            f=open(d+"betterOMR.txt","r") 
            betterOMRId=f.readlines()
            f.close()
            betterOMRIds.append(betterOMRId)
            print "betterOMRIds",betterOMRIds
            ed=ExcellData()
            files.insert(0,dirname+"\\Result\\result.S2.xml" )
            print files
            ed.saveData(ErrorsMatrix,files,percentages)  
            percentagesArray.append(percentages)  
           
            
        ed=ExcellData()
        ed.saveGlobalData(percentagesArray,dirGeneral,betterOMRIds,files)  
        self.__joinErrorParts(dirGeneral)
        print "----------- END ------------"
   
    ################################################################
    # @param rootDir root folder where all the scores to process are
    def runBigData(self,rootDir): 
        '''
        Checks if there is any folder to process 
        If the folder "Process" is written, but the "finalScore.xml" is not,
            runs the procedure
        
        usage
        
        mmOMR=MainMultiOMR()
        d="C:\\Users\\victor\\Desktop\\cach"
        mmOMR.runBigData(d)
        '''
        ff=FilesFunctions()
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            arrDir=dirName.split("\\")
            if arrDir[-1]=="Process":
                movements=ff.SubDirPath(dirName)
                for movement in movements:
                    print movement
                    if not os.path.isfile(movement+"\\finalScore.xml"):
                        logging.warning("Movement:"+movement+" "+rootDir)
                        self.processMovement(movement) 
   
    ################################################################
    # @param rootDir root folder where all the scores to process are
    def runLoopBigData(self,rootDir,adaptOMRs=False):
        '''
        Infinity loop for processing data
        Checks if there is any folder to process 
        If the folder "Process" is written, but the "finalScore.xml" is not,
            runs the procedure
        
        usage
        
        mmOMR=MainMultiOMR()
        d="C:\\Users\\victor\\Desktop\\cach"
        mmOMR.runLoopBigData(d)
        '''
        batchOMR=BatchOMR()
        ff=FilesFunctions()
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            subdirList=outWalk[1]
            if "OMRS" in subdirList:
                rootScore=dirName
                omrFinished=True
                scoreFinished=True
                for outWalk2 in os.walk(rootScore):
                    dirName2=outWalk2[0]
                    files= ff.getAllImgFiles(dirName2)
                    omrs=ff.getAllXMLFiles(dirName2)
                    if len(files)>0 and len(omrs)<4:
                        omrFinished=False
                        
                if os.path.exists(rootScore+"\\Process"):
                    movements=ff.SubDirPath(rootScore+"\\Process")
                    for movement in movements:
                        if not os.path.isfile(movement+"\\finalScore.xml"):
                            scoreFinished=False
                else:
                    scoreFinished=False 
                        
                        
                if omrFinished==True and scoreFinished==False:
                    print "---- CONFIGURE SCORES ---"
                    batchOMR.setupApp(rootScore)
                    print "---- CONFIGURE GROUND ---"
                    batchOMR.setGround(rootScore)
                    if adaptOMRs:
                        print "---- ADAPT OMRs ---"
                        self.runAdaptAllOMRs(rootScore+"\\Process")
                    print "---- RUN BIG DATA ---"
                    self.runBigData(rootScore)
        print "Waiting for processing..."
        time.sleep(5)  
        self.runLoopBigData(rootDir,adaptOMRs)
                     
                             
    ################################################################
    # @param rootDir root folder where all the scores to process are                   
    def runBigDataGround(self,rootDir):
        '''
        Checks if there is any folder to process to get the result
        If "resultGeneral.xlsx" is not written and "finalScore.xml" and "ground.xml" are in the movement root dir,
        launches the process
        
        usage
        
        mmOMR=MainMultiOMR()
        d="C:\\Users\\victor\\Desktop\\data"
        mmOMR.runBigDataGround(d)
        '''
        ff=FilesFunctions()
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            arrDir=dirName.split("\\")
            if arrDir[-1]=="Process":
                movements=ff.SubDirPath(dirName)
                for movement in movements:
                    if not os.path.isfile(movement+"\\parts\\resultGeneral.xlsx"):
                        if os.path.isfile(movement+"\\finalScore.xml") and os.path.isfile(movement+"\\ground.xml") :
                            self.processMovementGround(movement)
                            
    ################################################################
    # @param rootDir root folder where all the scores to process are                   
    def runFinalXLS(self,rootDir):
        '''
        Checks if there is any folder to process to get the result
        If "resultGeneral.xlsx" is not written and "finalScore.xml" and "ground.xml" are in the movement root dir,
        launches the process
        
        usage
        
        mmOMR=MainMultiOMR()
        d="C:\\Users\\victor\\Desktop\\data"
        mmOMR.runBigDataGround(d)
        '''
        ed=ExcellData()
        files=0
        S2_sum=0
        CP_sum=0
        PS_sum=0
        SE_sum=0
        SS_sum=0
        ff=FilesFunctions()
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            arrDir=dirName.split("\\")
            if arrDir[-1]=="Process":
                movements=ff.SubDirPath(dirName)
                for movement in movements:
                    if os.path.isfile(movement+"\\parts\\resultGeneral.xlsx"):
                        files=files+1
                        s2,cp,ps,se,ss=ed.processResultGeneral(movement+"\\parts\\resultGeneral.xlsx")
                        S2_sum=S2_sum+s2
                        CP_sum=CP_sum+cp
                        PS_sum=PS_sum+ps
                        SE_sum=SE_sum+se
                        SS_sum=SS_sum+ss
        ed.writeFinalXLS(rootDir,S2_sum/files,CP_sum/files,PS_sum/files,SE_sum/files,SS_sum/files)             
                            
    ################################################################
    # @param rootDir root folder where all the scores to process are 
    def runLoopBigDataGround(self,rootDir):
        '''
        Infinity loop for getting the results
        
        If "resultGeneral.xlsx" is not written and "finalScore.xml" and "ground.xml" are in the movement root dir,
        launches the process
        
        usage
        
        mmOMR=MainMultiOMR()
        d="C:\\Users\\victor\\Desktop\\data"
        mmOMR.runLoopBigDataGround(d)
        '''
        self.runBigDataGround(rootDir)
        print "Waiting for results..."
        time.sleep(5)  
        self.runLoopBigDataGround(rootDir)
        

    ################################################################
    # @param dirGeneral root folder of the movement 
   
    def __joinErrorParts(self,dirGeneral):
        '''
        Joins the different result.S2.xml error in a single file.
        The output file is "fullScore_errors.xml"
        
        The function tries to find the file "parts\\[idMovement]\\Result\\result.S2.xml" in each part
        '''
        ff=FilesFunctions()
        subdirname=ff.SubDirPath(dirGeneral+"\\parts\\")
        fullScore=stream.Score()
        for dirname in subdirname:
            d=dirname+"\\Result\\"
            urlSplit=dirname.split("\\")
            part=int(urlSplit[-1])
            f=d+"\\result.S2.xml"
            omr=converter.parse(f, forceSource=True)
            part=omr.getElementsByClass(stream.Part)[0]
            fullScore.append(part)
        fullScore.write("musicxml", dirGeneral+"\\parts\\fullScore_errors.xml")
        

    ###############################################
    # @param rootDir root folder of the general data                                
    def runCompleteProcess(self,rootDir):
        '''
        Instead of working in parallel, this function launches a serial process with the different 
        steps involved
        1.- SIKULI AUTOMATISM
        2.- SETUP APPLICATION (copying files)
        3.- CONVERT GROUND (taking the .krn and convert to ground.xml)
        4.- RUN MULTIOMR BIG DATA
        5.- RUN GET RESULT BIG DATA
        
        
        usage:
        mmOMR=MainMultiOMR()
        d="C:\\Users\\victor\\Desktop\\data"
        mmOMR.runCompleteProcess(d)
        '''
        batchOMR=BatchOMR()
        logging.basicConfig(filename=rootDir+'\\BigDataLogs.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        print "-------SIKULI AUTOMATISM----------"
        logging.warning("---SIKULI AUTOMATISM--- "+rootDir)
        batchOMR.processAllTiffFiles(rootDir,"ALL")
        print "-------SETUP APPLICATION----------"
        logging.warning("---SETUP APPLICATION--- "+rootDir)
        batchOMR.setupApp(rootDir)
        print "-------CONVERT GROUND----------"
        logging.warning("---CONVERT GROUND--- "+rootDir)
        batchOMR.setGround(rootDir)
        logging.warning("------RUN MULTIOMR BIG DATA--- "+rootDir)
        print "-------RUN MULTIOMR BIG DATA----------"
        self.runBigData(rootDir)
        print "-------RUN GET RESULT BIG DATA----------"
        self.runBigDataGround(rootDir)
    
    ###############################################
    # @param filename file to convert  
    def runConvertKrnToMusicXML(self,filename):
        '''
        converts a .krn file to .xml using music21
        
        usage:
        mmOMR=MainMultiOMR()
        file="C:\\Users\\victor\\Desktop\\data\\k458\\OMRS\\m2\\k458.krn"
        mmOMR.runConvertKrnToMusicXML(file)
        '''
        omr=converter.parse(filename)
        omr.write("musicxml", filename+'.xml')
    
    ###############################################
    # @param filename file to convert  
    def runConvertMidiToMusicXML(self,filename):
        '''
        converts a .mid file to .xml using music21
        
        usage:
        mmOMR=MainMultiOMR()
        file="C:\\Users\\victor\\Desktop\\data\\k458\\OMRS\\m2\\k458.mid"
        mmOMR.runConvertKrnToMusicXML(file)
        '''
        omr=converter.parse(filename)
        #Reordering the different staffs
        omrOrdered=stream.Score()
        numberParts=len(omr.parts)
        for i in reversed(range(numberParts)):
            mypart=omr.parts[i]
            
            omrOrdered.insert(0,mypart)
        omrOrdered.write("musicxml", filename+'.xml')
        
    ###############################################
    # @param filename file to convert  
    def runConvertVoicesToChord(self,filename):
        '''

        '''
        mf=MeasureFunctions()
        omr=converter.parse(filename)
        omr=mf.convertVoicesToChord(omr)
        omr.show()
    
    ###############################################
    # @param filename file to convert  
    def runConvertBeamsToTriplets(self,filename):
        '''

        '''
        mf=MeasureFunctions()
        omr=converter.parse(filename)
        omr=mf.convertBeamsToTriplets(omr)
#         omr.show()
        omr.write("musicxml", filename+'.xml')
    
    def runRemovesEmptyVoices(self,filename):
        '''

        '''
        mf=MeasureFunctions()
        omr=converter.parse(filename)
        omr=mf.removesEmptyVoices(omr)
        omr.write("musicxml", filename+'.xml')
        
    def runRemovesGaps(self,filename):
        '''

        '''
        mf=MeasureFunctions()
        omr=converter.parse(filename)
        omr=mf.removesGaps(omr)
        omr.write("musicxml", filename+'.xml')


    def runAdaptOMRs(self,dirname):
        '''
        Runs the following process in one directory.
        1.-Removing GAPS
        2.-Converting voices to chords
        3.-Converting triplets
        4.-Removing Rest Voices
        '''
        ff=FilesFunctions()
        mf=MeasureFunctions()
        files=ff.getFiles(dirname)
        for f in files:
            try:
                print f
                omr=converter.parse(f)
                print "--- Removing GAPS---"
                omr=mf.removesGaps(omr)
               
                print "--- Converting voices to chords---"
                omr=mf.convertVoicesToChord( omr)
                
                print "--- Converting triplets---"
                omr=mf.convertBeamsToTriplets(omr)
                print "--- Removing Rest Voices---"
                omr=mf.removeRestVoice(omr)
                
                omr.write("musicxml", f)
            except:
                pass
                                    
    def runAdaptAllOMRs(self,rootDir):
        '''
        Adapt all the files in one directory tree
        '''
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            self.runAdaptOMRs(dirName)
                   
              

        
           
    ##################################################
    # @param dirname the directory where the files are  
    def runViewM21(self,dirname):
        '''
        Shows all the .xml files in a folder using music21
        to check the differences before and after processing
        
        usage:
        mmOMR=MainMultiOMR()
        dirname="C:\\Users\\victor\\Desktop\\data\\k458\\OMRS\\m2"
        mmOMR.runViewM21(dirname)
        '''
        ff=FilesFunctions()
        mf=MeasureFunctions()
        files=ff.getFiles(dirname)
        for f in files:
            omr=converter.parse(f)
            omr.show()
            omr.show('text')

    
    ##################################################
    # @param dirname the directory where the files are  
    def runViewWrongMeasures(self,dirname):
        '''
        Flags and prints the possible wrong measures
        
        usage:
        mmOMR=MainMultiOMR()
        dirname="C:\\Users\\victor\\Desktop\\data\\k458\\OMRS\\m2"
        mmOMR.runViewWrongMeasures(dirname)
        '''
        ff=FilesFunctions()
        mf=MeasureFunctions()   
        path = dirname
        print("Path:"+path)
        omr_files=ff.getAllFiles(path)   
        for f in omr_files:
            omr=converter.parse(f)
            arrayErrors=mf.flagIncorrectMeasures(omr)[1]
            for array in arrayErrors:
                for i in range(len(array)):
                    array[i]=array[i]+1
            print 
            print f
            print "Errors measures duration:"+str(arrayErrors[0])
            print "Errors measures estimated:"+str(arrayErrors[1])
            print "Errors based on beams:"+str(arrayErrors[2])
            print "Errors based on last notes:"+str(arrayErrors[3])
            
            





    