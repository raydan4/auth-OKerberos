# Authentication Server
Recieves authentication request from client, validates the requests with OAuth Provider, and returns a JSON response with the resulting status and token.

### Success
```json
{
    "auth": "success",
    "token": "<encrypted OAUTH token>"
}
```

### Failure
```json
{
    "auth": "failure",
    "token": ""
}
```

Tokens are encrypted with using a keypair shared with the application server.

Responses sent back to the client will be encrypted with the SHA256 hash of the client's password.