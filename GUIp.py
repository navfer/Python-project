#https://apuntes.de/python/expresiones-regulares-y-busqueda-de-patrones-en-python-poder-y-flexibilidad/#gsc.tab=0
#https://rico-schmidt.name/pymotw-3/pickle/index.html
#https://stackoverflow.com/questions/55809976/seek-on-pickled-data
#https://www.reddit.com/r/learnpython/comments/pgfj63/sorting_a_table_with_pysimplegui/
#https://www.geeksforgeeks.org/python-sorted-function/
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Element_Header_or_Cell_Clicks.py
#https://github.com/PySimpleGUI/PySimpleGUI/issues/5646
#https://docs.python.org/3/howto/sorting.html



from SerializeFile import *
from Customer import *
import PySimpleGUI as sg
import re
import operator

import mysql.connector
from mysql.connector import errorcode


try:
  cnx = mysql.connector.connect(user='root', password='1234',
                                 host='127.0.0.1',
                                 database='testcustomer')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
  exit(-1)






#fCustomer = 'Customer.csv'
#fCustomer = open('Customer.dat', 'rb+')
lCustomer=[]
#df = pd.read_csv(fCustomer,index_col='ID')
rowSelected=-1
pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
pattern_ID = r"\d{3}"
pattern_phone = r"\d{3}-\d{6}"


def addCustomer(l_Customer,t_CustomerInterfaz, oCustomer):
    l_Customer.append(oCustomer)
    saveCustomer(cnx, oCustomer)
    t_CustomerInterfaz.append([oCustomer.ID, oCustomer.name, oCustomer.bill, oCustomer.email, oCustomer.phone,oCustomer.posFile])
    pass

def delCustomer(l_Customer,t_CustomerInterfaz, posinTable):
    cdel=None
    for o in l_Customer:
        if (o.customerinPos(t_CustomerInterfaz[posinTable][0])):
            cdel=o
            break
    if (cdel is not None):
        l_Customer.remove(cdel)
        t_CustomerInterfaz.remove(t_CustomerInterfaz[posinTable])
        cdel.erased=True
        deleteCustomer(cnx, cdel)
    pass

def updateCustomer(l_Customer,t_row_CustomerInterfaz, ind):
    cdel=None
    for o in l_Customer:
        if (o.customerinPos(ind)):
            cdel=o
            break
    if (cdel is not None):
        cdel.setCustomer(t_row_CustomerInterfaz[1],t_row_CustomerInterfaz[2],t_row_CustomerInterfaz[3],t_row_CustomerInterfaz[4])
        modifyCustomer(cnx, cdel)
    pass

def sort_table(table, cols):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table

