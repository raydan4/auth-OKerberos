# auth-OKerberos
Simple authencication protocol implementation with a client, an authentication server, an OAuth server, and an application server.


## OKerberos Client
Client application which will make authentication requests to an authentication server so that it can gain access to the application server's content.

## OKerberos Authentication Server
Receives authentication requests, validates them with the OAuth Provider, and returns an encrypted success or failure response to the client.

## OAuth Provider
Checks credentials against a database for validity.

## OAuth Enabled Application Server
Allows client to access content if properly authenticated by authentication server.