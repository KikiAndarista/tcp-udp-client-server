import Pyro4

@Pyro4.expose
class SendMsg(object):
    def __init__(self):
        self.last_msg = {}

    def send(self, name, msg):
        print(name, msg)
        self.last_msg.update({"from":name,"msg":msg})
        return True
    def get(self):
        if self.last_msg:  
            temp = self.last_msg
            self.last_msg = {}
            return temp
        else:
            return False

daemon = Pyro4.Daemon()              
uri = daemon.register(SendMsg)  
print("Ready. Object uri =", uri)     
daemon.requestLoop()                  