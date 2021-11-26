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
    
  def command_get_bookings(card: str, userId: str) -> list:
    userId = str(userId)
    try:
      file_name = '../dynamic-config/booking.json'
      bookings = DynamicConfigReader.get_json(file_name)
      
      if userId in bookings['current'][card].keys():
        return bookings['current'][card][userId]
      else:
        return []
        
    except KeyError:
      raise ConfigNotFoundError(f"Cannot find {card} or {userId} in config.")
  
  def command_get_forfeits() -> list:
    try:
      file_name = '../dynamic-config/forfeit.json'
      return DynamicConfigReader.get_json(file_name)['forfeits']     
    except KeyError:
      raise ConfigNotFoundError(f"Cannot find forfeits in config.")
    