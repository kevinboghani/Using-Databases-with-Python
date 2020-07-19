import sqlite3
con = sqlite3.connect('emaildb.sqlite')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

fname = input('Enter file name: ')
if len(fname)<1:
    fname = 'mbox.txt'
h = open(fname)
for line in h:
    if not line.startswith('From: '):
        continue
    words = line.split()
    email = words[1]
    temp = email.split('@')
    org = temp[1]
    cur.execute('SELECT count FROM Counts WHERE org = ?',(org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts VALUES (?,1)',(org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',(org,))
con.commit()
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
for row in cur.execute(sqlstr):
    print(str(row[0]),row[1])
con.close()