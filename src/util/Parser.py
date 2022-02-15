
class Parser():
  
  # if return is 0 - not valid
  def parseUserId(userId: str) -> int:
    try:
      return int(userId)
    except:
      try:
        givenUserId = str(userId)[3:-1]
        return int(givenUserId)
      except:
        return 0