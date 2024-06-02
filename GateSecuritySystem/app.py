from flask import Flask, request,render_template, redirect,session,Response
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import cv2
import pyzbar.pyzbar as pyzbar
import mysql.connector
from flask_admin import Admin
import qrcode
import os
from datetime import datetime

import time
from flask_admin.contrib.sqla import ModelView




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:9923@localhost/db'

db = SQLAlchemy(app)
app.secret_key = 'secret_key'
admin=Admin()  
admin.__init__(app)




#------create user table-----
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    mobile_number = db.Column(db.String(20))  # Mobile number field
    date_of_birth = db.Column(db.Date)        # Date of birth field
    
    password = db.Column(db.String(100))



    def __init__(self,email,password,name,mobile_number, date_of_birth):
        self.name = name
        self.email = email
        self.mobile_number = mobile_number
        self.date_of_birth = date_of_birth
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


admin.add_view(ModelView(User,db.session))




#--------------scurity gaurd-----------------

class Security(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    mobile_number = db.Column(db.String(20))  # Mobile number field
    date_of_birth = db.Column(db.Date)        # Date of birth field
    
    password = db.Column(db.String(100))



    def __init__(self,email,password,name,mobile_number, date_of_birth):
        self.name = name
        self.email = email
        self.mobile_number = mobile_number
        self.date_of_birth = date_of_birth
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


admin.add_view(ModelView(Security,db.session))   

#----------For admin-----------------------

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    mobile_number = db.Column(db.String(20))  # Mobile number field
    date_of_birth = db.Column(db.Date)        # Date of birth field
    
    password = db.Column(db.String(100))



    def __init__(self,email,password,name,mobile_number, date_of_birth):
        self.name = name
        self.email = email
        self.mobile_number = mobile_number
        
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), )
    mobile_number = db.Column(db.String(20))  # Mobile number field
    date_of_birth = db.Column(db.Date)
    entry_time=db.Column(db.Time)
    entry_date = db.Column(db.Date)
    def __init__(self,email,name,mobile_number, date_of_birth,entry_time,entry_date):
        self.name = name
        self.email = email
        self.mobile_number = mobile_number
        self.date_of_birth = date_of_birth
        self.entry_time = entry_time
        self.entry_date=entry_date

with app.app_context():
    db.create_all()

admin.add_view(ModelView(Visitor,db.session))





class UserEnter(db.Model):
    __tablename__ = 'userenter'
    ID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    entry_time = db.Column(db.Time, nullable=False)

# Create tables if they do not exist
with app.app_context():
    db.create_all()

admin.add_view(ModelView(UserEnter,db.session))



class UserExit(db.Model):
    __tablename__ = 'userexit'
    ID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    exit_time = db.Column(db.Time, nullable=False)

# Create tables if they do not exist
with app.app_context():
    db.create_all()

admin.add_view(ModelView(UserExit,db.session))





#-------genrate qr code-------

def genrate_qr(qrdata):
    qrdata = qrdata

# Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # QR code version (1 to 40, default is 1)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level ('L', 'M', 'Q', 'H')
        box_size=10,  # Size of each box (pixels)
        border=4,  # Border size (number of boxes)
    )

# Add data to the QR code
    qr.add_data(qrdata)

# Make the QR code
    qr.make(fit=True)

# Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

# Save the image
    qr_path=os.path.join(app.static_folder, f"{qrdata}.png")
    img.save(qr_path)


#----------scaner-----
def gen_frames():
    camera = cv2.VideoCapture(0)
    scanning = True
    qr_data = None
    while True:
        success, frame = camera.read()  
        if not success:
            break
        else:
            if scanning:
                decoded_objects = decode_qr(frame)
                for obj in decoded_objects:
                    (x, y, w, h) = obj.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    qr_data = obj.data.decode("utf-8")
                    cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    print("QR Code:", qr_data)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')
                if decoded_objects:
                     
                    insert_data(qr_data)
                    
                    scanning = False                    

                    time.sleep(5)  
                    scanning = True  
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')
    camera.release()



def decode_qr(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Use pyzbar to decode QR codes
    decoded_objects = pyzbar.decode(gray)
    return decoded_objects


#------user is present or not-------
            

##second camera

def gen_frames1():
    camera = cv2.VideoCapture(1)
    scanning = True
    while True:
        success, frame = camera.read()  
        if not success:
            break
        else:
            if scanning:
                decoded_objects = decode_qr1(frame)
                for obj in decoded_objects:
                    (x, y, w, h) = obj.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    qr_data = obj.data.decode("utf-8")
                    cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    print("QR Code:", qr_data)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')
                if decoded_objects:
                    insert_data_exit(qr_data)
                    scanning = False

                    
                    
                    time.sleep(5)  
                    scanning = True  
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')
    camera.release()


def decode_qr1(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Use pyzbar to decode QR codes
    decoded_objects = pyzbar.decode(gray)
    return decoded_objects






#----------insert entry time and exit time-------




    
#insert data entry;

import mysql.connector
import datetime

def insert_data(qr_data):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="9923",
            database="db"
        )

        cursor = mydb.cursor()

        # Get current date and time
        current_datetime = datetime.datetime.now()
        entry_time = current_datetime.strftime("%H:%M:%S")
        date = current_datetime.strftime("%Y-%m-%d")
        

        # Prepare and execute the INSERT INTO statement
        insert_query = "INSERT INTO userenter ( email, date, entry_time) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, ( qr_data, date, entry_time))

        # Commit the transaction
        mydb.commit()

        print("Data inserted successfully.")

    except mysql.connector.Error as error:
        print(f"Failed to insert data into userenter table: {error}")

    finally:
        # Close cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'mydb' in locals():
            mydb.close()

# Example usage




def insert_data_exit(qr_data):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="9923",
            database="db"
        )

        cursor = mydb.cursor()

        # Get current date and time
        current_datetime = datetime.datetime.now()
        exit_time = current_datetime.strftime("%H:%M:%S")
        date = current_datetime.strftime("%Y-%m-%d")
        

        # Prepare and execute the INSERT INTO statement
        insert_query = "INSERT INTO userexit ( email, date, exit_time) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, ( qr_data, date, exit_time))

        # Commit the transaction
        mydb.commit()


        print("Data inserted successfully.")

    except mysql.connector.Error as error:
        print(f"Failed to insert data into userexit table: {error}")

    finally:
        # Close cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'mydb' in locals():
            mydb.close()






    







            

