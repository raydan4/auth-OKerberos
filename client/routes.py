from flask import Flask, render_template, json, request
import requests, logging, base64

app = Flask(__name__)

# Configurations
authServer = 'http://192.168.1.1'
appServer = 'http://192.168.1.1'

@app.route("/")
def main():
    return render_template('index.html')
    
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
    
    
@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _password:
        # Send user/pass to server
        userpass = { "username": _name, "password": _password }
        x = requests.post(authServer, data = userpass)
        print("** Credentials were sent to authServer **")
        return userpass # Show in console
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'}) 

@app.route("/gettoken", methods=['POST','GET'])
def receiveToken():
    # Get request from AuthServer
    _encoded_response = request.body
    # Decode Response
    encrypted_response = base64.b64decode(encoded_response)
    # Decrypt Response
    hashed_password = SHA256(password) #TODO: Where is the password coming from??? Do I need to save it?
    response = aes256_decrypt(encrypted_response, hashed_password)
    # Get JSON object
    json_blob = json.loads(response)
    # Send Access Request to Application Server (this should be just the JSON you get from the auth server)
    x = requests.post(appServer, data = json_blob)
    print("** Token was sent to appServer **")    
    
@app.route("/getauth", methods=['POST','GET'])
def getAuth():
    req = request.get_json()
    if req == '{"message":"AUTHORIZED","status":200}':
        data = """
        <div class="jumbotron" style="background-color: #00ff00;">
        <h1>OAuth SUCCESS!</h1>
        <p class="lead"></p>
        <p>You have been granted access to the application</p>
        <code>{"message":"AUTHORIZED","status":200}</code>
        </div>
        """
        return render_template("auth.html", data=data)
    elif req == '{"message":"UNAUTHORIZED","status":403}':
        data = """
        <div class="jumbotron" style="background-color: #ff3333;">
        <h1>OAuth FAILURE</h1>
        <p class="lead"></p>
        <p>You have been denied access to the application</p>
        <code>{"message":"UNAUTHORIZED","status":403}</code>
        </div>
        """
        return render_template("auth.html", data=data)
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
	app.run()
	
	
	
	
	
	
	
	
	
