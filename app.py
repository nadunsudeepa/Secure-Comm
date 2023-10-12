from flask import Flask,render_template,request
import hashlib
import re
from flask_mysqldb import MySQL
import createKey
import decryptKey
import encryptData

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "kuser"
app.config['MYSQL_PASSWORD'] = "kumudu123"
app.config['MYSQL_DB'] = "SsAssignment"

mysql = MySQL(app)

@app.route('/')
def main():
    return render_template('Registration.html')

@app.route('/Registration',methods=['GET','POST'])
def Registration():
    if request.method == 'POST':
        md5_hash_pass=hashlib.new("md5")
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cpass = request.form['cpass']
        role = request.form['role']

        md5_hash_pass.update(password.encode())
        md5_hash_pass1 = md5_hash_pass.hexdigest()

        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM users where email= %s",(email,))
        account=cur.fetchone()
        if account:
            mesage ="Account already exists !"

        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            mesage="Invalid Email.!!"
        else:
            if password == cpass:
                cur.execute("INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,%s)",(username,email,md5_hash_pass1,role))
                mysql.connection.commit()
                cur.close()
                mesage = "Registration successfully"
                return render_template('SendMessage.html')

            else:
                mesage = "Confirm password not match..!"

        return render_template('Registration.html',mesage=mesage)
    return render_template('Registration.html',mesage = " " )


@app.route('/SendMessage',methods=['GET','POST'])
def SendMessage():
    if request.method == 'POST':
        msg=request.form['message']
        role=request.form['role']

        createKey.KeyGeneration()
        encryptData.Encryption(msg,role)

        return render_template('SendMessage.html',mesage="Message sucessfuly Encrypted")
    else:
        return render_template('SendMessage.html',mesage=' ')
    
@app.route('/RecivedMessage',methods=['GET','POST'])
def RecivedMessage():
    if request.method == 'POST':
        md5_hash_pass=hashlib.new("md5")
        email = request.form['email']
        password = request.form['password']

        md5_hash_pass.update(password.encode())
        md5_hash_pass1 = md5_hash_pass.hexdigest()
        
        cur1=mysql.connection.cursor()
        cur1.execute("SELECT email,password,role FROM users where email= %s and password= %s ",(email,md5_hash_pass1))
        account=cur1.fetchone()
        if account:
            user_type = account[2]
            data= decryptKey.Decryption(user_type)
            return render_template('RecivedMessage.html',Data=data,mesage=" ")  
        else:
            return render_template('RecivedMessage.html',Data='',mesage="Invalid Login !")    
    else:
        return render_template('RecivedMessage.html',mesage=' ')
        
        
@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM users")
    if users > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__ == "__main__":
    app.run(debug=True)
