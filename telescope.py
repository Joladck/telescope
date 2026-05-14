from PyQt6.QtWidgets import (QAbstractItemView,QApplication,QCheckBox,QComboBox,QDateEdit,QDialog,QDockWidget,QFileDialog,QFormLayout,QGridLayout,QHBoxLayout,QLabel,QLineEdit,QListWidget,
                             QMainWindow,QMessageBox,QPushButton,QTabWidget,QTableWidget,QTableWidgetItem, QVBoxLayout,QWidget)
from PyQt6.QtGui import QAction,QBrush
from PyQt6.QtCore import Qt
import pandas as pd
import kpler_handler as kph
import utility_dicts as ud
from datetime import datetime
import json
import sys
import os


selected=QBrush(Qt.GlobalColor['green'])
deselcted=QBrush(Qt.GlobalColor['white'])

class MWindow(QMainWindow):
    def  __init__(self,wt):
        '''
        constructor function
    
        wt: window title
        '''
        super().__init__()
        #data model
        self.kph_conf=kph.gen_conf()

        #windows setup
        self.setWindowTitle(wt)

        self.conf_window=config_window(self)
        self.product_search=product_picker(self.kph_conf,self)
        

        #directory for saving any documents
        cwpath=os.getcwd()
        confpath=cwpath
        confpath+='/conf.json'
        if os.path.exists('conf.json'):
            fl=open('conf.json','r')
            path=json.load(fl)
            self.save_path=path['path']
        else:
            self.save_path=''

        #menu setup
        self.menu_bar=self.menuBar()

        file_menu= self.menu_bar.addMenu('&File')
        help_menu= self.menu_bar.addMenu('&Help')

        ##menu items
        ###file menu
        load_action=QAction('&Load Dataset',self)
        load_action.setStatusTip('Load a saved dataset, erases current one')
        load_action.setShortcut('Ctrl+l')
        load_action.triggered.connect(self.load_existing_data)
        file_menu.addAction(load_action)

        conf_action=QAction('&Configure',self)
        conf_action.setStatusTip('Alter parametters important to multiple functions')
        conf_action.setShortcut('Ctrl+c')
        conf_action.triggered.connect(self.configuration_settings_setup)
        file_menu.addAction(conf_action)

        ##help menu
        doc_action=QAction('&Manual',self)
        doc_action.setStatusTip('pulls up a set of instructions for the program')
        doc_action.setShortcut('Ctrl+h')
        doc_action.triggered.connect(self.help_window)
        help_menu.addAction(doc_action)



        
        #adding central widget, table
        self.table=sm_table(self)
        self.setCentralWidget(self.table)

        #initializign Dock
        self.searcher=search_bar(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.searcher)

        #connecting Dock slots to functions, being done here because this parent widget
        #can connect to the table widget, whereas the dock would not have access to it
        self.searcher.submit.clicked.connect(self.data_submitted)
        self.searcher.test_data_load.clicked.connect(self.load_test)
        self.conf_window.accepted.connect(self.update_save_path)
        self.searcher.product.clicked.connect(self.product_window)



    #metaprogramming function for testing purposes  only
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

    #metaprogramming function for testing purposes  only
    def center_widget(self,name):
        '''SHOULD BE REMOVED
        this function is meant to help add widgets dynamically, it's temporary, and will be removed once the full scope
        of this class is realized'''
        command=f'self.setCentralWidget(self.{name})'
        exec(command)

    #TEST FUNCTION                               
    def load_test(self):
        data=pd.read_csv('Export.csv')
        self.table.load_data(data)

    #sends info from Dock to Table through MainWindow
    def data_submitted(self):
        
        output_dict={
            'dataset': self.searcher.data_set.currentText(),
            'countries': self.searcher.countries.text(),
            'start_date':self.searcher.start_date.dateTime().toPyDateTime(),
            'end_date':self.searcher.end_date.dateTime().toPyDateTime(),
            'units':self.searcher.units.currentText(),
            'period':self.searcher.period.currentText(),
            'split':self.searcher.data_count.currentText(),
            'product':self.searcher.product.text()
        }

        #this helps generate a dynamic name for the hypothetical save file
        dataset=output_dict['dataset']
        split=output_dict['split']
        self.file_title=f'{dataset}_split_by_{split}_{datetime.now().date}'

        #kpler function call via handler
        data=kph.flow_handler(output_dict,self.kph_conf)
        self.table.load_data(data)


        
    def load_existing_data(self):
        #TODO
        pass

    def configuration_settings_setup(self):
        self.conf_window.show()

    def update_save_path(self):
        fl=open('conf.json','r')
        path=json.load(fl)
        self.save_path=path['path']    

    def product_window(self):
        self.product_search.show()

    def product_save(self):
        pass

    def help_window(self):
        #TODO
        pass

    def export_table(self):  
        # function to save data loaded
        if pd.isna(self.table.view_data()):
            self.table.frame_data.to_csv (f'{self.save_path}/{self.file_title}')

        else:
            self.table.frame_data.to_csv(f'{self.save_path}/{self.file_title}')

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

    def overwrite_data(func):
        """
        because I foresee having to clear the table often, I made this decorator to handle that task
        because this is simply a fairly standard procedure that doesn't really need much more consideration
        this is probably the most eficient way of handling it. if I ever do need something to append to the current
        table, I can simply not use it.
        """
        def inner(self,data):

            if self.rowCount() != 0 or self.columnCount()!=0:
                self.clear()

            return func(self,data)
        return inner

    @overwrite_data
    def load_data(self,data):
        """
        takes the data and extracts from it relevant components for add_columns and add_rows
        """
        self.frame_data=data.copy()
        self.view_data=pd.DataFrame()
        dcols=data.columns
        data_dict=data.to_dict('records')

        self.add_cols(dcols)
        self.add_rows(data_dict)


