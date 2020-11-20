from flask import Flask, render_template, json, request
import requests, logging, base64
from Crypto.Hash import SHA256
from crypt import aes256_decrypt


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
    username = request.form['inputName']
    password = request.form['inputPassword']

    # validate the received values
    if username and password:
        # Send user/pass to server
        userpass = { "username": username, "password": password }
        response = requests.post(authServer, data = userpass)
        print("** Credentials were sent to authServer **")

        # Get request from AuthServer
        encoded_response = response.text
        # Decode Response
        encrypted_response = base64.b64decode(encoded_response)
        # Decrypt Response
        h = SHA256.new()
        h.update(password.encode('utf-8'))
        hashed_password = h.digest()
        decrypted_response = aes256_decrypt(encrypted_response, hashed_password)
        # Send authorized request to applicaiton server if things are good
        content = requests.post(appServer, json=decrypted_response, headers={"Content-Type":"application/json"})
        print("** Token was sent to appServer **") 

        req = json.loads(content.text)
        if req["message"] == "AUTHORIZED":
            data = """
            <div class="jumbotron" style="background-color: #77dd77;">
            <h1>OAuth SUCCESS!</h1>
            <p class="lead"></p>
            <p>You have been granted access to the application</p>
            <code>{"message":"AUTHORIZED","status":200}</code>
            </div>
            """
            return render_template("auth.html", data=data)
        elif req["message"] == "UNAUTHORIZED":
            data = """
            <div class="jumbotron" style="background-color: #ff6961;">
            <h1>OAuth FAILURE</h1>
            <p class="lead"></p>
            <p>You have been denied access to the application</p>
            <code>{"message":"UNAUTHORIZED","status":403}</code>
            </div>
            """
            return render_template("auth.html", data=data)

if __name__ == "__main__":
    app.run()
    
    
    
    
    
    
    
    
    
