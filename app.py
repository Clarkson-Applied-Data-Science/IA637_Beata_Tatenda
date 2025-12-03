from flask import Flask, render_template, request, session, redirect, send_from_directory
from flask_session import Session
from datetime import timedelta
import time

from user import user
from room import room
from appointment import appointment
from checkin import checkin

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'sdfvbgfdjeR5y5r'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
Session(app)

# --------------------------------------------------------
# BASIC UTILITIES
# --------------------------------------------------------
@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

def checkSession():
    if 'active' in session:
        if time.time() - session['active'] > 500:
            return False
        session['active'] = time.time()
        return True
    return False

# --------------------------------------------------------
# LOGIN / LOGOUT
# --------------------------------------------------------
@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    un = request.form.get('name')
    pw = request.form.get('password')

    if un and pw:
        u = user()
        if u.tryLogin(un, pw):
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('/main')
        return render_template('login.html', msg='Incorrect username or password.')

    return render_template('login.html', msg='Welcome back')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', msg="You have logged out.")

# --------------------------------------------------------
# SIGNUP (PATIENTS ONLY)
# --------------------------------------------------------
@app.route('/signup', methods=['GET','POST'])
def signup():
    u = user()

    
    if 'user' in session and session['user']['role'] == 'doctor':
        return render_template("ok_dialog.html", msg="Doctors cannot access signup.")

    if request.method == 'POST':
        d = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'password2': request.form.get('password2'),
            'role': 'patient'
        }
        u.set(d)
        if u.verify_new():
            u.insert()
            return render_template('ok_dialog.html', msg="Account created. Please log in.")
        return render_template('signup.html', obj=u)

    u.createBlank()
    return render_template('signup.html', obj=u)

# --------------------------------------------------------
# MAIN MENU
# --------------------------------------------------------
@app.route('/main')
def main():
    if not checkSession():
        return redirect('/login')
    return render_template('main.html')

# --------------------------------------------------------
# USER MANAGEMENT (DOCTORS ONLY)
# -----------------------------------------------------
@app.route('/users/manage', methods=['GET','POST'])
def manage_user():
    if checkSession() == False:
        return redirect('/login')

    
    if session['user']['role'] != 'doctor':
        return render_template('ok_dialog.html', msg="Access denied.")

    o = user()
    action = request.args.get('action')
    pkval = request.args.get('pkval')

    
    if pkval == 'new' or action == 'insert':
        return render_template(
            'ok_dialog.html',
            msg="Doctors cannot create accounts. Patients must sign up themselves."
        )

    # DELETE USER
    if action == 'delete':
        o.deleteById(pkval)
        return render_template(
            'ok_dialog.html',
            msg=f"User ID {pkval} has been deleted."
        )

    # UPDATE USER (doctor editing)
    if action == 'update':
        o.getById(pkval)
        o.data[0]['name'] = request.form.get('name')
        o.data[0]['email'] = request.form.get('email')
        o.data[0]['role'] = request.form.get('role')
        o.data[0]['password'] = request.form.get('password')
        o.data[0]['password2'] = request.form.get('password2')

        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html', msg="User updated successfully.")
        else:
            return render_template('users/manage.html', obj=o)

    # LIST ALL USERS
    if pkval is None:
        o.getAll()
        return render_template('users/list.html', obj=o)

    # MANAGE SPECIFIC USER
    o.getById(pkval)
    return render_template('users/manage.html', obj=o)


# --------------------------------------------------------
# ROOM MODULE
# --------------------------------------------------------
@app.route('/rooms')
def rooms_home():
    if not checkSession(): return redirect('/login')
    r = room()
    r.getAll()
    return render_template("room/list.html", obj=r)

@app.route('/rooms/manage', methods=['GET','POST'])
def manage_room():
    if not checkSession(): return redirect('/login')

    o = room()
    action = request.args.get('action')
    pkval = request.args.get('pkval')

    if action == 'delete':
        o.deleteById(pkval)
        return render_template('ok_dialog.html', msg=f"Room {pkval} deleted.")

    if action == 'insert':
        d = {
            'roomtype': request.form.get('roomtype'),
            'roomnumber': request.form.get('roomnumber')
        }
        o.set(d)
        o.insert()
        return render_template('ok_dialog.html', msg="Room added.")

    if action == 'update':
        o.getById(pkval)
        o.data[0]['roomtype'] = request.form.get('roomtype')
        o.data[0]['roomnumber'] = request.form.get('roomnumber')
        o.update()
        return render_template('ok_dialog.html', msg="Room updated.")

    if pkval == 'new':
        o.createBlank()
        return render_template('room/add.html', obj=o)

    if pkval:
        o.getById(pkval)
        return render_template('room/manage.html', obj=o)

    o.getAll()
    return render_template('room/list.html', obj=o)

# --------------------------------------------------------
# --------------------------------------------------------
# APPOINTMENT MODULE
# --------------------------------------------------------

@app.route('/appointments')
def appointments():
    if not checkSession():
        return redirect('/login')

    o = appointment()
    me = session['user']


    if me['role'] == 'doctor':
        o.getAll()
    else:
        o.getByField("patientid", me['uid'])

    return render_template("appointment/list.html", obj=o, me=me)


