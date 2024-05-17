from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from utils import userUtils as userU
from utils import dbUtils as dbU
import uuid
import datetime
import requests
import json
import resend
import random
import time
import traceback
from bson import json_util

main = Blueprint('main', __name__)
random_user_picture = 'https://randomuser.me/api/?lego'

def getProfilePicture():
    res = requests.get(random_user_picture)
    return res.json()['results'][0]['picture']['large']

def setProfilePicture(username):
    user = dbU.manipulate.find_document('users', {'username': username})
    return user['profile_picture'] if user['profile_picture'] else "https://t4.ftcdn.net/jpg/04/10/43/77/360_F_410437733_hdq4Q3QOH9uwh0mcqAhRFzOKfrCR24Ta.jpg"
    

def newCode():
    return random.randint(100000, 999999)

def getActualTempCode(verificationCode):
    db = dbU.connectDB()
    user = dbU.manipulate.find_document('users', {'verificationCode': verificationCode})
    return user['temporaryCode']

def getIfUserVerified(verificationCode):
    db = dbU.connectDB()
    user = dbU.manipulate.find_document('users', {'verificationCode': verificationCode})
    return user['verified']

def getChatInfo(chat_id):
    user = dbU.manipulate.find_document('users', {'userid': session['user']})
    # Find the chat with the chat_id inside the user's contacts
    for contact in user['contacts']:
        if contact['chatid'] == chat_id:
            return contact
        
def getLastMessage():
    user = dbU.manipulate.find_document('users', {'userid': session['user']})
    last_messages = {}
    for contact in user['contacts']:
        chat_id = contact['chatid']
        last_messages[chat_id] = contact['messages'][-1] if contact['messages'] else None
    return last_messages

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/auth/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        if session.get('user'):
            return redirect(url_for('main.renderChatsPage'))
        else:
            return render_template('auth/login.html')
    elif (request.method == 'POST'):
        username = request.json['username']  # Suponiendo que tienes un campo de formulario 'username'
        password = request.json['password'] # Suponiendo que tienes un campo de formulario 'password'
        
        if username == 'admin' and password == 'admin':
            session['user'] = username
            return jsonify({'message': 'User logged in', 'status': 'success'})
        else:
            user = dbU.manipulate.find_document('users', {'username': username})
            pswd = user['password']
            if not user:
                return jsonify({'message': 'User not found', 'status': 'not_found'})
            elif pswd != password:
                return jsonify({'message': 'Incorrect password', 'status': 'incorrect_password'})
            else:
                session['user'] = user['userid']
                # Check if the session is not empty
                if session.get('user'):
                    return jsonify({'message': 'User logged in', 'status': 'success'})
                else:
                    return jsonify({'message': 'User not logged in', 'status': 'not_logged_in'})

@main.route('/auth/register', methods=['GET', 'POST'])
def register():
    if (request.method == 'GET'):
        return render_template('auth/register.html')
    elif (request.method == 'POST'):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        repeatPassword = request.json['passwordRepeat']
        
        if password != repeatPassword:
            return jsonify({'message': 'Passwords do not match', 'status': 'passwords_not_match'})
        else:
            db = dbU.connectDB()
            if db == None:
                return jsonify({'message': 'Database connection error', 'status': 'db_connection_error'})
            elif dbU.manipulate.find_document('users', {'username': username}):
                return jsonify({'message': 'Username already exists', 'status': 'username_exists'})
            elif dbU.manipulate.find_document('users', {'email': email}):
                return jsonify({'message': 'Email already exists', 'status': 'email_exists'})
            else:
                data = {
                    'userid': uuid.uuid4().hex,
                    'username': username,
                    'email': email,
                    'password': password,
                    'verified': False,
                    'verificationCode': uuid.uuid4().hex,
                    'role': 'user',
                    'account_type': 'free',
                    'contacts': [],
                    'profile_picture': str(getProfilePicture()),
                    'created_at': str(datetime.datetime.now()),
                    'updated_at': str(datetime.datetime.now())
                }
                # Insert the user into the database
                dbU.manipulate.insert_document('users', data)
                # Generate a session with the userid
                session['user'] = data['userid']
                json_user_data = json.dumps(data, default=json_util.default)
                print("User data: ", json_user_data)
                return jsonify({'message': 'User registered', 'status': 'success', 'user': json_user_data})
        
