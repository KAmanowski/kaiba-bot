import logging
import requests
from exception.BadInputException import BadInputException

from exception.MerlinErrorException import MerlinErrorException
from exception.ServerNotKillableException import ServerNotKillableException
from util.ConfigReader import ConfigReader
from util.IPGrabber import IPGrabber

class Merlin():
  
  def __init__(self, devMode: bool):
    self.baseUrl = ""
    self.lostConnection = False
    self.port = (7332 if devMode else 7331)
    self.rebuild_url()
    
  def rebuild_url(self):
    self.baseUrl = f"http://{ConfigReader.get_startup_config('merlin-ip')}:{self.port}/"
    logging.warning(f"Rebuilding Merlin IP to {self.baseUrl}")
    
  def error_handle(self, e: Exception):
    self.rebuild_url()
    self.lostConnection = True
    raise MerlinErrorException("Merlin timed out/could not connect.", e)
  
  def log_reconnect(self):
    if self.lostConnection:
      self.lostConnection = False
      logging.info("Reconnected with Merlin.")
 
  def get_all_server_status(self):
    # Merlin return example:
    # {
    #   "external-ip": "1.2.3.344.3",
    #   "servers": [
    #     "valheim": {
    #         "online": true,
    #         "credentials": {
    #             "port": "port",
    #             "password": "password"
    #         }
    #     }
    #   ]
    # }
    
    url = self.baseUrl + "/server"
    
    try:
      res = requests.get(url=url, timeout=10)
    except Exception as e:
      self.error_handle(e)
      
    if (res.status_code != 200):
      raise MerlinErrorException(f"Merlin is unavailable. Status code: {str(res.status_code)}, JSON: {str(res.json())}")
    
    self.log_reconnect()
    return res.json()
  
  def server_command(self, server: str, command: str):
    url = self.baseUrl + "/server?command=" + command + "&name=" + server
    try:
      res = requests.post(url=url, timeout=(70 if command == 'kill' else 10))
    except Exception as e:
      self.error_handle(e)
    
    if res.status_code == 400:
      raise BadInputException(res.json()['reason'])
    if command == "kill" and res.status_code == 501:
        raise ServerNotKillableException(f"Server {server} needs to be killed manually.")
    if res.status_code != 200:
      raise MerlinErrorException(f"Merlin is unavailable. Status code: {str(res.status_code)}, JSON: {str(res.json())}")
    
    self.log_reconnect()
    return res.json()
      