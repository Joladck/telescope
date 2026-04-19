from PyQt6.QtWidgets import QApplication,QWidget,QLabel, QMainWindow,QTableWidget,QTableWidgetItem,QDockWidget,QComboBox, QVBoxLayout
from PyQt6.QtCore import Qt
import pandas as pd

class MWindow(QMainWindow):
    def  __init__(self,wt):
        '''
        constructor function
    
        wt: window title
        '''
        super().__init__()
        self.setWindowTitle(wt)

    def add_widget(self,name,**kwargs):
        '''
        SHOULD BE REMOVED
        this function is meant to help add widgets dynamically, it's temporary, and will be removed once the full scope
        of this class is realized
        name is the variable name
        **kwargs this is a bit of an odd one for me but this is supposed to take in a dictionary where keys are functions
                 and values are arguments
        '''
        nwidg=list(kwargs.items())
        k,val=nwidg[0]
        command= f"self.{name}={k}({val})"
        exec(command)

    def center_widget(self,name):
        '''SHOULD BE REMOVED
        this function is meant to help add widgets dynamically, it's temporary, and will be removed once the full scope
        of this class is realized'''
        command=f'self.setCentralWidget(self.{name})'
        exec(command)


class sm_table(QTableWidget):
    """
    sm_table (smart table) is an implementation of the table class that can dynamically fill itself
    """
    def __init__(self,parent):
        super().__init__(parent)

    def add_cols(self,header_list):
        """
        add_cols takes care of all the set up to properly set up columns for data

        header_list: list of strings with column names
        """
        #get col names and set count
        headcount=len(header_list)
        self.setColumnCount(headcount)

        #set and save col names
        self.setHorizontalHeaderLabels(header_list)
        self.col_heads=header_list

        #set a predetermined width for columns
        for i in range(headcount):
            self.setColumnWidth(i,150)


    def add_rows(self,dict):
        """
        add_rows takes care of the tasks necessary to add rows
        
        dict: dict is a list of dictionaries, specifically we expect a dictionary as per the output of pandas to_dict('records')
        """
        #get count for rows for the loop
        rowc=len(dict)
        self.setRowCount(rowc)
        for i in range(rowc):
            cell=0
            for z in self.col_heads:
                self.setItem(i,cell,QTableWidgetItem(str(dict[i][z])))
                cell+=1


class search_bar(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Search')
   
        self.endpoint=QComboBox(self)
        self.endpoint.addItems(['Exports','Imports',''])

        datalab=QLabel('Dataset', self)
        self.setWidget(datalab)
        self.setWidget(self.endpoint)
        


if __name__=='__main__':
    telescope=QApplication([])

    data=pd.read_csv('Export.csv')
    data=data[['Panama','Mexico']]
    dcols=data.columns
    data=data.to_dict('records')
    print(data)
    window=MWindow('Telescope')
    newWidg={QTableWidget: window }
    window.add_widget('search',search_bar='self')
    window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,window.search)
    window.add_widget('report_tab',sm_table='self')
    window.center_widget('report_tab')
    window.report_tab.add_cols(dcols)
    window.report_tab.add_rows(data)

    window.show()
    #QTableWidget().setColumnWidth()


    telescope.exec()   