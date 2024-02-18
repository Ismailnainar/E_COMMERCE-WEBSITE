from flask import Flask,render_template,redirect,request,url_for,session
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length
from wtforms.validators import input_required,length


app=Flask(__name__)
app.secret_key = "Mohamed@124"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='Ismail@1529'
app.config['MYSQL_DB'] ='e_com'

mysql = MySQL(app)
def isloggedin():
    return "Name" in session


class user:

    def __init__(self,id,Name,Password):
        self.id=id
        self.Name=Name
        self.Password=Password
class signupForm(FlaskForm):
    Name = StringField('Name', validators=[InputRequired(),Length(min=4,max=20)])
    Password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=20)])
    submit = SubmitField('signup')

class LoginForm(FlaskForm):
     Name = StringField('Name', validators=[InputRequired(),Length(min=4,max=20)])
     Password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=20)])
     submit = SubmitField('Login')

class AddProduct(FlaskForm):
    Name=StringField('Name',validators=[InputRequired(),Length(min=4,max=20)])
    Company_Name=StringField('Company_Name',validators=[InputRequired(),Length(min=4,max=20)])
    Price=StringField('Price',validators=[InputRequired(),Length(min=2,max=20)])
    Quantity=StringField('Quantity',validators=[InputRequired(),Length(min=2,max=20)])
    Submit=SubmitField('submit')

@app.route('/',methods=["GET","POST"])

def signup():
    form = signupForm()
    if form .validate_on_submit():
        Name=form.Name.data
        Password=form.Password.data
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO signup (Name,Password) VALUES(%s,%s)",(Name,Password))
        cur.connection.commit()
        cur.close()
        return redirect (url_for('login'))
    return render_template('signup.html',form=form)
   
@app.route('/login',methods=["GET","POST"])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        Name = form.Name.data
        Password = form.Password.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM signup WHERE Name=%s AND Password=%s",(Name,Password))
        data = cur.fetchall()
        cur.connection.commit()
        cur.close()
        if data:
            session["Name"] = Name
            return redirect(url_for('tabel'))
        else:
            return "invalid login password"
    return render_template("login.html",form=form)

@app.route('/tabel')
def tabel():
   if isloggedin:
     Name=session['Name']
     cur = mysql.connection.cursor()
     cur.execute("SELECT * FROM website WHERE Name=%s",(Name,))
     data = cur.fetchall()
     cur.connection.commit()
     cur.close()
     return render_template("table.html",values=data)

@app.route('/ADD',methods=["GET","POST"])
def ADD():
 form=AddProduct()
 if form.validate_on_submit():
  
    Company_Name = form.Company_Name.data
    Name = form.Name.data
    Price = form.Price.data
    Quantity = form.Quantity.data
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO website (Company_Name,Name,Price,Quantity) VALUES(%s,%s,%s,%s)",(Company_Name,Name,Price,Quantity))
    cur.connection.commit()
    cur.close()
    return redirect(url_for('tabel'))
 return render_template("add.html",form=form)

@app.route('/')
def logout():
    session.pop("Name",None)
    redirect(url_for('signup'))

if __name__ == "__main__":
    app.run(debug=True)