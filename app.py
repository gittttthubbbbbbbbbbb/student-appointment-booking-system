from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

users = {}
appointments = []
admin_credentials = {'admin': 'admin123'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('error.html', message="Username already exists.")
        users[username] = password
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('dashboard', user=username))
        else:
            return render_template('error.html', message="Invalid username or password.")
    return render_template('login.html')

@app.route('/dashboard/<user>', methods=['GET', 'POST'])
def dashboard(user):
    if request.method == 'POST':
        datetime_str = request.form['datetime']
        purpose = request.form['purpose']
        try:
            slot = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return render_template('error.html', message="Invalid date and time format.")
        for appt in appointments:
            if appt['slot'] == slot:
                return render_template('error.html', message="Slot already booked.")
        appointments.append({'user': user, 'slot': slot, 'status': 'Pending','purpose' : purpose})
        return render_template('appointment_success.html', user=user, slot=slot, purpose=purpose)
    return render_template('dashboard.html', user=user)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if admin_credentials.get(username) == password:
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('error.html', message="Invalid admin credentials.")
    return render_template('admin_login.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        action = request.form['action']
        index = int(request.form['index'])
        if 0 <= index < len(appointments):
            if action == 'accept':
                appointments[index]['status'] = 'Accepted'
            elif action == 'reject':
                appointments[index]['status'] = 'Rejected'
    return render_template('admin_dashboard.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)