import requests
from exception.BadInputException import BadInputException

from exception.MerlinErrorException import MerlinErrorException

class Merlin():
  
  baseUrl: str = "http://192.168.1.3:7331/"
  
  # Merlin return example:
  # {
  #     "valheim": {
  #         "online": true,
  #         "credentials": {
  #             "ip": "86.175.7.127:2456",
  #             "password": "davinky "
  #         }
  #     }
  # }
  def get_all_server_status():
    url = Merlin.baseUrl + "/server"
    
    res = requests.get(url=url, timeout=10)
    
    if (res.status_code != 200):
      raise MerlinErrorException("Merlin is unavailable.")
    
    return res.json()
  
  def server_command(server: str, command: str):
    url = Merlin.baseUrl + "/server?command=" + command + "&name=" + server
    
    res = requests.post(url=url, timeout=10)
    
    if res.status_code == 400:
      print("not found")
      raise BadInputException(res.json()['reason'])
    if res.status_code != 200:
      raise MerlinErrorException("Merlin is unavailable.")
    
    return res.json()
      