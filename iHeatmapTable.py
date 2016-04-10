import wx.grid  # there is no wx.grid.PyGridTableBase module


class TableBase(wx.grid.PyGridTableBase):
    def __init__(self, data):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data # numpy.array(data)[: , :]  # here it can be mixed with "letter" and number

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data[0])

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        pass

class Table(wx.grid.Grid):
    def __init__(self, parent, data):
        wx.grid.Grid.__init__(self, parent, -1)  # the parent here is notebook
        # self.CreateGrid(20,8)        
        if data != []:
            table = TableBase(data)       
            self.SetTable(table, True)

    def UpdateTable(self, data):
        if data != []:
            table = TableBase(data)
            self.SetTable(table, True)
            self.Refresh()
            self.Update()