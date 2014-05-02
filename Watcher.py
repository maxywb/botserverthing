import threading

class Watcher(threading.Thread):
## private
    def __init__(self,con):
        super(Watcher,self).__init__()
        self._connection = con
        self._stop = False

## public
    def join(self):
        self._stop = True
        threading.Thread.join(self)

