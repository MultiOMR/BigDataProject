'''
Created on 10/11/2014

@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

Functions related to SIKULI automatism 
'''
import logging
import os
import sys
from subprocess import Popen
import shutil
from music21 import converter
from Functions import FilesFunctions



class BatchOMR:
    '''
    Class for the SIKULI process
    '''
    ##################################################
    # @param idOMR It can be "SE" "SS" "CP" "PS" "ALL"   
    # @param dirName folder where the images are and .xml will be
    # @param files array with tiff files
    def Batch(self,idOMR,dirName,files):
        '''
        Runs the SIKULI process.
        - idOMR: SE, SS, CP, PS    
        - if exists, skip
        - it takes all the .tif files  and convert them to SE.xml, SS.xml, CP.xml or PS.xml
        - it waits until the process is finished
        
        usage:
        ff=FilesFunctions()
        dirName="C:\\Users\\victor\\Desktop\\data"
        files= ff.getAllImgFiles(dirName)
        batchOMR=BatchOMR()
        batchOMR.Batch("PS",dirName,files)
        '''

        print "Processing...",dirName+"/"+idOMR+".xml"
        if os.path.exists(dirName+"/"+idOMR+".xml"):
            print "....Completed ",dirName+"/"+idOMR+".xml"
            return
        rootApp=os.path.dirname(sys.argv[0])
        rootApp=rootApp.replace("\\","/")
        print rootApp
        strFiles=""
        for f in files:
            strFiles=strFiles+" \""+f+"\""
        print dirName,strFiles
    
        dirName=dirName.replace("\\","/")
        dirName="\""+dirName+"/\""
        
        cwd=rootApp+"/sikuli1.0.1/runScript.cmd -r "+rootApp+"/sikuli/"+idOMR+".sikuli --args "
        cwd=cwd+dirName+strFiles
        print cwd
        p = Popen(cwd)
        p.wait()
        p.communicate()
        print "....Completed ",dirName+"/"+idOMR+".xml"
    
    
    ###############################################
    # @param rootDir root process folder    
    def cleanXMLFiles(self,rootDir):
        '''
        Removes all the .xml files and .mro files in the tree folder
        It is used for testing mainly
        
        usage:
        
        batchOMR=BatchOMR()
        batchOMR.cleanXMLFiles("C:\\Users\\victor\\Desktop\\data")
        '''
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            fileList=outWalk[2]
            for myfile in fileList:
                if myfile.endswith('.xml'):
                    os.remove(dirName+"/"+myfile)
                    print myfile
                if myfile.endswith('.mro'):
                    os.remove(dirName+"/"+myfile)
                    print myfile
        
                    
    ###############################################
    # @param rootDir root process folder    
    # @param idOMR can be "PS" "CP" "SE" "SS" "ALL"           
    def processAllTiffFiles(self,rootDir,idOMR):
        '''
        Runs the complete process for the tree folder
        idOMR can be:
            PS
            CP
            SE
            SS
            ALL (run all the OMRs). Capella is removed for many problems associated
            
        usage:
        
        batchOMR=BatchOMR()
        batchOMR.processAllTiffFiles("C:\\Users\\victor\\Desktop\\data","SE")
        '''
        print rootDir
        logging.basicConfig(filename=rootDir+'\\BigDataLogs.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            print('Found directory: %s' % dirName)
            ff=FilesFunctions()
            files= ff.getAllImgFiles(dirName)
            if len(files)>0:
                logging.warning(idOMR+" "+dirName)
                if idOMR=="PS":
                    self.Batch("PS",dirName,files)
                if idOMR=="SE":
                    self.Batch("SE",dirName,files)
                if idOMR=="SS":
                    self.Batch("SS",dirName,files)
                if idOMR=="CP":
                    self.Batch("CP",dirName,files)
                if idOMR=="ALL":
    #                 logging.warning("CP: "+dirName)
    #                 Batch("CP",dirName,files)
                    logging.warning("PS: "+dirName)
                    self.Batch("PS",dirName,files)
                    logging.warning("SE: "+dirName)
                    self.Batch("SE",dirName,files)
                    logging.warning("SS: "+dirName)
                    self.Batch("SS",dirName,files)
    
    
    ###############################################
    # @param rootDir root process folder      
    def setupApp(self,rootDir):
        '''
        Configures the main folder to process the data
        Creates the "Process" close to "OMRS" folder and copy the .xml files.
            - the parts files in "part/XML" folder with the structure:
                                - idpart.version.omrId.xml
            - the full scores in fullScore/XML" folder with the structure:
                                - FS.version.omrId.xml
        usage:
        batchOMR=BatchOMR()
        batchOMR.setupApp("C:\\Users\\victor\\Desktop\\data")                  
        '''
        ff=FilesFunctions()
        ################
        # FOR PARTS ####
        ################
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            subdirList=outWalk[1]
            if "OMRS" in subdirList:
                rootScore=dirName
            if(dirName.upper().find("\\OMRS\\")!=-1 and dirName.upper().find("\\XML")!=-1 and dirName.upper().find("\\PARTS")!=-1):
                arrDir=dirName.split("\\")
                idpart=arrDir[len(arrDir)-2]  
                version=arrDir[len(arrDir)-3] 
                idmovement=arrDir[len(arrDir)-5] 
                files= ff.getAllXMLFiles(dirName)
                myfolder=rootScore+"\\Process\\"+idmovement+"\\parts\\"+idpart+"\\XML\\"
                if not os.path.exists(myfolder):
                    os.makedirs(myfolder)
                for f in files:
                    if not os.path.isfile(myfolder+idpart+"."+version+"."+f):
                        shutil.copy2(dirName+"\\"+f, myfolder+idpart+"."+version+"."+f)
                           
        ###########################
        # FOR FULL SCORE ##########
        ###########################  
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            subdirList=outWalk[1]
            if "OMRS" in subdirList:
                rootScore=dirName
            if(dirName.upper().find("\\OMRS\\")!=-1 and dirName.upper().find("\\XML")!=-1 and dirName.upper().find("\\FULLSCORE")!=-1):
                arrDir=dirName.split("\\")
                version=arrDir[len(arrDir)-2] 
                idmovement=arrDir[len(arrDir)-4] 
                files= ff.getAllXMLFiles(dirName)
                myfolder=rootScore+"\\Process\\"+idmovement+"\\fullScore\\XML\\"
                for f in files:
                    if not os.path.exists(myfolder):
                        os.makedirs(myfolder)
                    if not os.path.isfile(myfolder+"FS."+version+"."+f):
                        shutil.copy2(dirName+"\\"+f, myfolder+"FS."+version+"."+f)

                        
                        
                    
        
    ####################################
    # @param rootDir root process folder       
    def setGround(self,rootDir):
        '''
        Process kern files in the OMRS folder (.krn) and set them as a "ground.xml"
        in "Process" folder
        
        usage:
        batchOMR=BatchOMR()
        batchOMR.setGround("C:\\Users\\victor\\Desktop\\data")
        '''
        for outWalk in os.walk(rootDir):
            dirName=outWalk[0]
            ff=FilesFunctions()
            kernFile=ff.getKernFile(dirName)
            newpath=dirName.replace("\\OMRS\\","\\Process\\")
            
            if not os.path.isfile(newpath+'\\ground.xml'):
                if kernFile!=None:
                    
                    print dirName+"\\"+kernFile
                    xmlFile=ff.getXMLFile(dirName)
                    
                    #if we have a .xml file, we copy it
                    if xmlFile!=None:
                        shutil.copyfile(dirName+"\\"+xmlFile,newpath+"\\ground.xml")
                    else:
                        omr=converter.parse(dirName+"\\"+kernFile)
                        omr.write("musicxml", newpath+'\\ground.xml')
    
