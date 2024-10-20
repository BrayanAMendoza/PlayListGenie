import requests
import base64


#Add your:  client id and Private client secret
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET' 
client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}" #Estblishing credentials to client_creds

#encoding/securing the client credentials 
client_cred_base64 = base64.b64encode(client_creds.encode())


#requesting access token 
token_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {client_cred_base64.decode()}' #passing the decoded authorized tokens
}

data = {
    'grant_type':'client_credentials'
}

response = requests.post(token_url, data = data, headers= headers)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print("Successfully obtained Access token")

else:
    print("Error in obtaining the access token")
    exit()

    

