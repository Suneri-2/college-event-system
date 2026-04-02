from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Event, Registration, Notification, Announcement
import os

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE PATH
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "college_system.db")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect(url_for('register'))

# ---------------- AUTH ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            role=request.form['role']
        )
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully!")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            email=request.form['email'],
            password=request.form['password'],
            role=request.form['role']
        ).first()

        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role

            if user.role == 'admin':
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid login")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- ADMIN ----------------
@app.route('/admin/home')
def admin_home():
    return render_template("admin_home.html",
        events=Event.query.all(),
        users=User.query.filter_by(role='student').all(),
        notifications=Notification.query.all(),
        announcements=Announcement.query.all()
    )

@app.route('/admin/events', methods=['GET','POST'])
def admin_events():
    if request.method == 'POST':
        e = Event(
            title=request.form['title'],
            date=request.form['date'],
            time=request.form['time'],
            venue=request.form['venue'],
            description=request.form['description']
        )
        db.session.add(e)
        db.session.commit()
        return redirect(url_for('admin_events'))

    return render_template("admin_events.html", events=Event.query.all(), event_to_update=None)

@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    e = Event.query.get(event_id)
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for('admin_events'))

@app.route('/update_event/<int:event_id>', methods=['GET','POST'])
def update_event(event_id):
    event = Event.query.get(event_id)

    if request.method == 'POST':
        event.title = request.form['title']
        event.date = request.form['date']
        event.time = request.form['time']
        event.venue = request.form['venue']
        event.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin_events'))

    return render_template("admin_events.html",
        events=Event.query.all(),
        event_to_update=event)

@app.route('/admin/notifications', methods=['GET','POST'])
def admin_notifications():
    if request.method == 'POST':
        n = Notification(
            title=request.form['title'],
            message=request.form['message']
        )
        db.session.add(n)
        db.session.commit()
    return render_template("admin_notifications.html",
        notifications=Notification.query.all())

@app.route('/delete/notification/<int:notification_id>')
def delete_notification(notification_id):
    n = Notification.query.get(notification_id)
    db.session.delete(n)
    db.session.commit()
    return redirect(url_for('admin_notifications'))

@app.route('/admin/announcements', methods=['GET','POST'])
def admin_announcements():
    if request.method == 'POST':
        a = Announcement(
            title=request.form['title'],
            message=request.form['message']
        )
        db.session.add(a)
        db.session.commit()
    return render_template("admin_announcements.html",
        announcements=Announcement.query.all())

@app.route('/admin/participants')
def admin_participants():
    return render_template("admin_participants.html",
        registrations=Registration.query.all(),
        students=User.query.all(),
        events=Event.query.all())

@app.route('/admin/reports')
def admin_reports():
    return render_template("admin_reports.html",
        registrations=Registration.query.all(),
        students=User.query.all(),
        events=Event.query.all())

# ---------------- STUDENT ----------------
@app.route('/student/dashboard')
def student_dashboard():
    return render_template("student_dashboard.html",
        events=Event.query.all(),
        notifications=Notification.query.all(),
        announcements=Announcement.query.all())

@app.route('/student/events')
def student_events():
    return render_template("student_events.html",
        events=Event.query.all())

@app.route('/register_event/<int:event_id>', methods=['GET','POST'])
def register_event(event_id):
    event = Event.query.get(event_id)   # only for display

    if request.method == 'POST':
        student_name = request.form.get('student_name')
        semester = request.form.get('semester')
        roll_no = request.form.get('roll_no')

        print(student_name, semester, roll_no)

        # ✅ NO event_id stored
        reg = Registration(
            student_name=student_name,
            semester=semester,
            roll_no=roll_no
        )

        db.session.add(reg)
        db.session.commit()

        flash("✅ Registration Successful!")
    return render_template("student_register.html", event=event)

    return render_template("student_register.html", event=event)


@app.route('/student/notifications')
def student_notifications():
    return render_template("student_notifications.html",
        notifications=Notification.query.all())

@app.route('/student/announcements')
def student_announcements():
    return render_template("student_announcements.html",
        announcements=Announcement.query.all())

@app.route('/student/reports')
def student_reports():
    return render_template("student_reports.html",
        registrations=Registration.query.all(),
        events=Event.query.all())

# ---------------- RUN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)