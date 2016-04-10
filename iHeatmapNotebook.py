import wx
from iHeatmapTable import *

class Notebook(wx.Notebook):
    """
    Notebook class
    """
    def __init__(self, parent, data):  # data type is pandas dataframe
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)

    def OnPageChanged(self, event):
        self.currentPageId = event.EventObject.GetChildren()[event.Selection].Id
        print "the updated tab Id of notebook is"
        print self.currentPageId
        event.Skip()

    def GetListTabId(self):
        return self.listTabId

    def GetCurrentTabId(self):
        return self.currentPageId

    def UpdateNotebook(self, data, number):
        if data != []:
            if number == []:
                # generate the tab based on the number of data
                # self.listTabPanel = [Table(self, [list(data[n])]+ data[n].values.tolist()) for n in range(len(data))]  # when input with pandas dataframe
                self.listTabPanel = [Table(self, data[n]) for n in range(len(data))]
                self.listTabId = [self.listTabPanel[n].Id for n in range(len(data))]
                # print self.listTabPanel[0].GetColLabelValue(2)
                # print self.listTabPanel[0].Table.colLabels[2]   try to show whether the colname is set as we wanted
                # set the page Id to the first tab of notebook             
                self.currentPageId = self.listTabPanel[0].Id
                print "the Ids of the notebook are"
                print self.listTabId

                self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged) # This bind the event to function, Changed for the tab after change, Changing for the tab before the change

                [self.AddPage(self.listTabPanel[n], "data" + str(n+1)) for n in range(len(data))]
                self.listTabPanel[0].SetColLabelValue(2, "first")   
                # self.listTabPanel[0].Refresh()
                self.listTabPanel[0].Update() 
                # print self.listTabPanel[0].GetColLabelValue(2)                

            if number != []:
                self.listTabPanel[number].UpdateTable(data)