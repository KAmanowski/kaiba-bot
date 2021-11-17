from io import TextIOWrapper
import os
import json

from exception.ConfigNotFound import ConfigNotFoundError

class ConfigReader:
  
  def get_json(fileName: str) -> TextIOWrapper:
    dirname = os.path.dirname(__file__)
    fullFileName = os.path.join(dirname, fileName)
    file = open(fullFileName)
    
    config = json.load(file)
    file.close()
    
    return config

  def get_token() -> str:
    try:
      authF = ConfigReader.get_json('../config/auth.json')
      return authF['token']
    except KeyError:
      raise ConfigNotFoundError("Cannot find token.")
    
  def get_startup_config(configName: str) -> str:
    try:
      configFile = ConfigReader.get_json('../config/startup.json')
      return configFile[configName]
    except KeyError:
      raise ConfigNotFoundError("Cannot find " + configName + ".")
    
  def getErrorMessage(messageName: str) -> str:
    try:
      errorMessages = ConfigReader.get_json('../config/error.json')
      return errorMessages['messages'][messageName]
    except KeyError:
      raise ConfigNotFoundError("Cannot find " + messageName + ".")
  
    # returns channel id in a server
  def get_channel_id(server: str, channel: str) -> int:
    try:
      config = ConfigReader.get_json('../dynamic-config/server-channel-ids.json')
      channel_id = config[server][channel]
      
      return channel_id
    except KeyError:
      raise ConfigNotFoundError("Cannot find " + server + " or " + channel + " in config.")
    