# --------------------------------------------------------
# MANAGE APPOINTMENT
# --------------------------------------------------------
@app.route('/appointments/manage', methods=['GET','POST'])
def manage_appointment():
    if not checkSession():
        return redirect('/login')

    o = appointment()
    me = session['user']
    action = request.args.get('action')
    pkval   = request.args.get('pkval')

    # ----------------------------------------------------
    # DELETE — DOCTOR ONLY
    # ----------------------------------------------------
    if action == 'delete':
        if me['role'] != 'doctor':
            return render_template("ok_dialog.html", msg="Access denied.")
        o.deleteById(pkval)
        return render_template("ok_dialog.html", msg="Appointment deleted.")


    # ----------------------------------------------------
    # INSERT — Patient request OR Doctor creation
    # ----------------------------------------------------
    if action == 'insert':
        d = {}
        d['date'] = request.form.get('date')
        d['time'] = request.form.get('time')

        if me['role'] == 'patient':
            d['patientid'] = me['uid']
            d['doctorid']  = None
            d['duration']  = 0
            d['status']    = "requested"


        else:
            d['patientid'] = request.form.get('patientid') or None
            d['doctorid']  = request.form.get('doctorid') or None
            d['duration']  = request.form.get('duration') or 0
            d['status']    = request.form.get('status')

        o.set(d)

        if o.verify_new():
            o.insert()
            return render_template("ok_dialog.html", msg="Appointment added.")

        return render_template("appointment/add.html", obj=o, me=me)


    # ----------------------------------------------------
    # UPDATE — DOCTOR ONLY
    # ----------------------------------------------------
    if action == 'update':
        if me['role'] != 'doctor':
            return render_template("ok_dialog.html", msg="Patients cannot update appointments.")

        o.getById(pkval)

        o.data[0]['date']     = request.form.get('date')
        o.data[0]['time']     = request.form.get('time')
        o.data[0]['duration'] = request.form.get('duration') or 0
        o.data[0]['status']   = request.form.get('status')
        o.data[0]['doctorid'] = request.form.get('doctorid') or None   

        o.update()
        return render_template("ok_dialog.html", msg="Appointment updated.")

    if pkval == 'new':
        o.createBlank()
        return render_template("appointment/add.html", obj=o, me=me)

    if pkval:
        o.getById(pkval)

        
        u = user()
        u.getByField("role", "doctor")
        doctors = u.data

        return render_template(
            "appointment/manage.html",
            obj=o,
            doctors=doctors,
            me=me
        )

    return redirect('/appointments')

# --------------------------------------------------------
# CHECK-IN MODULE (DOCTOR ONLY)
# --------------------------------------------------------
@app.route('/checkin')
def checkin_list():
    if not checkSession(): 
        return redirect('/login')

    if session['user']['role'] != 'doctor':
        return render_template("ok_dialog.html", msg="Access denied.")

    o = checkin()
    o.getAll()
    return render_template("checkin/list.html", obj=o)



@app.route('/checkins/manage', methods=['GET','POST'])
def manage_checkin():
    if not checkSession(): 
        return redirect('/login')


    if session['user']['role'] != 'doctor':
        return render_template("ok_dialog.html", msg="Access denied.")

    o = checkin()
    action = request.args.get('action')
    pkval = request.args.get('pkval')

    # ----------------------------------------------------
    # DELETE
    # ----------------------------------------------------
    if action == 'delete':
        o.deleteById(pkval)
        return render_template("ok_dialog.html", msg="Check-in deleted.")

    # ----------------------------------------------------
    # INSERT (doctor creates check-in)
    # ----------------------------------------------------
    if action == 'insert':

        d = {
            'aid': request.form.get('aid'),
            'uid': session['user']['uid'],   
            'rid': request.form.get('rid'),
            'checkintime': request.form.get('checkintime'),
            'checkouttime': request.form.get('checkouttime'),
            'status': request.form.get('status')
        }

        o.set(d)
        o.insert()

        return render_template("ok_dialog.html", msg="Check-in added.")

    # ----------------------------------------------------
    # UPDATE
    # ----------------------------------------------------
    if action == 'update':
        o.getById(pkval)
        row = o.data[0]

        row['rid'] = request.form.get('rid')
        row['checkintime'] = request.form.get('checkintime')
        row['checkouttime'] = request.form.get('checkouttime')
        row['status'] = request.form.get('status')

        o.update()
        return render_template("ok_dialog.html", msg="Check-in updated.")

    # ----------------------------------------------------
    # CREATE NEW CHECK-IN FORM
    # ----------------------------------------------------
    if pkval == 'new':

        o.createBlank()

        a = appointment()
        a.cur.execute("""
            SELECT a.aid, a.date, a.time, p.name AS patient_name
            FROM appointment a
            LEFT JOIN user p ON a.patientid = p.uid
            WHERE a.status = 'confirmed'
            ORDER BY a.date, a.time
        """)
        appts = a.cur.fetchall()

        # Load rooms
        r = room()
        r.getAll()

        return render_template(
            "checkin/add.html",
            obj=o,
            appointments=appts,
            rooms=r.data,
            doctor=session['user']
        )

    # ----------------------------------------------------
    # EDIT CHECK-IN FORM
    # ----------------------------------------------------
    if pkval:
        o.getById(pkval)

        r = room()
        r.getAll()

        return render_template("checkin/manage.html", obj=o, rooms=r.data)

    o.getAll()
    return render_template("checkin/list.html", obj=o)
