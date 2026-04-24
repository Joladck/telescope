from PyQt6.QtWidgets import QApplication,QWidget,QDateEdit, QPushButton, QMainWindow,QTableWidget,QTableWidgetItem,QDockWidget,QComboBox, QLineEdit,QVBoxLayout,QHBoxLayout,QFormLayout
from PyQt6.QtCore import Qt
import pandas as pd
import kpler_handler as kph

"""
test
"""
class MWindow(QMainWindow):
    def  __init__(self,wt):
        '''
        constructor function
    
        wt: window title
        '''
        super().__init__()
        self.setWindowTitle(wt)

        self.table=sm_table(self)
        self.setCentralWidget(self.table)

        self.searcher=search_bar(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.searcher)

        self.searcher.submit.clicked.connect(self.data_submitted)

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

    def data_submitted(self):
        output_dict={
            'dataset': self.searcher.data_set.currentText(),
            'countries': self.searcher.countries.text(),
            'start_date':self.searcher.start_date.text(),
            'end_date':self.searcher.end_date.text(),
            'units':self.searcher.units.currentText(),
            'period':self.searcher.period.currentText(),
            'split':self.searcher.data_count.currentText(),
            'product':self.searcher.product.text()
        }
        data=kph.flow_handler(output_dict,kph.conf)
        self.table.load_data(data)


"""
I would be interested in turning this into the MVC class eventually
"""
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

    def load_data(self,data):
        self.frame_data=data.copy()
        dcols=data.columns
        data_dict=data.to_dict('records')

        self.add_cols(dcols)
        self.add_rows(data_dict)


class search_bar(QDockWidget):
    def __init__(self, parent):
        #Dock init
        super().__init__(parent)
        self.setWindowTitle('Search')
        
        #search form layout init
        self.search_form=QWidget()
        layout=QFormLayout(self.search_form)
        
        ##search fields for kpler
        self.data_set=QComboBox(self.search_form)
        self.data_set.addItems(['Exports','Imports',''])
        self.countries=QLineEdit('Enter items separated by a comma',self.search_form,)
        self.start_date=QDateEdit(self.search_form)
        self.end_date=QDateEdit(self.search_form)
        self.units=QComboBox(self.search_form)
        self.units.addItems(['kbd','bbl','kb','mmbbl','mt','kt','t','cm'])
        self.period=QComboBox(self.search_form)
        self.period.addItems(['annually','monthly','weekly','eia-weekly','daily'])
        self.data_count=QComboBox(self.search_form)
        self.data_count.addItems(['origin countries','destination countries','buyers','charterers','crude quality', 'destination continents',
        'destination installations','destination padds','destination subcontinents','destination trading regions', 'grades', 'long haul vessel type',
        'long haul vessel type cpp','long haul vessel type oil', 'origin continents', 'origin installations', 'origin padds',
        'origin subcontinent', 'origin trading region', 'products', 'routes', 'sellers','source', 'total','trade status','vessel type', 'vessel type cpp',''
        'vessel type oil' ])
        self.product=QLineEdit('Enter items separated by a comma',self.search_form)
        self.submit=QPushButton('Submit',self.search_form)
        
        
        #self.submit.clicked.connect(self.data_submitted)        
    
        ##adding to layout
        layout.addRow('Dataset', self.data_set)
        layout.addRow('Countries',self.countries)
        layout.addRow('Start Date',self.start_date)
        layout.addRow('End Date',self.end_date)
        layout.addRow('Unit',self.units)
        layout.addRow('Period',self.period)
        layout.addRow('Data Type',self.data_count)
        layout.addRow('Product',self.product)
        layout.addRow(self.submit)
        #Dock widget setup
        self.search_form.setLayout(layout)
        self.setWidget(self.search_form)

    """
    Scheduled for deletion

    def data_submitted(self):
        output_dict={
            'dataset': self.data_set.currentText(),
            'countries': self.countries.text(),
            'start_date':self.start_date.text(),
            'end_date':self.end_date.text(),
            'units':self.units.currentText(),
            'period':self.period.currentText(),
            'split':self.data_count.currentText(),
            'product':self.product.text()
        }

        return output_dict
    """
        


if __name__=='__main__':
    telescope=QApplication([])

    #data=pd.read_csv('Export.csv')
 #   data=data[['Panama','Mexico']]
    #dcols=data.columns
    #data=data.to_dict('records')
    window=MWindow('Telescope')
    #window.table.add_cols(dcols)
    #window.table.add_rows(data)

    window.show()
    #QTableWidget().setColumnWidth()


    telescope.exec()   