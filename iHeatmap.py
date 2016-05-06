import os
import wx
import sys
# import wx.lib.filebrowsebutton as filebrowse

import numpy
import statsmodels.stats.multitest as multitest
import pandas as pd

# sys.path.append("C:/Users/sling/iCloudDrive/iHeatmap")  is not needed to build the package
from scipy import stats
from iFun import *
from iHeatmapTable import *
from iHeatmapDialog import *
from iHeatmapNotebook import Notebook


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title= "(iHeatmap) interactive heatmap builder" ,size=(1200, 600))
        
        ico = wx.Icon('egypt200.png', wx.BITMAP_TYPE_ANY)
        self.SetIcon(ico)
        
        # set menuFile and menuBar
        menuFile = wx.Menu()
        menuFile.Append(1, "&Input files")
        menuFile.Append(2, "&Save")
        menuFile.Append(3, "&Save As")
        menuFile.AppendSeparator()
        menuFile.Append(4, "E&xit")
        
        menuAbout = wx.Menu()
        menuAbout.Append(10, "&About...")
        
        menuHeatmap = wx.Menu()
        menuHeatmap.Append(21, "&BuildHeatmap")
        
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        menuBar.Append(menuHeatmap, "&Heatmap")
        menuBar.Append(menuAbout, "&About")

        
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnInputFile, id=1)
        self.Bind(wx.EVT_MENU, self.OnSave, id=2)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=3)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=4)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=10)
        self.Bind(wx.EVT_MENU, self.OnHeatmap, id=21)
                
        # make sizers of windows
        self.sizerMainFrame = wx.BoxSizer(wx.VERTICAL)

        # make frame with notebook 
        self.notebook = Notebook( self, [])
        self.sizerMainFrame.Add(self.notebook, 1, wx.EXPAND)
        
        # update sizers
        self.SetSizer(self.sizerMainFrame)
        self.Layout()

    def OnInputFile(self, event):
        # get paths
        inputDlg = InputDialog()
        
        # read files
        # self.data store a list of data
        self.data = [self.ReadingData(inputDlg.GetPath()[n]) for n in range(inputDlg.GetInputFilesQuantityShowed())]

        # update notebook
        self.notebook.UpdateNotebook(self.data, [])
    
    # read in different type of data using pandas or different separator based on postfix
    # generally three types: \t, ",", space
    # now csv
    # data is a 2D array
    def ReadingData(self, path):
#        data = []
        print "path: " + path
        if path != u'':
            f = open(path)
            filename, file_extension = os.path.splitext(path)        
            data = []    
            if(file_extension == ".csv"):
                sep = ","
            else:
                sep= None  #  separated by arbitrary strings of whitespace characters (space, tab, newline, return, formfeed)    
            if (file_extension ==".tsv"):
                sep= "\t"            
            # data = pd.read_csv(path, header=0)
            # print data.dtypes
            for line in f:
                # split the file by space
                data.append(line.split(sep))

        return data

    def OnSave(self, event):
        pass

    def OnSaveAs(self, event):
        pass

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        wx.MessageBox("Simple GUI for heatmap\nAuthor: iBAS", "About...", wx.OK | wx.ICON_INFORMATION, self)

    def OnHeatmap(self,event):
        number = self.notebook.GetListTabId().index(self.notebook.GetCurrentTabId())
        heatmapDlg = DialogHeatmap(title=u"Input for heatmap")
        pars = heatmapDlg.GetValue()
        
        print(pars)
        
        matStart = pars[0]-1                
        import rpy2.robjects as robjects
        from rpy2.robjects.packages import importr
        base = importr("base")
        heatmap = importr("heatmap3")
        grdevices = importr("grDevices")
        data = self.data[number]
        numData = numpy.array(data)[1:,2: ].astype(float)
        numData = numpy.transpose(numData)
        items = numpy.array(data)[0,matStart: ].astype(str)  
              

        from rpy2.robjects import numpy2ri        
        numpy2ri.activate()   # transfer the numpy array to matrix in R 
        
        nr,nc = numData.shape
        xvec = robjects.FloatVector(numData.transpose().reshape(numData.size))
        numDataR =  robjects.r.matrix(xvec, nrow=nr, ncol=nc)                       
        numDataR.rownames = robjects.StrVector(items) # different from R format
        
        annoCols = [ x-1 for x in pars[1]] 
        
        #annoColDicList =[]
        for n, annoCol in enumerate(annoCols):            
            anno = numpy.array(data)[1:, int(annoCol)]
            annoColDic = getCategoryColorDic (list(set(anno)), colsDic)
            cols = getMemberColor(anno, annoColDic)
            if (n==0):
                annoColor1 = robjects.StrVector(cols)  
                annoColDicList =  [annoColDic]    
                ColSideColors = base.cbind(annoColor1) # should use matrix in R instead of dataframe
                print     annoColDicList               
            if (n==1):
                annoColor2 = robjects.StrVector(cols)
                ColSideColors = base.cbind(annoColor1 , annoColor2)
                annoColDicList = annoColDicList + [annoColDic]
                print annoColDicList
            if (n>=2):
                annoColorX = robjects.StrVector(cols)              
                ColSideColors = base.cbind(ColSideColors , annoColorX)
                annoColDicList = [annoColDicList, annoColDic]
        
        print base.dim(ColSideColors)
        annoName = robjects.StrVector(numpy.array(data)[0, annoCols])
        ColSideColors.colnames = annoName
        
        outputDlg = OutputDialog()
        outPath = outputDlg.GetPath()
        print outPath
        fileName = outPath + "/heatmap.pdf"         
        grdevices.pdf(file = fileName )
        heatmap.heatmap3(numDataR,ColSideColors=ColSideColors,showRowDendro=False)
        grdevices.dev_off()
        
        heatmap.heatmap3(numDataR,ColSideColors=ColSideColors,showRowDendro=False)
        
        from rpy2.robjects.functions import SignatureTranslatedFunction
        # explicitly translate the R argument to legal python name 
        heatmap.showLegend = SignatureTranslatedFunction(heatmap.showLegend,
                                           init_prm_translate = {'pt_bg': 'pt.bg'})
        # Plot legends in another window
        for i in range(len(annoColDicList)):
            grdevices.dev_new()
            anno = robjects.StrVector(annoColDicList[i].keys())
            col =  robjects.StrVector(annoColDicList[i].values())
            heatmap.showLegend(legend= anno,col=col,cex=1.5, title="Annotation Legend: "+annoName[i], pch=22, lwd = robjects.NA_Integer, pt_bg=col)
            fileName = outPath +"/heatmapLegend" + str(i) + ".pdf"
            grdevices.pdf(file = fileName )
            heatmap.showLegend(legend= anno,col=col,cex=1.5, title="Annotation Legend: "+annoName[i], pch=22, lwd = robjects.NA_Integer, pt_bg=col)
            grdevices.dev_off()


if __name__ == '__main__':
    app = wx.App()

    frame = MainFrame()
    frame.Show()

    app.MainLoop()
