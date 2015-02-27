'''
@organization: Lancaster University & University of Leeds
@version: 1.0
Created on 11/12/2014

@author: Victor Padilla
@contact: v.padilla@lancaster.ac.uk

GDI interface application with wxpython
The application can be run through command line (without windows interface) using 
MainMultiOMR library
'''
import wx
import webbrowser
from Functions import AddingXMLSingleMeasures
from Automatism import BatchOMR 
from MainMultiOMR import MainMultiOMR

import modulefinder

class MainWindow(wx.Frame):
    '''
    Configuration of the main interface. 
    The application could be used without this interface, just with the classes of MainMultiOMR
    '''
    
    def __init__(self, parent, title):
        ''' 
        init function
        
        '''
        self.runMainMenu(parent,title)
        mf=MainMultiOMR()
        mf._loadNWunsch()
        

    def runMainMenu(self,parent,title):
        ''' 
        Configure the main menu for the application
        
        '''
        wx.Frame.__init__(self, parent, title=title, size=(400,400))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() 

        preprocessmenu=wx.Menu()
        automatmenu=wx.Menu()
        processmenu= wx.Menu()
        resultmenu=wx.Menu()
        utilsmenu=wx.Menu()
        menu=wx.Menu()

        menuOssias=preprocessmenu.Append(wx.ID_ANY, "& Remove Ossias"," Remove Ossias")
       
        menuPSAuto=automatmenu.Append(wx.ID_ANY, "&PS"," PS")
        menuSSAuto=automatmenu.Append(wx.ID_ANY, "&SS"," SS")
        menuCPAuto=automatmenu.Append(wx.ID_ANY, "&CP"," CP")
        menuSEAuto=automatmenu.Append(wx.ID_ANY, "&SE"," SE")
        automatmenu.AppendSeparator()
        menuAllAuto=automatmenu.Append(wx.ID_ANY, "&All"," All")
        automatmenu.AppendSeparator()
        menuCleanXML=automatmenu.Append(wx.ID_ANY, "&Clean XML"," Clean XML")
        automatmenu.AppendSeparator()
        menuSetupApp=automatmenu.Append(wx.ID_ANY, "&Setup Application"," Setup Application")
                
        menuOpenOneMovement = processmenu.Append(wx.ID_OPEN, "&Process one Movement"," Process one Movement")
        menuOpenLoopBigData = processmenu.Append(wx.ID_ANY, "&Process Big Data"," Process big Data")
        menuOpenLoopBigDataAdapt = processmenu.Append(wx.ID_ANY, "&Process Big Data Adapting OMRs"," Process big Data Adapting OMRs")
        processmenu.AppendSeparator()
        menuOpenCompleteProcess = processmenu.Append(wx.ID_ANY, "&Complete process"," Complete Process")

        menuOpenOneMovementGround=resultmenu.Append(wx.ID_ANY, "&Result one Movement"," Result one Movement")
        menuOpenLoopBigDataGround = resultmenu.Append(wx.ID_ANY, "&Result Big Data"," Result Big Data")    
        processmenu.AppendSeparator()   
        menuFinalXLS = resultmenu.Append(wx.ID_ANY, "&Write final xls"," Write final xls") 
        
        
        menuWrongMeasures = utilsmenu.Append(wx.ID_ANY, "&View Wrong Measures"," Wrong measures")
        utilsmenu.AppendSeparator()
        menuJoinXMLs = utilsmenu.Append(wx.ID_ANY, "&Join XML"," Join XML")
        utilsmenu.AppendSeparator()
        menuViewM21 = utilsmenu.Append(wx.ID_ANY, "&View Through Music21"," View Music21")
        utilsmenu.AppendSeparator()
        menuConvertKrnToMusicXML = utilsmenu.Append(wx.ID_ANY, "&Krn to MusicXML"," Krn to MusicXML")
        menuConvertMidiToMusicXML = utilsmenu.Append(wx.ID_ANY, "&Midi to MusicXML"," Midi to MusicXML")
        menuConvertVoicesToChord = utilsmenu.Append(wx.ID_ANY, "&Voices to Chord"," Voices to Chord")
        menuConvertBeamsToTriplets = utilsmenu.Append(wx.ID_ANY, "&Beams to Triplets"," Beams to Triplets")
        menuRemovesEmptyVoices = utilsmenu.Append(wx.ID_ANY, "&Removes empty voices"," Removes empty voices")
        menuRemovesGaps = utilsmenu.Append(wx.ID_ANY, "&Removes Gaps"," Removes Gaps")
        utilsmenu.AppendSeparator()
        menuAdaptOMRs = utilsmenu.Append(wx.ID_ANY, "&Adapt OMRs"," Adapt OMRs")
        
        menuAbout = menu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menu.AppendSeparator()
        menuDocumentation = menu.Append(wx.ID_ANY, "& Technical Documentation"," Technical Documentation")
        menuUserManual = menu.Append(wx.ID_ANY, "& User Manual"," User Manual")
        menu.AppendSeparator()
        menuExit = menu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        menuBar = wx.MenuBar()
        menuBar.Append(preprocessmenu,"&Preprocessing") 
        menuBar.Append(automatmenu,"&Automatism") 
        menuBar.Append(processmenu,"&Process") 
        menuBar.Append(resultmenu,"&Results") 
        menuBar.Append(utilsmenu,"&Utils") 
        menuBar.Append(menu,"&Help") 
        
        self.SetMenuBar(menuBar)  
        
        self.Bind(wx.EVT_MENU, self.OnRemoveOssias, menuOssias)
        
        self.Bind(wx.EVT_MENU, self.OnViewPSAuto, menuPSAuto)
        self.Bind(wx.EVT_MENU, self.OnViewSSAuto, menuSSAuto)
        self.Bind(wx.EVT_MENU, self.OnViewCPAuto, menuCPAuto)
        self.Bind(wx.EVT_MENU, self.OnViewSEAuto, menuSEAuto)
        self.Bind(wx.EVT_MENU, self.OnViewAllAuto, menuAllAuto)
        self.Bind(wx.EVT_MENU, self.OnViewCleanXML, menuCleanXML)
        self.Bind(wx.EVT_MENU, self.OnViewSetupApp, menuSetupApp)
        
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnDocumentation, menuDocumentation)
        self.Bind(wx.EVT_MENU, self.OnUserManual, menuUserManual)
        self.Bind(wx.EVT_MENU, self.OnOpenOneMovement, menuOpenOneMovement)
        self.Bind(wx.EVT_MENU, self.OnOpenLoopBigData, menuOpenLoopBigData)
        self.Bind(wx.EVT_MENU, self.OnOpenLoopBigDataAdapt, menuOpenLoopBigDataAdapt)
        self.Bind(wx.EVT_MENU, self.OnOpenCompleteProcess, menuOpenCompleteProcess)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        self.Bind(wx.EVT_MENU, self.OnViewWrongMeasures, menuWrongMeasures)
        self.Bind(wx.EVT_MENU, self.OnViewJoinXMLs, menuJoinXMLs)
        self.Bind(wx.EVT_MENU, self.OnViewM21, menuViewM21)
        self.Bind(wx.EVT_MENU, self.OnViewConvertKrnToMusicXML, menuConvertKrnToMusicXML)
        self.Bind(wx.EVT_MENU, self.OnViewConvertMidiToMusicXML, menuConvertMidiToMusicXML)
        self.Bind(wx.EVT_MENU, self.OnViewConvertVoicesToChord, menuConvertVoicesToChord)
        self.Bind(wx.EVT_MENU, self.OnViewConvertBeamsToTriplets, menuConvertBeamsToTriplets)
        self.Bind(wx.EVT_MENU, self.OnViewRemovesEmptyVoices, menuRemovesEmptyVoices)
        self.Bind(wx.EVT_MENU, self.OnViewRemovesGaps, menuRemovesGaps)
        self.Bind(wx.EVT_MENU, self.OnViewAdaptOMRs, menuAdaptOMRs)
        

        
        self.Bind(wx.EVT_MENU, self.OnOpenOneMovementGround, menuOpenOneMovementGround)
        self.Bind(wx.EVT_MENU, self.OnOpenLoopBigDataGround, menuOpenLoopBigDataGround)
        self.Bind(wx.EVT_MENU, self.OnOpenFinalXLS, menuFinalXLS)
        
        self.Show(True)
        
   
    def OnRemoveOssias(self,e):
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mmo=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            dirGeneral = dlg.GetPath()
            mmo.processOssia(dirGeneral)   
        dlg.Destroy()
        
    
    
    def OnViewPSAuto(self,e):
        '''
        ################ AUTOMATISM MENU ################## 
        Search all the images folder and convert .tif images to .XML 
        using PhotoScore (SIKULI)
        '''
        batchOMR=BatchOMR()
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            batchOMR.processAllTiffFiles(dirname,"PS")
        print "END"
        dlg.Destroy()
        
    def OnViewSSAuto(self,e):
        '''
        ################ AUTOMATISM MENU ################## 
        Search all the images folder and convert .tif images to .XML 
        using SmartScore (SIKULI)
        '''
        batchOMR=BatchOMR()
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            batchOMR.processAllTiffFiles(dirname,"SS")
        print "END"
        dlg.Destroy()
        
    def OnViewCPAuto(self,e):
        '''
        ################ AUTOMATISM MENU ################## 
        Search all the images folder and convert .tif images to .XML 
        using Capella (SIKULI)
        '''
        batchOMR=BatchOMR()
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            batchOMR.processAllTiffFiles(dirname,"CP")
        print "END"
        dlg.Destroy()
        
    def OnViewSEAuto(self,e):
        '''
        ################ AUTOMATISM MENU ################## 
        Search all the images folder and convert .tif images to .XML 
        using SharpEye (SIKULI)
        '''
        batchOMR=BatchOMR()
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            batchOMR.processAllTiffFiles(dirname,"SE")
        print "END"
        dlg.Destroy()
        
    def OnViewAllAuto(self,e):
        '''
        ################ AUTOMATISM MENU ################## 
        Search all the images folder and convert .tif images to .XML 
        using ALL the predefined OMR (SIKULI)
        '''
        batchOMR=BatchOMR()
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            batchOMR.processAllTiffFiles(dirname,"ALL")
        print "END"
        dlg.Destroy()
        
    def OnViewCleanXML(self,e):
        '''
        ################ AUTOMATISM MENU ################## 
        Utility for deleting all the files produced by the different OMR
        (.XML files and .mro in case of SharpEye) 
        '''
        batchOMR=BatchOMR()
        if wx.MessageBox("All XML Files will be deleted. Do you wish to continue?", "Please confirm",
                         wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            batchOMR.cleanXMLFiles(dirname)
        print "END"
        dlg.Destroy()
        
    def OnViewSetupApp(self,e):
        '''
        ################ AUTOMATISM MENU ################## 
        Utility for setup the 'Process' folder once the OMR files are finished
        Two steps:
        1.- Copy the XML files
        2.- Take the .krn file and convert to ground.xml in the appropriate folder
        '''
        batchOMR=BatchOMR()
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            print "-------COPY XML FILES----------"
            batchOMR.setupApp(dirname)
            print "-------CONVERT GROUND----------"
            batchOMR.setGround(dirname)
            ######## preparing files
            
        print "END"
        dlg.Destroy()
        
        
       
    def OnOpenOneMovement(self,e):
        '''
        ######################### PROCESS MENU ###########################  
        Processing just one movement
        '''
        
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            dirGeneral = dlg.GetPath()
            print "----START----:",dirGeneral
            mf.processMovement(dirGeneral)

        dlg.Destroy()
        
    def OnOpenLoopBigData(self,e):
        '''
        ######################### PROCESS MENU ###########################  
        BigData Process menu option
        The program is waiting for files to process
        This option can be executed in a different machine reading a common folder 
        '''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            rootDir = dlg.GetPath()
            mf.runLoopBigData(rootDir,adaptOMRs=False)
        dlg.Destroy()
    
    def OnOpenLoopBigDataAdapt(self,e):
        '''
        ######################### PROCESS MENU ###########################  
        BigData Process menu option
        The program is waiting for files to process
        This option can be executed in a different machine reading a common folder 
        '''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            rootDir = dlg.GetPath()
            mf.runLoopBigData(rootDir,adaptOMRs=True)
        dlg.Destroy()
        
        
    def OnOpenCompleteProcess(self,e):
        '''
        ######################### PROCESS MENU ###########################  
        Run the complete process:
            1- Convert all .tif files to .XML (SIKULI)
            2- Processing all the files
            3- Get all the results
        This option is thought in mind for running in a single machine
        '''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            dirGeneral = dlg.GetPath()
            print "----START----:",dirGeneral
            mf.runCompleteProcess(dirGeneral)
            
        dlg.Destroy()
        
        
    def OnOpenOneMovementGround(self,e):
        '''
        ########################## RESULT MENU ################################# 
        Check each .xml file against 'ground.xml' and evaluate the differences.
        The final result is written in the appropriated file
        Example:
        k428\Process\m1\parts\resultGeneral.xlsx
        '''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            dirGeneral = dlg.GetPath()
            mf.processMovementGround(dirGeneral)   
        dlg.Destroy()
        
    def OnOpenLoopBigDataGround(self,e):
        '''
        ########################## RESULT MENU ################################# 
        BigData Result menu option
        The program is waiting for files to get the result
        This option can be executed in a different machine reading a common folder 
        '''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            rootDir = dlg.GetPath()
            mf.runLoopBigDataGround(rootDir)
            
        dlg.Destroy()   
        
    def OnOpenFinalXLS(self,e):
        '''
        ########################## RESULT MENU ################################# 
        BigData Result menu option
        The program is waiting for files to get the result
        This option can be executed in a different machine reading a common folder 
        '''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            rootDir = dlg.GetPath()
            mf.runFinalXLS(rootDir)
            
        dlg.Destroy()       
     
    def OnViewWrongMeasures(self,e):
        '''
        ########################## UTILS MENU #####################################  
        Check the different errors in measures using 
        different procedures
        '''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            print "---------S1------------"
            mf.runViewWrongMeasures(dirname)

        dlg.Destroy()
   
        
    def OnViewJoinXMLs(self,e):
        '''
        ########################## UTILS MENU #####################################  
        Add different measures
        (under development)
        '''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            addingXML=AddingXMLSingleMeasures()
            addingXML.runViewJoinXML(dirname)

        dlg.Destroy()
        

        
    def OnViewM21(self,e):
        '''
        ########################## UTILS MENU #####################################  
        Show an .xml file processed by music21
        to check the differences and possible errors
        '''
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            mf.runViewM21(dirname)
        dlg.Destroy()
        
        
   
    
    def OnViewConvertKrnToMusicXML(self,e):
        '''
        ########################## UTILS MENU #####################################  
        convert one .krn file to .xml
        '''
        dlg = wx.FileDialog(self, "Open .krn file", "", "",
                                       "KRN files (*.krn)|*.krn", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            mf.runConvertKrnToMusicXML(filename)
        print "END"
        dlg.Destroy()
        
    def OnViewConvertMidiToMusicXML(self,e):
        '''
        ########################## UTILS MENU #####################################  
        convert one .midi file to .xml
        '''
        dlg = wx.FileDialog(self, "Open .mid file", "", "",
                                       "MIDI files (*.mid)|*.mid", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            mf.runConvertMidiToMusicXML(filename)
        print "END"
        dlg.Destroy()
        
    def OnViewConvertVoicesToChord(self,e):
        '''
        ########################## UTILS MENU #####################################  
        '''
        dlg = wx.FileDialog(self, "Open .mid file", "", "",
                                       "xml files (*.xml)|*.xml", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            mf.runConvertVoicesToChord(filename)
        print "END"
        dlg.Destroy()
    
    def OnViewConvertBeamsToTriplets(self,e):
        '''
        ########################## UTILS MENU #####################################  
        '''
        dlg = wx.FileDialog(self, "Open .mid file", "", "",
                                       "xml files (*.xml)|*.xml", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            mf.runConvertBeamsToTriplets(filename)
        print "END"
        dlg.Destroy()
    
    def OnViewRemovesEmptyVoices(self,e):
        '''
        ########################## UTILS MENU #####################################  
        '''
        dlg = wx.FileDialog(self, "Open .mid file", "", "",
                                       "xml files (*.xml)|*.xml", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            mf.runRemovesEmptyVoices(filename)
        print "END"
        dlg.Destroy()
    def OnViewRemovesGaps(self,e):
        '''
        ########################## UTILS MENU #####################################  
        '''
        dlg = wx.FileDialog(self, "Open .mid file", "", "",
                                       "xml files (*.xml)|*.xml", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            mf.runRemovesGaps(filename)
        print "END"
        dlg.Destroy()
    
    def OnViewAdaptOMRs(self,e):
        '''
        ########################## UTILS MENU #####################################  
        '''
        
        dlg = wx.DirDialog(None, "Choose a directory","",wx.DD_DEFAULT_STYLE)
        mf=MainMultiOMR()
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
            mf.runAdaptOMRs(dirname)
        dlg.Destroy()
        
    def OnAbout(self,e):
        '''
        ##########################  MENU #####################################
        about menu option
        '''
        dlg = wx.MessageDialog( self, "Big Data Project", "Big Data Project", wx.OK)
        dlg.ShowModal() 
        dlg.Destroy()
        
    def OnDocumentation(self,e):
        '''
        ##########################  MENU #####################################
        open documentation web
        '''
        webbrowser.open_new("..\\Documentation\\html\\index.html")
    def OnUserManual(self,e):
        '''
        ##########################  MENU #####################################
        open user manual
        '''    
        webbrowser.open_new("..\\Documentation\\Manual.pdf")
    def OnExit(self,e):
        '''
        ##########################  MENU #####################################
        exit menu option
        '''
        self.Close(True)  
        
   
        

app = wx.App(False)
frame = MainWindow(None, "Big Data Process")
app.MainLoop()