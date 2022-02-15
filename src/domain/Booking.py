class Booking():
    
    def __init__(self, reason: str, reporter: str, time: float):
        self.reason = reason
        self.reporter = reporter
        self.time = time
        
    def to_json(self):
        obj = {}
        obj['reason'] = self.reason
        obj['reporter'] = self.reporter
        obj['time'] = self.time
        
        return obj