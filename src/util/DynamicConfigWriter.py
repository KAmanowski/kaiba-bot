import os
import json
from exception.ConfigNotFound import ConfigNotFoundError

class DynamicConfigWriter:
  
  def get_json(file_name: str) -> any:
    dirname = os.path.dirname(__file__)
    full_file_name = os.path.join(dirname, file_name)
    file = open(full_file_name)
    
    config = json.load(file)
    file.close()
    
    return config
  
  def save_json(file_name: str, json_obj: any):
    dirname = os.path.dirname(__file__)
    full_file_name = os.path.join(dirname, file_name)
    
    file = open(full_file_name, 'w')
    file.write(json.dumps(json_obj, indent=2))
    file.close()
    
  # def lock_write_command(command: str, locked: bool):
  #   try:
  #     file_name = '../dynamic-config/lock.json'
  #     config = DynamicConfigWriter.get_json(file_name)
  #     config['commands'][command] = locked
  #     DynamicConfigWriter.save_json(file_name, config)
  #   except KeyError:
  #     raise ConfigNotFoundError("Cannot find " + command + " lock in config.")
    
  def task_write_message_id(task_name: str, message_id: int):
    try:
      file_name = '../dynamic-config/task.json'
      config = DynamicConfigWriter.get_json(file_name)
      config[task_name]['message_id'] = message_id
      DynamicConfigWriter.save_json(file_name, config)
    except KeyError:
      raise ConfigNotFoundError("Cannot find " + task_name + " in config.")

    