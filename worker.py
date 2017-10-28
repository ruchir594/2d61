from cascade import Cas
import datetime

brother = Cas()

class Mapped(object):
    def __init__(self):
        self.d = {}
        self.tab2col = {}

        self.tab2col['Zipcode'] = ['Zipcode','City','State','Country']
        self.tab2col['Address'] = ['Addressid','Zipcode','addressLine1','addressLine2']
        self.tab2col['Affiliation'] = ['Affiliationid','Address_Addressid','Dept','AffType','Designation']
        self.tab2col['Issue'] = ['Issueid','Iyear','Iperiod','totalPageCount','printDate']
        self.tab2col['Editor'] = ['Eid','EFName','ELName','Eemail','Ephoneno','Address_Addressid','Affiliation_Affiliationid']
        self.tab2col['Reviewer'] = ['Rid','RFName','RLName','Remail','Rphoneno','Affiliation_Affiliationid']
        self.tab2col['Manuscript'] = ['Mid','Title','Subtitle','dateReceived','Status','Filepath','isWithinScope','dateAccepted','Editor_Eid']
        self.tab2col['Master_Manu_Issue'] = ['Manuscript_Mid','Issue_Issueid' ,'noOfPages','startPageNo' ,'issuevolume','issuenumber']
        self.tab2col['Master_Manu_Revw'] = ['Manuscript_Mid','Reviewer_Rid','ratingAppropriateness','ratingClarity','ratingMethodology','ratingContribution','finalRecommendation','feedbackDate']
        self.tab2col['Author'] = ['Aid','Address_Addressid','Affiliation_Affiliationid','AFName','ALName','Aphoneno','Aemail']
        self.tab2col['Master_Manu_Auth'] = ['Author_Aid','Manuscript_Mid','AuthorOrderNo']
        self.tab2col['RICode'] = ['code', 'interest']

    def process(self, selfid, access, q=None):
        #temp = {'1': 'insert', '2': 'update', '3': 'delete'}
        if access == 'author':
            #print 'Hello Author,\n'
            print '1. Submit a Manuscript\n2. Retract a Manuscript\n5. Self'
            q = raw_input("> ")
            if q not in ['1', '2', '3', '4', '5']:
                print '---- NOT A VALID RESPONSE ---'
                return None, None
            if q == '1':
                a, b = self.command_builder('Manuscript', 'insert')
                brother.cascade_exec(a, b)
                a, b = self.command_builder('Master_Manu_Auth', 'insert_full', colnames=['Author_Aid','Manuscript_Mid', 'AuthorOrderNo'], retcols = [selfid, b['Mid'], '1'])
                brother.cascade_exec(a, b)
                return None, None
            if q == '2':
                return self.command_builder('Manuscript', 'delete', primeKeys=1)
            if q == '5' or q == 'self':
                return self.command_builder('Author', 'select_special', retcols=[selfid])
            if q == 'quit':
                return

        elif access == 'reviewer':

            #print 'Hello Reviewer,\n'
            print '1. Add a Review \n2. Get All Reviews Assigned'
            q = raw_input("> ")
            if q == '1':
                return self.command_builder('Master_Manu_Revw', 'update', ['ratingAppropriateness','ratingClarity','ratingMethodology','ratingContribution','finalRecommendation','feedbackDate'], primeKeys=2)
            if q == '2':
                return self.command_builder('Master_Manu_Revw', 'select_special', retcols=[selfid])

        else:
            #print 'Hello Editor'
            print '1. Assign Reveiwers \n2. Change Manuscript Status\n3. Add Manuscript to Issue\n4. See Manuscripts by an Author\n5. Publish Issue'
            q = raw_input("> ")
            if q == '1':
                return self.command_builder('Master_Manu_Revw', 'insert', primeKeys=2)
            if q == '2':
                return self.command_builder('Manuscript', 'update', ['Status'], primeKeys=1)
            if q == '4':
                return self.command_builder('Master_Manu_Auth', 'select', colnames=['AuthorAid'], retcols=['*'])
            if q == '5':
                r = raw_input('Enter Issue_Id to publish > ')
                return 'update Manuscript set status=Published where Manuscript.Mid and (Master_Manu_Issue.Manuscript_Mid=Manuscript.Mid and Master_Manu_Issue.Issue_Issueid='+r+');', {"some":"value"}
            print '---- NOT A VALID RESPONSE ---'
            return None, None



    def command_builder(self, tabname, act, colnames=[], primeKeys=None, retcols=[]):
        # returns two string. Which can be passed to executor in main file
        some_head = None
        d = None
        if act == 'insert':
            some_head = 'INSERT INTO '+ tabname +' '#(Zipcode, City, State, Country) VALUES (%(zip)s, %(city)s, %(state)s, %(country)s)'

            temp = ''
            tempval = ''
            for e in self.tab2col[tabname]:
                temp += e + ', '
                tempval += '%(' + e + ')s, '
            temp = temp[:-2]
            tempval = tempval[:-2]

            some_head += '(' + temp + ')'
            some_head += ' VALUES '
            some_head += '(' + tempval + ')'

            #print some_head

            data = {}
            for e in self.tab2col[tabname]:
                print 'Enter value for ' + e + ' .Enter nothing if N/A'
                q = raw_input("> ")
                data[e] = ''
                if q:
                    data[e] = q

            #print data
            #return some_head, data

        elif act == 'update':
            print 'updating ' + tabname + ' requires ' + str(primeKeys) + ' keys.'

            tempkey = ''
            for e in self.tab2col[tabname][:primeKeys]:
                q = raw_input("Enter "+e+" > ")
                tempkey += e + "=" + q + ' AND '
            tempkey = tempkey[:-5]

            some_head = 'UPDATE '+ tabname + ' SET '

            temp = ''
            data = {}
            for e in colnames:
                temp += e + '=%(' + e +')s, '
                data[e] = raw_input('Enter Value for '+e+'>')
            temp = temp[:-2]

            some_head += temp
            some_head += ' WHERE ' + tempkey

            #return some_head, data

        elif act == 'delete':
            print 'Deleting ' + tabname + ' requires ' + str(primeKeys) + ' Keys.'
            temp= ''
            tempkey = ''
            data = {}
            for e in self.tab2col[tabname][:primeKeys]:
                q = raw_input("Enter "+e+" > ")
                tempkey += e + '=%(' + e + ')s AND '
                data[e] = q
            tempkey = tempkey[:-5]

            some_head = 'DELETE FROM ' + tabname + ' WHERE '
            some_head += tempkey
            #print data

            #return some_head, data

        elif act == 'select':
            print 'Okay! Here you go...'
            temp = ''
            data = {}
            if primeKeys:
                for e in self.tab2col[tabname][:primeKeys]:
                    q = raw_input("Enter "+e+" > ")
                    tempkey += e + '=%(' + e + ')s AND '
                    data[e] = q
                tempkey = tempkey[:-5]

            for e in colnames:
                temp += e + '=%(' + e +')s, '
                data[e] = raw_input('Enter Value for '+e+'>')
            temp = temp[:-2]

            some_head = 'SELECT '
            for e in retcols:
                some_head += e + ', '
            some_head = some_head[:-2]

            some_head += ' FROM ' + tabname
            if temp:
                some_head += ' WHERE ' + temp

            #return some_head, data

        elif act == 'select_special':
            #print 'Okay! this is who you are'
            some_head = 'SELECT * FROM '+ tabname + ' WHERE ' + self.tab2col[tabname][0] + ' = ' + retcols[0]
            if tabname == 'Master_Manu_Revw':
                some_head = 'SELECT * FROM '+ tabname + ' WHERE ' + self.tab2col[tabname][1] + ' = ' + retcols[0]
            data = {'some':'values'}
            #return some_head, data

        elif act == 'insert_full':
            some_head = 'INSERT INTO ' + tabname + ' '
            temp = ''
            tempval = ''
            for e in colnames:
                temp += e + ', '
                tempval += '%(' + e + ')s, '
            temp = temp[:-2]
            tempval = tempval[:-2]

            some_head += '(' + temp + ')'
            some_head += ' VALUES '
            some_head += '(' + tempval + ')'

            #print some_head

            data = {}
            for i in range(len(retcols)):
                data[colnames[i]] = retcols[i]
            #print some_head, data
            return some_head, data


        # Default Values

        if 'Editor_Eid' in data:
            data['Editor_Eid'] = '30001'

        if 'Filepath' in data:
            data['Filepath'] = 'drive/dir/path/script/' + data['Mid'] + '.pdf'

        if 'Status' in data and data['Status'] == '':
            data['Status'] = 'Submitted'

        curr_dates = ['feedbackDate', 'dateReceived']
        for e in curr_dates:
            if e in data:
                data[e] = datetime.datetime.today().strftime('%m/%d/%Y')

        default_ints = ['ratingAppropriateness','ratingClarity','ratingMethodology','ratingContribution']
        for e in default_ints:
            if e in data and data[e] == '':
                data[e] = 0

        print some_head, data
        return some_head, data

    def onceprint(self, selfid, access):
        if access == 'author':
            return self.command_builder('Author', 'select_special', retcols=[selfid])
        if access == 'editor':
            return self.command_builder('Editor', 'select_special', retcols=[selfid])
        if access == 'reviewer':
            return self.command_builder('Reviewer', 'select_special', retcols=[selfid])
        return None, None
