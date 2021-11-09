from io import TextIOWrapper
import os
import json

from exception.ConfigNotFound import ConfigNotFoundError

class ConfigReader:
  
  def getJson(fileName: str) -> TextIOWrapper:
    dirname = os.path.dirname(__file__)
    fullFileName = os.path.join(dirname, fileName)
    return open(fullFileName)

  def getToken() -> str:
    authF = ConfigReader.getJson('../config/auth.json')
    
    token = json.load(authF)['token']
    
    if not token:
      raise ConfigNotFoundError("Cannot find token.")
    else:
      return token
    
  def getStartupConfig(configName: str) -> str:
    configFile = ConfigReader.getJson('../config/startup.json')
    
    config = json.load(configFile)[configName]
    
    if not config:
      raise ConfigNotFoundError("Cannot find " + configName + ".")
    else:
      return config
    
  def getErrorMessage(messageName: str) -> str:
    errorMessages = ConfigReader.getJson('../config/error.json')
  
    errorMessage = json.load(errorMessages)['messages'][messageName]
    
    if not errorMessage:
      raise ConfigNotFoundError("Cannot find " + errorMessage + ".")
    else:
      return errorMessage
    