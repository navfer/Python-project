class Customer:
    headings = ['ID','Name','Bill Address','Email','Phone','Pos']
    fields = {
        '-ID-': 'Customer ID:',
        '-Name-': 'Customer Name:',
        '-Bill-': 'Billing Address:',
        '-Email-': 'Email:',
        '-Phone-': 'Phone:',
        '-PosFile-': 'Position into File'
    }

    # El método __init__ es llamado al crear el objeto
    def __init__(self, ID, name, bill, email,phone, posFile):
        # Atributos de instancia
        self.ID = ID
        self.name = name
        self.bill = bill
        self.email = email
        self.phone = phone
        self.posFile = posFile
        self.erased = False

    def __eq__(self, oC):
        return oC.ID==self.ID

    def __str__(self):
        return str(self.ID)+str(self.name)+str(self.bill)+str(self.email)+str(self.phone)+str(self.posFile)
    def customerinPos(self,pos):
        return self.ID==pos

    def setCustomer(self,name, bill, email, phone):
        self.name = name
        self.bill = bill
        self.email = email
        self.phone = phone

    def getCustomerDict(self):
        return {
            'name': self.name,
            'Bill Address': self.bill,
            'email': self.email,
            'phone': self.phone,
            'pos': self.posFile,
            'erased': self.erased
        }

    def getCustomerHeadsToModify(self):
        return ['name','Bill Address','email','phone','pos','erased']

    def getCustomerValuesToModify(self):
        return [self.name,self.bill,self.email,self.phone,self.posFile,self.erased]