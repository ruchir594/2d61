import mysql.connector
from worker import Mapped
from user import User

config = {
  'user': 'ruchir',
  'password': 'TnKYH1yV',
  'host': 'sunapee.cs.dartmouth.edu',
  'database': 'ruchir_db',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

#add_zip = ("INSERT INTO Zipcode (Zipcode, City, State, Country) VALUES (%(zip)s, %(city)s, %(state)s, %(country)s)")
#data = {
#    'zip': '03755',
#    'city': 'Hanover',
#    'state': 'NH',
#    'country': 'United States'
#}

#a = ("UPDATE Manuscript SET Status=%(Status)s WHERE Mid=%(Mid)s")
#b = {
#    'Status': 'Double Yo',
#    'Mid': '1234567'
#}
#cursor.execute((a), b)
#cnx.commit()
#cursor.close()
#cnx.close()


people = User()
drive = Mapped()


james = ''
james != 'quit'
login = False
access = None
while james != 'quit':
    #login = True
    #selfid = '10002'
    #access = 'reviewer'
    if not login:
        print 'log in, enter id <_> password!'
        entered = raw_input("> ")
        james = entered
        if entered.split('_') in people.users:
            login = True
            superflag = True
            selfid = entered.split('_')[0]
            access = people.find(entered.split('_')[0])
    else:
        # comes here if only logged in
        print 'What would you like to do?'
        if superflag:
            superflag = False
            a, b = drive.onceprint(selfid, access)
            cursor.execute((a), b)
            for e in cursor:
                if access == 'author':
                    print 'Hello ',  e[3], e[4]
                if access == 'editor':
                    print 'Hello ', e[1], e[2]
                if access == 'reviewer':
                    print 'Hello ', e[1], e[2], ' at ', e[3]
            cnx.commit()
        a, b = drive.process(selfid, access)
        if a and b:
            cursor.execute((a), b)
            for e in cursor:
                print e
            cnx.commit()
            print '...executed!'
        else:
            print '... Cascade Executed!'
        james = raw_input('> ')

#cursor.execute(add_zip, data)


# making sure it is commited
cnx.commit()

#close
cursor.close()
cnx.close()
