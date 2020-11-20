from flask import Flask, render_template, json, request
import requests, logging, base64
from Crypto.Hash import SHA256
from crypt import aes256_decrypt


app = Flask(__name__)

# Configurations
authServer = 'https://verify.silentnoise.fail/token'
appServer = 'https://auth-app.silentnoise.fail'

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
        blob = { "username": username, "password": password }
        response = requests.post(authServer, json=blob, headers={"Content-Type": "application/json"})
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
        print(decrypted_response)
        # Send authorized request to applicaiton server if things are good
        content = requests.post(appServer, json=decrypted_response, headers={"Content-Type":"application/json"})
        print("** Token was sent to appServer **") 

        req = json.loads(content.text)
        auth = req["message"] == "AUTHORIZED"
        return render_template("auth.html", auth=auth, data=content.text)

if __name__ == "__main__":
    app.run()
    
    
    
    
    
    
    
    
    
