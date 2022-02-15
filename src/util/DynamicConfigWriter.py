import os
import json

from discord import user
from domain.Booking import Booking
from exception.ConfigNotFound import ConfigNotFoundError

class DynamicConfigWriter():
  
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
      raise ConfigNotFoundError(f"Cannot find {task_name} in config.")
    
  def command_book(card: str, userId: str, booking: Booking):
    userId = str(userId)
    try:
      file_name = '../dynamic-config/booking.json'
      bookings = DynamicConfigWriter.get_json(file_name)
      
      if userId in bookings['current'][card].keys():
        userBookList: list = bookings['current'][card][userId]
        userBookList.append(booking.to_json())
        bookings['current'][card][userId] = userBookList
      else:
        bookings['current'][card][userId] = [booking.to_json()]
        
      DynamicConfigWriter.save_json(file_name, bookings)
    except KeyError:
      raise ConfigNotFoundError(f"Cannot find {card} or {userId} in config.")
    
  def task_migrate_bookings_to_history(card: str):
    try:
      file_name = '../dynamic-config/booking.json'
      bookings = DynamicConfigWriter.get_json(file_name)
      
      for userId in bookings['current'][card]:
        if not (userId in bookings['history'][card].keys()):
          bookings['history'][card][userId] = []
          
        for x in range(len(bookings['current'][card][userId])):
          bookings['history'][card][userId].append(bookings['current'][card][userId][x])
          
      bookings['current'][card] = {}  
        
      DynamicConfigWriter.save_json(file_name, bookings)
    except KeyError:
      raise ConfigNotFoundError(f"Cannot find {card} in config.")