def popup_select_order(the_list):
    select_multiple=False
    output=[]
    lst_head=sg.Listbox(the_list,key='_LIST_',size=(15,len(the_list)),select_mode='extended' if select_multiple else 'single',bind_return_key=True)
    lst_order=sg.Listbox(output,key='_LIST_OUT_',size=(15,len(the_list)),select_mode='single',bind_return_key=True)
    first_column = [
        [lst_head],
    ]
    second_column = [
        [sg.Button(key="Add Order", image_filename="right.png", image_subsample=18)],
        [sg.Button(key="Del Order", image_filename="left.png", image_subsample=8)],
    ]
    third_column = [
        [lst_order],
    ]
    layout = [
        [sg.Column(first_column),sg.Column(second_column),sg.Column(third_column)],
        [sg.OK()]
    ]
    window = sg.Window('Select Order',layout=layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'OK':
            break
        if event == 'Add Order':
            if (lst_head.get() != []):
                val = lst_head.get()[0]
                the_list.remove(val)
                output.append(val)
                window['_LIST_'].update(the_list)
                window['_LIST_OUT_'].update(output)
        if event == 'Del Order':
            if (lst_order.get() != []):
                val = lst_order.get()[0]
                the_list.append(val)
                output.remove(val)
                window['_LIST_'].update(the_list)
                window['_LIST_OUT_'].update(output)

    window.close()
    del window
    return output

def interfaz():
    font1, font2 = ('Arial', 14), ('Arial', 16)
    sg.theme('Purple')
    sg.set_options(font=font1)
    table_data=[]
    readCustomer(cnx, lCustomer)
    for o in lCustomer:
        if (not o.erased):
            table_data.append([o.ID, o.name, o.bill, o.email, o.phone, o.posFile])

    layout = ([
        [sg.Push(), sg.Text('Veterinary Record'), sg.Push()]] + [
        [sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in Customer.fields.items()] +

    [
        [sg.Push()] +
        [sg.Table(values=table_data, headings=Customer.headings, max_col_width=50, num_rows=10,
            display_row_numbers=False, justification='center', enable_events=True, enable_click_events=True,
            vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            expand_x=True,bind_return_key=True, key='-Table-')],

        [sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')] +
        [sg.Push()],
        [sg.Button('Purge'), sg.Push(),sg.Button('Sort File')],
    ])

    #In this part we can configure a new theme from the project
    sg.theme('DarkBlue1')
    window = sg.Window('Customer Management with Files', layout,finalize=True)
    window['-PosFile-'].update(disabled=True)
    window['-Table-'].bind("<Double-Button-1>", " Double")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
          break
        if event == 'Add':
            Email_Valid=False
            ID_Valid=False
            Phone_Valid=False
            if re.match(pattern_email, values['-Email-']):
                Email_Valid=True
            if re.match(pattern_ID, values['-ID-']):
                ID_Valid = True
            if re.match(pattern_phone, values['-Phone-']):
                Phone_Valid=True

            if (Email_Valid & ID_Valid & Phone_Valid):
                addCustomer(lCustomer,table_data, Customer(values['-ID-'],values['-Name-'],values['-Bill-'],values['-Email-'],values['-Phone-'],-1))
                window['-Table-'].update(table_data)
            else:
                if (not ID_Valid):
                    sg.popup_ok("The customer ID must be at least 3 digits long", title="Ok")
                if (not Email_Valid):
                    sg.popup_ok("The email does not have a correct format", title="Ok")
                if (not Phone_Valid):
                    sg.popup_ok("The phone is not formatted correctly", title="Ok")

        if event == 'Delete':
            if(len(values['-Table-'])>0):
                delCustomer(lCustomer,table_data,values['-Table-'][0])
                window['-Table-'].update(table_data)

        if (event == '-Table- Double'):
            if len(values['-Table-']) > 0:
                rowSelected=values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[rowSelected][0]))
                window['-Name-'].update(str(table_data[rowSelected][1]))
                window['-Bill-'].update(str(table_data[rowSelected][2]))
                window['-Email-'].update(str(table_data[rowSelected][3]))
                window['-Phone-'].update(str(table_data[rowSelected][4]))
                window['-PosFile-'].update(str(table_data[rowSelected][5]))
            pass
        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Name-'].update('')
            window['-Bill-'].update('')
            window['-Phone-'].update('')
            window['-Email-'].update('')
            window['-PosFile-'].update('')
        if event == 'Modify':
            valida=False
            if re.match(pattern_email, values['-Email-']):
                if re.match(pattern_ID, values['-ID-']):
                    if re.match(pattern_phone, values['-Phone-']):
                        valida=True
            if valida:
                table_data[rowSelected][1] = values['-Name-']
                table_data[rowSelected][2] = values['-Bill-']
                table_data[rowSelected][3] = values['-Email-']
                table_data[rowSelected][4] = values['-Phone-']
#               for t in table_data:
#                    if t[-1] == int(values['-PosFile-']):
#                        rowToUpdate=t
#                        t[1], t[2], t[3], t[4] = values['-Name-'], values['-Bill-'], values['-Email-'] , values['-Phone-']
#                      break
                updateCustomer(lCustomer,table_data[rowSelected], values['-ID-'])
                window['-Table-'].update(table_data)
                window['-ID-'].update(disabled=False)
        if isinstance(event, tuple):
        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
        # You can also call Table.get_last_clicked_position to get the cell clicked
            if event[0] == '-Table-':
                if event[2][0] == -1:  # Header was clicked
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)
        if event == 'Purge':
            pass

        if event == 'Sort File':
            lst_full=Customer.headings[:]
            lst = popup_select_order(lst_full)  # returns list of selected items
            lst_index=[]
            for l in lst:
                lst_index.append(Customer.headings.index(l))
            table_data = sort_table(table_data, lst_index)
            sortCustomer(cnx,lst)
            window['-Table-'].update(table_data)

    window.close()

interfaz()
cnx.close()

