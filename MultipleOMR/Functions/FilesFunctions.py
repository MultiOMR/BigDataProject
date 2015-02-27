'''
@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

Auxiliary functions to manipulate files and convert to music21
for processing

'''

from music21 import converter
import os

class FilesFunctions:
    
    def getFiles(self,path):
        '''
        Takes the XML files in a folder excluding ground and results 
        returns alphabetically
        
        usage:
        ff=FilesFunctions()
        files=ff.getFiles("C:\\Users\\victor\\Desktop\\data\k458\Process\m2\parts\0\XML")
        '''
        
        omr_files=[]
        dir_content = os.listdir(path)
        dir_content.sort()
        for myfile in dir_content:
            directory = os.path.join(path,myfile)
            extension = os.path.splitext(myfile)[1]
            if myfile.find("result.")==-1 and myfile!="ground.xml" and extension.upper()==".XML":
                omr_files.append(os.path.abspath(directory))
        return omr_files
    
    def getAllFiles(self,path):
        '''
        Takes all the files in a folder
        returns alphabetically
        
        usage:
        ff=FilesFunctions()
        files=ff.getAllFiles("C:\\Users\\victor\\Desktop\\data\k458\Process\m2\parts\0\XML")
        '''
        omr_files=[]
        dir_content = os.listdir(path)
        dir_content.sort()
        for myfile in dir_content:
            directory = os.path.join(path,myfile)
            omr_files.append(os.path.abspath(directory))
        return omr_files
    
        
    def SubDirPath (self,d):
        '''
        Returns the directories from a path
        
        usage:
        ff=FilesFunctions()
        subdirArray=ff.SubDirPath("C:\\Users\\victor\\Desktop\\data\k458\Process\m2\parts")
        
        #returns ["C:\\Users\\victor\\Desktop\\data\k458\Process\m2\parts\1",
                "C:\\Users\\victor\\Desktop\\data\k458\Process\m2\parts\2"....] 
        '''
        return filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)])  
    
    
    def getGround(self,path):
        '''
        Returns the ground file from a path
        
        usage:
        ff=FilesFunctions()
        ground=ff.getGround("C:\\Users\\victor\\Desktop\\data\\k458\\Process")
        '''
        dir_content = os.listdir(path)
        dir_content.sort()
        for myfile in dir_content:
            if myfile=="ground.xml":
                directoryFile = os.path.join(path,myfile)
                return directoryFile
            
            
    def getFinalScore(self,path):
        '''
        Returns the finalScore.xml file from a path
        
        usage:
        ff=FilesFunctions()
        finalScore=ff.getFinalScore("C:\\Users\\victor\\Desktop\\data\\k458\\Process")
        '''
        dir_content = os.listdir(path)
        dir_content.sort()
        for myfile in dir_content:
            if myfile=="finalScore.xml":
                directoryFile = os.path.join(path,myfile)
                return directoryFile 
    
    def writeText(self,path,betterOmrIds):
        '''
        Writes betterOMR.txt file with the number of the OMR files chosen in the phylogenetic tree
        
        usage:
        ff=FilesFunctions()
        betterOmrIds=[2,3,5]
        ff.writeText("C:\\Users\\victor\\Desktop\\data\\k458\\Process",betterOmrIds)
        '''
        f=open(path+"\\betterOMR.txt","w")
        for idOMR in betterOmrIds:
            f.write(str(idOMR)+"\n")
        f.close()
        
    def getOMRs(self,path): 
        '''
        Takes the different .xml in a folder and convert them to music21
        Returns an array with the files processed
        
        ff=FilesFunctions()
        OMRs=ff.getOMRs("C:\\Users\\victor\\Desktop\\data\\k458\\Process\\m2\parts\0\XML",)
        '''
        fsFiles=self.getFiles(path)  
        OMRs=[]
        for f in fsFiles:
            try:
                print f
                OMRs.append(converter.parse(f, forceSource=True))
            except:
                OMRs.append([])
                print "OMR error"
        return OMRs   
    
    def getOMR(self,f): 
        '''
        Takes the  .xml file in a folder and convert them to music21

        '''
        OMR=[]
        try:
            print f
            OMR=converter.parse(f, forceSource=True)
        except:
            OMR=[]
            print "OMR error"
        return OMR  
    def getAllImgFiles(self,d):
        '''
        Returns all the .tif files from a directory ordered alphabetically
        
        usage:
        ff=FilesFunctions()
        imageFiles=ff.getAllImgFiles("C:\\Users\\victor\\Desktop\\data\\k458\\OMRS\\m2\parts\Peters\0\XML",)
        '''
        files=[]
        dir_content = os.listdir(d)
        dir_content.sort()
        for myfile in dir_content:
            if myfile.endswith('.tif'):
                files.append(myfile)
        return files

    def getKernFile(self,d):
        '''
        Returns the first .krn file from a directory ordered alphabetically
        
        usage:
        ff=FilesFunctions()
        kernFile=ff.getKernFile("C:\\Users\\victor\\Desktop\\data\\k458\\Process\\m2\parts\Peters\0\XML",)
        '''
        dir_content = os.listdir(d)
        dir_content.sort()
        for myfile in dir_content:
            if myfile.endswith('.krn'):
                return myfile
    def getXMLFile(self,d):
        '''
        Returns the first .xml file from a directory ordered alphabetically
        
        usage:
        ff=FilesFunctions()
        xmlFile=ff.getXMLFile("C:\\Users\\victor\\Desktop\\data\\k458\\Process\\m2\parts\Peters\0\XML",)
        '''
        dir_content = os.listdir(d)
        dir_content.sort()
        for myfile in dir_content:
            if myfile.endswith('.xml'):
                return myfile
                
    def getAllXMLFiles(self,d):
        '''
        Returns the .xml files from a directory ordered alphabetically
        
        usage:
        ff=FilesFunctions()
        xmlFiles=ff.getAllXMLFiles("C:\\Users\\victor\\Desktop\\data\\k458\\OMRS\\m2\parts\Peters\0\XML",)
        '''
        files=[]
        dir_content = os.listdir(d)
        dir_content.sort()
        for myfile in dir_content:
            if myfile.endswith('.xml'):
                files.append(myfile)
        return files    
           
