# Application Server
Shares keypair with authentication server.

Recieves access requests from client. Decrypts encrypted token in JSON response containing authentication token using keypair. This verifies that the token came from the authentication server.

### Expected client request body format:
```json
{
    "token": "<encrypted OAuth token>"
}
```