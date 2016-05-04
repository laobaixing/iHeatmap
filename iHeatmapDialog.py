import wx
import os
import wx.lib.filebrowsebutton as filebrowse
#from _cffi_backend import string

class InputDialog(wx.Dialog):
    
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, title="Import files", size=(450, 250))

        
        self.dataFilesQuantityMax = 4  # the max quantity of "Add File" buttons, should be put in the dialogue class
        self.inputFilesQuantityShowed = 1
        self.startDirectory = os.getcwd()

        # make sizers
        sizerMainFrame = wx.BoxSizer(wx.VERTICAL)
        self.listFlBrwssizerBtns = wx.BoxSizer(wx.VERTICAL)
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)

        #  make buttons
        self.listFlBrwsBtn = [filebrowse.FileBrowseButton(self, id=wx.NewId(), labelText="data" + str(flBrwsBtn+1), initialValue="", size=(400, -1), buttonText="Browse...", startDirectory=self.startDirectory) for flBrwsBtn in range(self.dataFilesQuantityMax)]
        btnAddFile = wx.Button(self, wx.NewId(), label="&Add file")
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")

        self.Bind(wx.EVT_BUTTON, self.OnAddFile, btnAddFile)

        #  set sizers of list file browse buttons
        self.listFlBrwssizerBtns.Add(wx.Size(1, 20))

        for flBrwsBtn in range(self.dataFilesQuantityMax):
            self.listFlBrwssizerBtns.Add(self.listFlBrwsBtn[flBrwsBtn], flag=wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, border=5)
            if flBrwsBtn > 0:
                self.listFlBrwsBtn[flBrwsBtn].Hide()

        #  set sizers of Open and Cancel buttons
        sizerBtns.Add(wx.Size(1, 20))
        sizerBtns.Add(btnAddFile, flag=wx.ALL, border=5)
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)

        #  set sizerMainFrame
        sizerMainFrame.Add(self.listFlBrwssizerBtns)
        sizerMainFrame.Add(sizerBtns)

        self.SetSizer(sizerMainFrame)
        self.Fit()
        self.Layout()

        if self.ShowModal() == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.status = False
            self.Destroy()

    def OnAddFile(self, event):
        # inputFilesQuantityShowed start from 1
        currentPath = self.listFlBrwsBtn[self.inputFilesQuantityShowed-1].GetValue()
        # print(currentPath)
        self.listFlBrwsBtn[self.inputFilesQuantityShowed].startDirectory = os.path.dirname(currentPath)
        self.inputFilesQuantityShowed += 1

        for flBrwsBtn in range(self.inputFilesQuantityShowed):
            self.listFlBrwsBtn[flBrwsBtn].Show()

        self.Fit()
        self.Layout()

    def GetPath(self):
        if self.status:
            return [self.listFlBrwsBtn[FlBrwsBtn].GetValue() for FlBrwsBtn in range(self.dataFilesQuantityMax)]
        else:
            return []

    def GetInputFilesQuantityShowed(self):
        if self.status:
            return self.inputFilesQuantityShowed
        else:
            return 1



#######################################################################################
## Dialog class for heatmap
#######################################################################################

class DialogHeatmap ( wx.Dialog ):
    
    def __init__( self, title ):
        # wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = u"Input for Scatter Plot", pos = wx.DefaultPosition, size = wx.Size(606,375 ), style = wx.DEFAULT_DIALOG_STYLE )
        wx.Dialog.__init__(self, None, -1, title= title, size=(450, 250))
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Please input for heatmap", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        gSizer3 = wx.GridSizer( 0, 2, 0, 0 )  # list control in two columns
        
#         self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"By Row or Column", wx.DefaultPosition, wx.DefaultSize, 0 )
#         self.m_staticText2.Wrap( -1 )
#         gSizer3.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
#         m_choice1Choices = [ u"Col", u"Row" ]
#         self.m_choice1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
#         self.m_choice1.SetSelection( 0 )
#         gSizer3.Add( self.m_choice1, 0, wx.ALL, 5 )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Data for heatmap start from", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        gSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )
        
        self.m_textCtrl6 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl6, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Name or number of annotation variables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        gSizer3.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        self.m_textCtrl7 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl7, 0, wx.ALL, 5 )     
        
