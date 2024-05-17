import pymongo
import dotenv
import os
import sys
import simple_term_menu as stm
import datetime
import survey
import colorama as cl
import time
import requests

dotenv.load_dotenv()

class _utils_:
    def __init__(self) -> None:
        self.db_uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("MONGODB_DB")
        self.client = pymongo.MongoClient(self.db_uri, document_class=dict, tz_aware=False, connect=True)
    
    def getUsers(self):
        database = self.client['webchat-app']
        users_collection = database['users']
        users = users_collection.find()
        usernames = [user['username'] for user in users]
        return usernames
    
    def _getProfilePicture(self):
        # Get a random profile picture from the API
        response = requests.get("https://randomuser.me/api/?lego")
        data = response.json()
        picture = data['results'][0]['picture']['large']
        return str(picture)
    
    def createContact(self, username: str, add_to: str = None):
        database = self.client['webchat-app']
        contacts_collection = database['users']
        contact_schema = {
            "username": username,
            "chatid": os.urandom(16).hex(),
            "messages": [],
            "last_message": None,
            "status": "offline",
            "is_blocked": False,
            "is_muted": False,
            "is_favourite": False,
            "is_archived": False,
            "is_pinned": False,
            "is_group": False,
            "last_time_online": "Never",
            "created_at": str(datetime.datetime.now()),
            "updated_at": str(datetime.datetime.now())
        }
        contacts_collection.update_one({"username": add_to}, {"$push": {"contacts": contact_schema}}, upsert=True)
        # If the contact is created, return the chatid
        print(f"Contact created with chatid: {contact_schema['chatid']}")
        return contact_schema['chatid']
    
    def createUser(self, username: str, email: str, password: str, repeatPassword: str, profile_picture: str = ""):
        database = self.client['webchat-app']
        users_collection = database['users']
        data = {
            'userid': os.urandom(16).hex(),
            'username': username,
            'email': email,
            'password': password,
            'verified': True,
            'verificationCode': os.urandom(16).hex(),
            'contacts': [],
            'profile_picture': self._getProfilePicture(),
            'created_at': str(datetime.datetime.now()),
            'updated_at': str(datetime.datetime.now())
        }
        if password != repeatPassword:
            print("Passwords do not match!")
            return False
        else:
            if users_collection.find_one({"username": username}):
                print("Username already exists!")
                return False
            elif users_collection.find_one({"email": email}):
                print("Email already exists!")
                return False
            else:
                data['username'] = username
                data['email'] = email
                data['password'] = password
                users_collection.insert_one(data)
                print("User registered successfully!")
                return True

    def createMessage(self, userid: str, chatid: str, message: str, sender: str, receiver: str = None):
        database = self.client['webchat-app']
        users_collection = database['users']
        message_schema = {
            "message": message,
            "sender": sender,
            "receiver": receiver,
            "created_at": str(datetime.datetime.now())
        }

        user = users_collection.find_one({"userid": userid})
        if user:
            for index, contact in enumerate(user['contacts']):
                if contact['chatid'] == chatid:
                    users_collection.update_one(
                        {"userid": userid},
                        {"$push": {f"contacts.{index}.messages": message_schema}}
                    )
                    users_collection.update_one(
                        {"username": receiver},
                        {"$push": {f"contacts.{index}.messages": message_schema}}
                    )
            print("Message sent successfully!")
            return True
        else:
            print("User not found!")
            return False
    
    def retriveContactsFromUser(self, username: str):
        database = self.client['webchat-app']
        users_collection = database['users']
        user = users_collection.find_one({"username": username})
        contacts = user['contacts']
        return contacts
    
    def getUserId(self, username: str):
        database = self.client['webchat-app']
        users_collection = database['users']
        user = users_collection.find_one({"username": username})
        return user['userid']
class core:
    def __init__(self) -> None:
        self.db_uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("MONGODB_DB")
        self.utils = _utils_()
    
    def execute_add_contact(self):
        os.system("clear")
        username = self.utils.getUsers()
        menu = stm.TerminalMenu(username, title="Select a user to add a contact to!", menu_cursor='❯ ', menu_cursor_style=('fg_red', 'bold'), menu_highlight_style=('fg_yellow', 'bold'))
        menu_index = menu.show()
        if username[menu_index] == username[menu_index]:
            # Now we need to propmt the user to search for the user they want to add
            username_search = survey.routines.select("Enter the username you want to add as a contact: ", options=username)
            if username[username_search] == username[menu_index]:
                print("You cannot add yourself as a contact!")
            else:
                print(f"Adding {cl.Fore.LIGHTYELLOW_EX}{cl.Style.BRIGHT}{username[username_search]}{cl.Fore.RESET} to {cl.Fore.CYAN}{cl.Style.BRIGHT}{username[menu_index]}{cl.Fore.RESET} contacts!")
                time.sleep(3)
                self.utils.createContact(username=str(username[username_search]), add_to=str(username[menu_index]))
        else:
            print("An error occured while adding the contact!")
            sys.exit(1)
            
    def execute_register_user(self):
        os.system("clear")
        print("Register a new user!")
        print("-" * 20)
        time.sleep(2)
        username = survey.routines.input("Enter your username: ")
        email = survey.routines.input("Enter your email: ")
        password = survey.routines.conceal("Enter your password: ")
        repeatPassword = survey.routines.conceal("Repeat your password: ")
        time.sleep(2)
        print(f"Creating user with username: {username}, email: {email}, password: {password}, repeatPassword: {repeatPassword}")
        time.sleep(2)
        self.utils.createUser(username=username, email=email, password=password, repeatPassword=repeatPassword)
        
        
    def execute_create_message(self):
        os.system("clear")
        print("Create a new message!")
        print("-" * 21)
        time.sleep(2)
        # Select the user to be the sender
        username = self.utils.getUsers()
        username_search = survey.routines.select("Select the user to be the sender: ", options=username)
        # Select the contact to send the message to
        # Check if the user has contacts
        contacts = self.utils.retriveContactsFromUser(username=username[username_search])
        if not contacts:
            print("You do not have any contacts to send messages to!")
            sys.exit(1)
        else:
            contacts_list = [contact['username'] for contact in contacts]
            contact_search = survey.routines.select("Select the contact to send the message to: ", options=contacts_list)
        # Get the message to send\
        message = survey.routines.input("Enter the message: ")
        # Get the sender
        sender = username[username_search]
        chatid = contacts[contact_search]['chatid']
        time.sleep(2)
        print(f"Creating message from {username[username_search]} to: {contacts_list[contact_search]}, chatid: {chatid}, message: {message}, sender: {sender}")
        time.sleep(2)
        self.utils.createMessage(userid=self.utils.getUserId(username=username[username_search]), chatid=chatid, message=message, sender=sender, receiver=contacts_list[contact_search])