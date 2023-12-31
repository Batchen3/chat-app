from curses import flash
from flask import Flask, render_template, request, redirect, session
import csv
import os
import base64
import datetime



#----------------------------------------------------------------------------
# Init
#----------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = 'chat@secret'  # Set a secret key for session management
if not os.path.exists('rooms'):
    os.makedirs("rooms")

    
#------------------------------------------------------------------------------
# Helper functions
#-----------------------------------------------------------------------------

#  For user authentication
def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decode_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password.encode('utf-8'))
    return decoded_bytes.decode('utf-8')

def check_user_credentials(username, password):
    with open(os.getenv("CSV_PATH"), 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == username:
                if decode_password(row[1]) != password:
                     return "user with that name already exist"
                else:
                     return "you already registered, please login"
    return False

def add_user_to_csv(username, encoded_password):
    # Save user details to the CSV file
    with open(os.getenv("CSV_PATH"), 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, encoded_password])

#  For creating new room
def valid_room_name(new_room_name):
    rooms = os.listdir(os.getenv('ROOMS_FILES_PATH'))
    for room in rooms:
        if room == f'{new_room_name}.txt':
            return False
    return True

#-----------------------------------------------------------------------------
# Routes
#-----------------------------------------------------------------------------
@app.route('/')
def index():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        encoded_password = encode_password(password)
        ans = check_user_credentials(username, password)
        if not ans:
            add_user_to_csv(username, encoded_password)
            return redirect('/login')
        else:
            return ans
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if check_user_credentials(username, password) == "you already registered, please login":
            session['username'] = username
            return redirect('/lobby')
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')



@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if 'username' in session:
        if request.method == 'POST':
            room_name = request.form['new_room']
            if valid_room_name(room_name):  
                # Checking if the room name is unique 
                path=os.getenv('ROOMS_FILES_PATH')+room_name+".txt"
                room =  open(path, 'w')  
            else:
                return "Oops... There is already exist room named "+room_name+" Please try another name"
        rooms = os.listdir(os.getenv('ROOMS_FILES_PATH'))
        new_rooms = [x[:-4] for x in rooms]
        return render_template('lobby.html', all_rooms=new_rooms)
    else:
        return redirect('/login')

@app.route('/chat/<room>', methods=['GET', 'POST'])
def chat(room):
    if 'username' in session:
        return render_template('chat.html', room=room)
    else:
        return redirect('/login')
    

@app.route('/api/chat/<room>', methods=['GET','POST'])
def update_chat(room):
    path=os.getenv('ROOMS_FILES_PATH')+room+".txt"
    if request.method == 'POST':
        message = request.form['msg']
        username = session['username']
        ist_offset = datetime.timedelta(hours=3)
        utc_time = datetime.datetime.utcnow()
        local_time = utc_time + ist_offset
        timestamp = local_time.strftime("%Y-%m-%d %H:%M:%S")
        # Append the message to the room's unique .txt file
        with open(path, 'a', newline='') as file:
            file.write(f'[{timestamp}] {username}: {message}\n')
            
    with open(path, 'r' ) as file:
        file.seek(0)
        lines = file.read()
    return lines


@app.route('/api/chat/<room>/clear', methods=['POST'])
def clear_chat(room):
    name_to_remove= session['username']
    path=os.getenv('ROOMS_FILES_PATH')+room+".txt"
    with open(path, 'r') as f:
        lines = f.readlines()

    with open(path, 'w') as f:
        for line in lines:
            if name_to_remove not in line:
                f.write(line) 

@app.route("/health")
def health():
    return "OK", 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

