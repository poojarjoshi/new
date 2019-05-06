from flask import Flask, render_template,redirect,url_for,request
import sqlite3
import subprocess,sys,os

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/users')
def get_users():
    con = sqlite3.connect('firewall.db')
    #con.row_factory = lambda cursor, row: row[0]
    db = con.cursor()
    res = db.execute('select * from IPDetails')
    #res1 = db.execute('select * from SecGroupDetails')
    res2 = db.execute('select SGID from SecGroupDetails ')
    for sgid  in res2:
     index = 0 
     print ('sgid  is' , sgid)
     IPDetails = db.execute('select IP, Port from IPDetails ')
     for IP,Port in IPDetails:
      Port= str(Port)
      print ('ip and port',(IP,Port))
      #subprocess.Popen(['aws', 'ec2', 'authorize-security-group-ingress', '--group-id',sgid, '--protocol','tcp' ,'--port', str(Port), '--cidr',IP) ])
      subprocess.Popen(['aws', 'ec2', 'authorize-security-group-ingress', '--group-id', sgid[index], '--protocol', 'tcp' ,'--port',Port, '--cidr',IP])
     index += 1 
      #output = variable.communicate()
     # rc = variable.returncode
     # print("value is" ,rc)

    return render_template('sample1.html', rows=res.fetchall())

@app.route('/delete/<int:value>', methods=['POST'])
def delete_user(value):
    con = sqlite3.connect('firewall.db')
    db = con.cursor()

    res = db.execute('delete from IPDetails where ID = ?',(value,))
    con.commit() 
    con.close() 
    return redirect(url_for('get_users'))

@app.route('/add/', methods=['POST'])
def add_user():
    con = sqlite3.connect('firewall.db')
    db = con.cursor()
    ID=request.form.get('one')
    IP=request.form.get('two')
    Description=request.form.get('three')
    Port=request.form.get('four')
    res = db.execute('insert into IPDetails (ID,IP,Description,Port) values (?,?,?,?)',(ID,IP,Description,Port))
    con.commit()
    con.close()
    return redirect(url_for('get_users'))


@app.route('/sync/', methods=['POST'])
def sync_user():
        con = sqlite3.connect('firewall.db')
        db = con.cursor()
                
        res = db.execute('select SGID from SecGroupDetails ')
        print (res)
        con.commit()
        con.close()
        return 'sucessfully synced SG'


if __name__ == "__main__":
    app.run(port=8015)