class search_bar(QDockWidget):
    def __init__(self, parent):
        #Dock init
        super().__init__(parent)
        self.setWindowTitle('Search')

        self.main_window=QWidget(self)
        main_layout=QVBoxLayout(self.main_window)
        

        #tab for utility purposes
        tab=QTabWidget()
        
        #search form layout init
        self.search_form=QWidget(self)
        layout_1=QFormLayout(self.search_form)
        
        ##search fields for kpler
        self.data_set=QComboBox(self.search_form)
        self.data_set.addItems(['Exports','Imports',''])

        self.countries=QLineEdit('Enter items separated by a comma',self.search_form,)

        self.start_date=QDateEdit(self.search_form)
        self.end_date=QDateEdit(self.search_form)
        self.start_date.setDisplayFormat('MM/dd/yyyy')
        self.end_date.setDisplayFormat('MM/dd/yyyy')

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

        

        self.product=QPushButton('Product')

        ##buttons
        self.submit=QPushButton('Submit',self.search_form)
        self.exportb=QPushButton('Export',self.search_form)
        self.test_data_load=QPushButton('Load Test',self.search_form)
        
        #self.submit.clicked.connect(self.data_submitted)        
    
        ##adding to layout
        layout_1.addRow('Dataset', self.data_set)
        layout_1.addRow('Countries',self.countries)
        layout_1.addRow('Start Date',self.start_date)
        layout_1.addRow('End Date',self.end_date)
        layout_1.addRow('Unit',self.units)
        layout_1.addRow('Period',self.period)
        layout_1.addRow('Data Type',self.data_count)
        layout_1.addRow('Product',self.product)
        layout_1.addRow(self.submit)
        layout_1.addRow(self.exportb)        
        layout_1.addRow(self.test_data_load)

        
        
        #second form for editing
        self.edit_form=QWidget(self)
        layout_2=QFormLayout(self.edit_form)

        ##these are fields useful for editing WIP        
        self.wip=QLabel('This Section is a Work in Progress')

        ##adding to layout
        layout_2.addRow(self.wip)

        
        #Dock widget setup
        self.search_form.setLayout(layout_1)
        self.edit_form.setLayout(layout_2)
        
        #adding tabs
        tab.addTab(self.search_form,'Import')
        tab.addTab(self.edit_form,'Edit')

        #finalizing dock components
        main_layout.addWidget(tab)
        self.main_window.setLayout(main_layout)
        self.setWidget(self.main_window)
 
