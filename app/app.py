from flask import Flask
import time
import os
import atexit
from flask_socketio import SocketIO

banner = r"""
_______ _______  ______ _    _ _______  ______         
|______ |______ |_____/  \  /  |______ |_____/         
______| |______ |    \_   \/   |______ |    \_                       
                    ++                 
                 ++++++++              
              ++++++++++++++           
          ++++++++++++++++++++++       
       ++++++++++++++++++++++####      
       #++++++++++++++++++#######      
       #+++++++++++++++##########      
       #++++#+++++++#############      
       #++#++++++################      
       #+++++##++################      
       #+#++#++++################      
       #++-++++++################      
       #+++++--++################      
       #++++-++++################      
       #+++-+++++################      
       #++-+++-++###############       
       #++#+--+++###############       
       ##++#+++++############          
          ##++#++#########             
             ###+#####                 
                 ##                    
______________________________________________________
"""

app = Flask(__name__)
socketio = SocketIO(app)

from routes import main

app.register_blueprint(main)
app.secret_key = os.urandom(24)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=3000, debug=True)