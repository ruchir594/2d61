# Note

A list of Valid Id and Password are ['30001', 'qwerty30'], ['10002', 'qwerty2'], ['10003', 'qwerty3'], ['70007', 'qwerty7']

# Architecture

We have implemented some general functions which allow us to do a lot more than what is given in requirements.

## Class Mapped

This is a workhorse of a class. It has a method Command_Builder which takes

1. * Table Name
2. * Action (Insert, Update, Delete, Select)
3. Columns (Necessary for update)
4. Number of Primary key for that tables
5. RetCols (Necessary for Select)

\* are mendatory parameters.

this allows us to call a single function for Editor to Accept, Reject, Typeset, Publish a Manuscript.

Only thing editor has to do it select "update status" and method promps with a command to update status of a given manuscript. Which is also true for Reviewer's ability to submit a review.

Our design is reflects the idea of building an easy GUI front end on top of it, such that a drop down menu can support various values for a parameter.

Some of these parameters are over ridden for special case command builder

## Class Ces

Implemented in file cascade.py, it's functions allow is to cascade queries on SQL.

This was done to add additional features to satisfy real life requirements on updating multiple tables at once.
It was be implemented as a replacement for Trigger.



## Cascade Queries

We have implemented Cascade Queries as and when necessary.

An example.

```
Hello  Benjamin Huff
1. Submit a Manuscript
2. Retract a Manuscript
5. Self
> 1
Enter value for Mid .Enter nothing if N/A
> 666000
Enter value for Title .Enter nothing if N/A
> Cascade Checking X
Enter value for Subtitle .Enter nothing if N/A
> whatever
Enter value for dateReceived .Enter nothing if N/A
>
Enter value for Status .Enter nothing if N/A
>
Enter value for Filepath .Enter nothing if N/A
>
Enter value for isWithinScope .Enter nothing if N/A
>
Enter value for dateAccepted .Enter nothing if N/A
>
Enter value for Editor_Eid .Enter nothing if N/A
>
INSERT INTO Manuscript (Mid, Title, Subtitle, dateReceived, Status, Filepath, isWithinScope, dateAccepted, Editor_Eid) VALUES (%(Mid)s, %(Title)s, %(Subtitle)s, %(dateReceived)s, %(Status)s, %(Filepath)s, %(isWithinScope)s, %(dateAccepted)s, %(Editor_Eid)s) {'Status': 'Submitted', 'Subtitle': 'whatever', 'Filepath': 'drive/dir/path/script/666000.pdf', 'Editor_Eid': '30001', 'Title': 'Cascade Checking X', 'Mid': '666000', 'dateReceived': '10/27/2017', 'isWithinScope': '', 'dateAccepted': ''}

INSERT INTO Master_Manu_Auth (Author_Aid, Manuscript_Mid, AuthorOrderNo) VALUES (%(Author_Aid)s, %(Manuscript_Mid)s, %(AuthorOrderNo)s) {'AuthorOrderNo': '1', 'Author_Aid': '10002', 'Manuscript_Mid': '666000'}
... Cascade Executed!
>

```

Notice, when Author is added, he or she only needs to specify ID for their paper, Title, and subtitle.
This query makes an entry in Manuscript
Later a second query is fired to connect Manuscript with Author, this is done automatically, as we already have ID of person, and the Manuscript ID.

Adding subsequent sub authors is done independently.

# Some Examples of Code

```
log in, enter id <_> password!
> 10003_qwerty3            
What would you like to do?
Hello  Liberty Hensley
1. Submit a Manuscript
2. Retract a Manuscript
5. Self
```

Editor Rejecting Manuscript Example

```
Hello Editor
1. Assign Reveiwers
2. Change Manuscript Status
3. Add Manuscript to Issue
4. See Manuscripts by an Author
> 2
updating Manuscript requires 1 keys.
Enter Mid > 1230002
Enter Value for Status>Rejected
...executed!
```


Reviewer adding reviews is super easy!

```
Hello Reviewer,

1. Add a Review
2. Get Pending Review ID
> 1
updating Master_Manu_Revw requires 2 keys.
Enter Manuscript_Mid > 1230002
Enter Reviewer_Rid > 70010
Enter Value for ratingAppropriateness>8
Enter Value for ratingClarity>5
Enter Value for ratingMethodology>5
Enter Value for ratingContribution>8
Enter Value for finalRecommendation>yes
Enter Value for feedbackDate>
{'ratingContribution': '8', 'feedbackDate': '10/27/2017', 'ratingAppropriateness': '8', 'ratingMethodology': '5', 'finalRecommendation': 'yes', 'ratingClarity': '5'}
...executed!
```

Ability for a Reviewer to see every review he/she was assigned.
```
greywind:2d ruchir$ python try.py
log in, enter id <_> password!
> 70007_qwerty7
What would you like to do?
SELECT * FROM Reviewer WHERE Rid = 70007 {'some': 'values'}
Hello  Rana Avery  at  ac.facilisis.facilisis@atvelit.net
1. Add a Review
2. Get All Reviews Assigned
> 2
SELECT * FROM Master_Manu_Revw WHERE Reviewer_Rid = 70007 {'some': 'values'}
(100009, 70007, 1, 4, 6, 6, u'no', u'07/19/2017')
(100025, 70007, 6, 2, 6, 5, u'yes', u'02/18/2017')
(100049, 70007, 3, 2, 6, 7, u'yes', u'02/27/2018')
(100050, 70007, 2, 5, 7, 10, u'no', u'05/23/2017')
(100075, 70007, 8, 2, 10, 3, u'yes', u'04/09/2018')
...executed!
>

```


# Scope of Improvements

### Design of Database

Foreign key constraints have "No Action on UPDATE and DELETE" and should have been set to "CASCADE". Which interferes with Editors ability to Publish an Issue.

### Design of Architecture

Design can be handled much better with always Cascade on running an SQL query.
