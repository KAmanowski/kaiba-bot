from io import TextIOWrapper
import os
import json

from exception.ConfigNotFound import ConfigNotFoundError

class DynamicConfigReader:
  
  def get_json(fileName: str) -> any:
    dirname = os.path.dirname(__file__)
    fullFileName = os.path.join(dirname, fileName)
    file = open(fullFileName)
    
    config = json.load(file)
    file.close()
    
    return config
    
  def task_get_channel_id(taskName: str) -> str:
    try:
      config = DynamicConfigReader.get_json('../dynamic-config/task.json')
      channel_id = config[taskName]['channel_id']
      
      return channel_id
    except KeyError:
      raise ConfigNotFoundError("Cannot find " + taskName + " in config.")
    
  def task_get_message_id(taskName: str) -> str:
    try:
      config = DynamicConfigReader.get_json('../dynamic-config/task.json')
      message_id = config[taskName]['message_id']
      
      return message_id
    except KeyError:
      raise ConfigNotFoundError("Cannot find " + taskName + " in config.")
    