class config_window(QDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.setWindowTitle('Configuration')
        self.setBaseSize(700,100)

        #widget + layout combo
        main_layout=QGridLayout()
        
        ##form wiget
        self.config_menu=QWidget()
        config_form=QFormLayout()

        #in form layout
        file_item=QWidget()
        file_item_layout=QHBoxLayout()

        #class attributes
        self.desc_lab_path=QLabel('Path')
        self.current_path=QLineEdit('enter path here')
        ##ideally I would have an icon
        self.pathfind_dialogue_button=QPushButton("Find Path")

        self.desc_usr_lab=QLabel('Username')
        self.user_input=QLineEdit('example@company.com')

        self.desc_pass_lab=QLabel('Password')
        self.pass_input=QLineEdit('********')
        ##make the field hide password characters
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.apply=QPushButton('Apply')
        self.apply.clicked.connect(self.apply_changes)
        
        #form rows
        ##file_line item row
        file_item_layout.addWidget(self.current_path)
        file_item_layout.addWidget(self.pathfind_dialogue_button)
        file_item.setLayout(file_item_layout)

        config_form.addRow(self.desc_lab_path,file_item)
        config_form.addRow(self.desc_usr_lab,self.user_input)
        config_form.addRow(self.desc_pass_lab,self.pass_input)
        self.config_menu.setLayout(config_form)

        #adding wigets to layout
        main_layout.addWidget(self.config_menu,0,0)
        main_layout.addWidget(self.apply,1,1)
        self.setLayout(main_layout)
        

        
    def apply_changes(self):
        config={'username':self.user_input.text(),
                   'password':self.pass_input.text(),
                   'path':self.current_path.text()}
        
        conf_fl=open('conf.json','w')
        json.dump(config,conf_fl)
        self.done(1)

class product_picker(QDialog):
    """
    this function is going to help search products, it'll create a list of of checkable products that I can then send back as an argument to 
    the main window. it will have a means to narrow the scope but in principle it will have the complete list you would get from doing Product.get()
    it will have a search function that I intend to work with the regex matching coefficient
    """
    def __init__(self,conf,parent):
        super().__init__(parent)
        self.setWindowTitle('Product Picker')

        #window items
        self.search_bar=QLineEdit()
        self.scope=QComboBox()
        self.scope.addItems(ud.product_type)
        self.search_list=QListWidget()
        self.submit_btn=QPushButton('Submit')
        
        #properties
        self.config=conf
        #data
        self.info=self.get_products(conf)
        print(self.item_dict)
        self.search_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        #layout
        layout=QGridLayout()
        

        layout.addWidget(self.search_bar,0,0)
        layout.addWidget(self.scope,1,0)
        layout.addWidget(self.search_list,2,0)
        layout.addWidget(self.submit_btn,3,1)

        self.setLayout(layout)

        #signals
        self.scope.currentTextChanged.connect(self.new_scope)

    def narrow_scope(func):
        def inner(self,conf,scope='',data=pd.DataFrame):

            names=kph.Products(conf).get()
            if not(scope):
                return func(self,conf,scope,names)
            else:
                names=names.loc[names['Type (Product)']==scope]
                return func(self,conf,scope,names)
        return inner
        
    @narrow_scope
    def get_products(self,conf,scope='',data=pd.DataFrame()):
        
        data['Id_prod_s']=data['Id (Product)'].astype(str)
        display_names=data['Name'].to_list()
        info=data['Id_prod_s'].copy()
        self.item_dict={}
        for i in range(len(info)):
            self.search_list.addItem(display_names[i])
            self.item_dict[i]=self.search_list.item(i)


        return info
    
    def new_scope(self,text):
        self.search_list.clear()
        self.get_products(self.config,text)

    
    
    



        





if __name__=='__main__':
    telescope=QApplication([])

    window=MWindow('Telescope')

    window.show()

    telescope.exec()   