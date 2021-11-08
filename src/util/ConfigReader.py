import os
import json

from exception.ConfigNotFound import ConfigNotFoundError

def getToken() -> str:
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, './config/json/auth.json')
  authF = open(filename,)
  
  token = json.load(authF)['token']
  
  if not token:
    raise ConfigNotFoundError("Cannot find token.")
  else:
    return token