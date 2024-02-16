import pickle
from Customer import *

def saveCustomer(cnx,oC):
    cursor = cnx.cursor()
    add_Customer = ("INSERT INTO Customer "
                    "(ID, Name, Bill, email, Phone) "
                    "VALUES (%s, %s, %s, %s, %s)")
    data_Customer = (oC.ID, oC.name , oC.bill, oC.email, oC.phone)
    cursor.execute(add_Customer, data_Customer)
    cnx.commit()
    cursor.close()

def deleteCustomer(cnx,oC):
    cursor = cnx.cursor()
    delete_Customer = ("DELETE FROM Customer "
                       "WHERE ID=%s ")
    cursor.execute(delete_Customer, (oC.ID,))
    cnx.commit()
    cursor.close()
def modifyCustomer(cnx,oC):
    cursor = cnx.cursor()
    modify_Customer = ("UPDATE Customer SET Name=%s, Bill=%s, email=%s, Phone=%s WHERE ID=%s ")
    data_Customer = (oC.name , oC.bill, oC.email, oC.phone, oC.ID)
    cursor.execute(modify_Customer, data_Customer)
    cnx.commit()
    cursor.close()

def readCustomer(cnx,lC):
    cursor = cnx.cursor()
    query = ("SELECT ID, Name, Bill, email, Phone FROM Customer ")
    cursor.execute(query)
    myresult = cursor.fetchall()
    for row in myresult:
        lC.append(Customer(row[0], row[1], row[2],row[3], row[4],-1))
    cursor.close()

def sortCustomer(cnx,lst):
    cursor = cnx.cursor()
    query = ("ALTER TABLE Customer ORDER BY ")
    order_Customer= ', '.join(lst)
    query = query + order_Customer
    cursor.execute(query)
    cnx.commit()
    cursor.close()