# --------------------------------------------------------
# PATIENT CHECK-IN START
# --------------------------------------------------------
@app.route('/checkin/start')
def patient_checkin_start():
    if not checkSession(): 
        return redirect('/login')

    me = session['user']

    if me['role'] != 'patient':
        return render_template("ok_dialog.html", msg="Doctors cannot use patient check-in.")

    o = appointment()
    o.getUpcomingForPatient(me['uid'])

    if len(o.data) == 0:
        return render_template("ok_dialog.html", msg="You have no upcoming appointments.")

    return render_template("checkin/start.html", obj=o)
# --------------------------------------------------------
# PATIENT SELF CHECK-IN — QUICK CHECK IN
# --------------------------------------------------------
@app.route('/checkin/submit/<aid>')
def patient_submit_checkin(aid):
    if not checkSession():
        return redirect('/login')

    me = session['user']

    if me['role'] != 'patient':
        return render_template("ok_dialog.html", msg="Access denied.")

    o = checkin()
    
    d = {
        'aid': aid,
        'uid': me['uid'],          
        'rid': None,               
        'checkintime': time.strftime("%H:%M"),
        'checkouttime': None,
        'status': "waiting"
    }

    o.set(d)
    o.insert()

    return render_template(
        "ok_dialog.html",
        msg="You are checked in! Please wait to be called."
    )

#====================================================
@app.route('/forgot', methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form.get('email')

        u = user()
        u.getByField('email', email)

        if len(u.data) == 0:
            return render_template("ok_dialog.html", msg="Email not found.")

        session['reset_uid'] = u.data[0]['uid']
        return redirect('/reset')

    return render_template('forgot.html')
#==========================================================================
@app.route('/reset', methods=['GET','POST'])
def reset():
    if 'reset_uid' not in session:
        return redirect('/login')

    u = user()
    u.getById(session['reset_uid'])

    if request.method == 'POST':
        pw1 = request.form.get('password')
        pw2 = request.form.get('password2')

        u.data[0]['password'] = pw1
        u.data[0]['password2'] = pw2

        if u.verify_update():
            u.update()
            del session['reset_uid']
            return render_template("ok_dialog.html", msg="Password updated. You may now log in.")
        else:
            return render_template("reset.html", obj=u)

    u.createBlank()
    return render_template("reset.html", obj=u)
#===========================================================================
@app.route("/dashboard")
def dashboard():
    if not checkSession():
        return redirect("/login")

    if session['user']['role'] not in ["doctor", "admin"]:
        return render_template("ok_dialog.html", msg="Access denied.")

    import matplotlib.pyplot as plt
    import os

    o = appointment()

    # Create analytics folder if missing
    analytics_folder = os.path.join("static", "analytics")
    if not os.path.exists(analytics_folder):
        os.makedirs(analytics_folder)

    # ----------------------------------------------------
    # DAILY APPOINTMENT CHART
    # ----------------------------------------------------
    daily = o.daily_appointment_count()
    days = [row['day'] for row in daily]
    totals = [row['total'] for row in daily]

    chart1_filename = "daily_appointments.png"
    chart1_path = os.path.join(analytics_folder, chart1_filename)

    plt.figure(figsize=(8,4))
    plt.bar(days, totals)
    plt.xticks(rotation=45)
    plt.title("Daily Appointment Count")
    plt.tight_layout()
    plt.savefig(chart1_path)
    plt.close()

    # ----------------------------------------------------
    # HOURLY APPOINTMENT CHART
    # ----------------------------------------------------
    hourly = o.hourly_appointment_distribution()
    hours = [row['hour'] for row in hourly]
    hour_totals = [row['total'] for row in hourly]

    chart2_filename = "hourly_distribution.png"
    chart2_path = os.path.join(analytics_folder, chart2_filename)

    plt.figure(figsize=(8,4))
    plt.bar(hours, hour_totals)
    plt.title("Hourly Appointment Distribution")
    plt.xlabel("Hour")
    plt.ylabel("Total Appointments")
    plt.tight_layout()
    plt.savefig(chart2_path)
    plt.close()

    # ----------------------------------------------------
    # TABLE DATA
    # ----------------------------------------------------
    doctor_volume = o.doctor_volume_last_30_days()
    checkin_rate = o.checkin_conversion_rate()
    checkin_rate = round(checkin_rate*100, 2) if checkin_rate else 0

    return render_template(
        "analytics/dashboard.html",
        daily_chart=chart1_filename,
        hourly_chart=chart2_filename,
        doctor_volume=doctor_volume,
        checkin_rate=checkin_rate
    )


#====================================================
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)