#------create table for perticular user---------
'''def user_entry(table_id):
    

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9923",
    database="db")

    if mydb.is_connected():
        print("Connected to MySQL!")
        cursor = mydb.cursor()
    
    cursor.execute(f"""

        CREATE TABLE user{table_id} (
            email VARCHAR(255),
            date DATE,
            entry_time TIME ,
            exit_time TIME ,
            spend_time TIME 
            );

        """)
    mydb.commit()
    
    mydb.close()

    
    
'''








@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile_number = request.form['mobile_number']
        date_of_birth = request.form['date_of_birth']

        new_user = User(name=name, email=email, password=password, mobile_number=mobile_number, date_of_birth=date_of_birth)
        db.session.add(new_user)
        db.session.commit()

        genrate_qr(new_user.email)
        #table create
        #user_entry(new_user.id)
        return redirect('/login')


    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')

#----------for securtiy gaurd-----------------


@app.route('/security_register',methods=['GET','POST'])
def sescurity_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile_number = request.form['mobile_number']
        date_of_birth = request.form['date_of_birth']

        security = Security(name=name, email=email, password=password, mobile_number=mobile_number, date_of_birth=date_of_birth)
        db.session.add(security)
        db.session.commit()

        
        
        return redirect('/admin')


    return render_template('security_register.html')

#---------------for security login-----------


@app.route('/security_login',methods=['GET','POST'])
def security_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        security = Security.query.filter_by(email=email).first()
        
        if security and security.check_password(password):
            session['email'] = security.email
            return redirect('/gaurd')
        else:
            return render_template('security_login.html',error='Invalid user')

    return render_template('security_login.html')


@app.route('/gaurd')
def gaurd():
    if session['email']:
        security = Security.query.filter_by(email=session['email']).first()
        
        
        return render_template('gaurd_dashboard.html' )
    
    return redirect('/security_login')














@app.route('/admin_register',methods=['GET','POST'])
def admin_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile_number = request.form['mobile_number']
        date_of_birth = request.form['date_of_birth']

        admin = Admin(name=name, email=email, password=password, mobile_number=mobile_number, date_of_birth=date_of_birth)
        db.session.add(admin)
        db.session.commit()

        
        #table create
        #user_entry(new_user.id)
        return redirect('/admin_login')
    return render_template('adminregister_page.html')


@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        admin = Admin.query.filter_by(email=email).first()
        
        if admin and admin.check_password(password):
            session['email'] = admin.email
            return redirect('/admin')
        else:
            return render_template('adminlogin_page.html',error='Invalid user')

    return render_template('adminlogin_page.html')


@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        user_enter_data = UserEnter.query.all()
        user_exit_data = UserExit.query.all()
        image_path=f'{user.email}.png'
        return render_template('Dashboard.html', user=user,user_enter_data=user_enter_data ,user_exit_data=user_exit_data,image_path=image_path)
    
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/')

@app.route('/scanner')
def scanner():

    return render_template('scanner.html')

@app.route('/Qr_image')
def Qr_image():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        image_path=f'{user.email}.png'
    return render_template('qr_image.html' ,image_path=image_path)



@app.route('/visitor',methods=['GET','POST'])
def visitor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        mobile_number = request.form['mobile_number']
        date_of_birth = request.form['date_of_birth']

        current_datetime = datetime.datetime.now()
        entry_time = current_datetime.strftime("%H:%M:%S")
        entry_date = current_datetime.strftime("%Y-%m-%d")


        

        visitor = Visitor(name=name, email=email,  mobile_number=mobile_number, date_of_birth=date_of_birth,entry_date=entry_date,entry_time=entry_time)
        db.session.add(visitor)
        db.session.commit()
        return render_template('index.html')




    return render_template('visitor.html')



@app.route('/entry_exit_page')
def entry_exit_page():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        email = user.email
        if email:
        # Correct the filter condition
            user_enter_data = UserEnter.query.filter(UserEnter.email == email).all()
            user_exit_data = UserExit.query.filter(UserExit.email == email).all()
        else:
            user_enter_data = UserEnter.query.all()
            
        
        

    return render_template('entry_exit_page.html' , user=user, user_enter_data=user_enter_data ,user_exit_data=user_exit_data)


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/video_feed')

def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/video_feed1')

def video_feed1():
    return Response(gen_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)

