class Animal:
    #The headings are the column names for attributes
    headings = ['ID','Name','Type', 'Phone','Owner','Adress']

    #Fields assigns keys for GUI identifiers to the corresponding field names
    fields = {
        '-Name-': 'Pet Name:',
        '-Type-': 'Type:',
        '-Phone-': 'Phone:',
        '-Owner-': 'Owner Name:',
        '-Adress-': 'Email Adress:',
    }

    #Class constructor
    def __init__(self,ID,name,type,phone,owner,adress):
        self.ID = ID
        self.name = name
        self.type = type
        self.phone = phone
        self.owner = owner
        self.adress = adress
        self.erased = False


    def __eq__(self, oA):
        return oA.ID==self.ID

    def __str__(self):
        return str(self.ID)+str(self.name)+str(self.type)+str(self.phone)+str(self.owner)+str(self.adress)
    def animalinPos(self,pos):
        return self.ID==pos


    def setAnimal(self,name, type, phone, owner, adress):
        self.name = name
        self.type = type
        self.phone = phone
        self.owner = owner
        self.adress = adress


    def getAnimalDict(self):
        return {
            'name': self.name,
            'type': self.type,
            'phone': self.phone,
            'owner': self.owner,
            'adress': self.adress,
            'erased': self.erased
        }

    def getAnimalHeadsToModify(self):
        return ['name', 'type', 'phone', 'owner', 'adress', 'erased']

    def getAnimalValuesToModify(self):
        return [self.name, self.type, self.phone, self.owner, self.adress, self.erased]