#         self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Method", wx.DefaultPosition, wx.DefaultSize, 0 )
#         self.m_staticText5.Wrap( -1 )
#         gSizer3.Add( self.m_staticText5, 0, wx.ALL, 5 )
#         
#         m_choice2Choices = [ u"ward.D", u"Spearman" ]
#         self.m_choice2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
#         self.m_choice2.SetSelection( 0 )
#         gSizer3.Add( self.m_choice2, 0, wx.ALL, 5 )      
        
        bSizer1.Add( gSizer3, 1, wx.EXPAND, 5 )
        
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)
        bSizer1.Add(sizerBtns)#  , 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )
        
        result = self.ShowModal()   # Show the dialog and wait for the input
        if result == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.Destroy()        
        
    def _is_int_(self,s):
        try:
            int(s)
            return(True)
        except ValueError:
            return False
    
    def _str2num_(self,s):
        vals = []
        if self._is_int_(s) :
            vals = [int(s)]
        else:
            if("," in s) :
                xs = s.split(",")
                for x in xs:
                    if self._is_int_(x):
                        vals = vals+ [int(x)]
                    else:
                        if("_" in x):
                            y = x.split("-")
                            if(len(y) == 2):
                                ynum = [int(z) for z in y ]
                                vals = vals + range(ynum[0], ynum[1]+1)
                            else:
                                print("%s the format is not correct", x)
                                return(None)
                        else:
                            print("%s the format is not correct", x)
                            return(None)
            else:
                if("-" in s):
                    y = s.split("-")
                    if(len(y) == 2):
                        ynum = [int(z) for z in y ]
                        vals = range(ynum[0], ynum[1]+1)
                    else:
                        print("%s the format is not correct", x)
                        return(None)                    
                else:
                    print("the format is not correct")  
                    return(None)
        return(vals) 
     
    def GetValue(self):
        if self.status:
            # direction = str(self.m_choice1.GetStringSelection())
            val1= int(self.m_textCtrl6.GetValue())
            valstr2 = self.m_textCtrl7.GetValue()
            valnum2 = self._str2num_(valstr2)
            #  method = str(self.m_choice2.GetStringSelection())
            return (val1, valnum2)  
        else:
            return []
                    
    def __del__( self ):
        pass
    

class OutputDialog(wx.Dialog):
    
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, title="Output results", size=(450, 250))
    
        self.startDirectory = os.getcwd()

        # make sizers
        sizerMainFrame = wx.BoxSizer(wx.VERTICAL)
        self.FlBrwsBtnsSizer = wx.BoxSizer(wx.VERTICAL)
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)

        #  make buttons
        self.FlBrwsBtn = filebrowse.DirBrowseButton(self, id=wx.NewId(), labelText="Output path", size=(400, -1), buttonText="Browse...", startDirectory=self.startDirectory) 
        btnOK = wx.Button(self, wx.ID_OK, label="&OK")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        
        # self.Bind(wx.EVT_BUTTON, self.OnOK, btnOK)        

        #  set sizers of list file browse buttons
        self.FlBrwsBtnsSizer.Add(wx.Size(1, 20))

        self.FlBrwsBtnsSizer.Add(self.FlBrwsBtn, flag=wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, border=5)

        #  set sizers of OK and Cancel buttons
        sizerBtns.Add(wx.Size(1, 20))
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOK, flag=wx.ALL, border=5)

        #  set sizerMainFrame
        sizerMainFrame.Add(self.FlBrwsBtnsSizer)
        sizerMainFrame.Add(sizerBtns)

        self.SetSizer(sizerMainFrame)
        self.Fit()
        self.Layout()

        if self.ShowModal() == wx.ID_OK:
            print "OK"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.status = False
            self.Destroy()

    def GetPath(self):
        if self.status:
            return self.FlBrwsBtn.GetValue() 
        else:
            return None

 