@main.route('/auth/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
    if (request.method == 'GET'):
        return render_template('auth/forgot-password.html')
    elif (request.method == 'POST'):
        email = request.json['email']
        db = dbU.connectDB()
        user = dbU.manipulate.find_document('users', {'email': email})
        if not user:
            return jsonify({'message': 'User not found', 'status': 'not_found'})
        else:
            return jsonify({'message': 'User found', 'status': 'found'})       
    
@main.route('/auth/verify-account', methods=['GET', 'POST'])
def verifyAccount():
    verifCode = request.args.get('code')
    if not verifCode or verifCode == None:
        return "Verification code not found"
    else:
        if (request.method == 'GET'):
            # Check if the verification code is valid
            db = dbU.connectDB()
            user = dbU.manipulate.find_document('users', {'verificationCode': verifCode})
            if not user:
                return jsonify({'message': 'Verification code not found', 'status': 'not_found'})
            if getIfUserVerified(verifCode) == 'true':
                return redirect(url_for('main.home'))
            else:
                # Update the users document with a new field adding a 6 digit verification code (534-543)
                dbU.manipulate.insert_field('users', {'verificationCode': verifCode}, {'temporaryCode': str(newCode())})
                # Send the verification code to the user's email
                # ...
                # Now get the user temporary code
                time.sleep(5)
                userCode = getActualTempCode(verifCode)
                return render_template('auth/verify-account.html', code=userCode)
            
@main.route('/api/accountVerification', methods=['POST'])
def accountVerification():
    try:
        if (request.method == 'POST'):
            print("POST REQUEST RECEIVED BY THE SERVER: \n", str(request.json))
            code = request.json['code']

            if not code:
                return jsonify({'message': 'Missing code or verification code', 'status': 'error'})

            if code:
                db = dbU.connectDB()
                dbU.manipulate.update_field('users', {'temporaryCode': code}, {'verified': True})
                dbU.manipulate.delete_field('users', {'temporaryCode': code}, 'temporaryCode')
                return jsonify({'message': 'Account verified', 'status': 'success'})
            else:
                return jsonify({'message': 'Incorrect code', 'status': 'incorrect_code'})
    except Exception as e:
        print("Error occurred: ", str(e))
        print(traceback.format_exc())
        return jsonify({'message': 'An error occurred', 'status': 'error'})
        
@main.route('/chats/<chat_id>')
def renderChatPage(chat_id):
    # Check if a session cookie is avaliable.
    if session.get('user'):
        user = dbU.manipulate.find_document('users', {'userid': session['user']})
        # Hide fields that are not needed
        user.pop('password')
        print("User: ", json.dumps(user, default=json_util.default, indent=4))
        if chat_id:
            # Find the correct contact based on the chat_id
            contact = next((contact for contact in user['contacts'] if contact['chatid'] == chat_id), None)
            contact_user = dbU.manipulate.find_document('users', {'username': contact['username']})
            if contact:
                return render_template('chats.html', currentUser=user, chat_id=chat_id, contact_pic=contact_user['profile_picture'], profile_picture=setProfilePicture, chat_data=getChatInfo(chat_id), last_message=getLastMessage())
            else:
                return "Contacto no encontrado", 404
    else:
        return redirect(url_for('main.login'))

@main.route('/chats')
def renderChatsPage():
    # Check if a session cookie is avaliable.
    if session.get('user'):
        user = dbU.manipulate.find_document('users', {'userid': session['user']})
        user.pop('password')
        if not user:
            return jsonify({'message': 'User not found', 'status': 'not_found'})
        else:
            print("Last message: ", getLastMessage())
            return render_template('chats.html', currentUser=user, profile_picture=setProfilePicture, chat_data=getChatInfo, last_message=getLastMessage())
    else:
        return redirect(url_for('main.login'))

@main.route('/api/sendMessage/<chat_id>', methods=['POST'])
def sendMessage(chat_id):
    if (request.method == 'POST'):
        message = request.json['message']
        if not message:
            return jsonify({'message': 'Message not found', 'status': 'not_found'})
        else:
            user = dbU.manipulate.find_document('users', {'userid': session['user']})
            chatinf = getChatInfo(chat_id)
            print("Last message: ", getLastMessage())
            dbU.chatUtils.createMessage(userid=user['userid'], chatid=chat_id, message=message, sender=user['username'], receiver=chatinf['username'])
            return jsonify({'message': 'Message sent', 'status': 'success'})
    
@main.route('/auth/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.home'))

@main.route('/api/getMessages/<chat_id>')
def getMessages(chat_id):
    user = dbU.manipulate.find_document('users', {'userid': session['user']})
    chatinf = getChatInfo(chat_id)
    messages = chatinf['messages']
    return jsonify({'messages': messages, 'status': 'success'})