import threading


class THREAD_PRESET(threading.Thread):
    def __init__(self, target, args=() , daemon=False):
        super(THREAD_PRESET, self).__init__()
        self.target = target
        self.args = args
        self.daemon= daemon
        self.result = None

    def run(self):
        self.result = self.target(self.args)

# class Thread_DataManager:
#     def __init__(self) -> None:
#         self.users=[]
#         self.ThreadSessions={}
#         self.user_count=0
#         self.user_socket_dict={}
#         self.Threads = {}

class Thread:
    def __init__(self):
        self.Activated_threads = set([])
        self.Threads = {}
        self.Thread_count=0
        
    def Constructor(self, target, args=(), daemon=False, thread_mutex = 0):
        new_thread_name='THREAD_{}_{}'.format(target.__name__,thread_mutex)
        
        if self.Activated_threads.intersection({new_thread_name}):
            return self.Constructor(target, args, daemon, thread_mutex + 1)
        
        new_thread = THREAD_PRESET(target, args, daemon)
        
        self.Activated_threads.add(new_thread_name)
        self.Threads[new_thread_name] = new_thread
        self.Thread_count += 1
        
        return new_thread

    def Destructor(self,thread_name):
        if not self.Activated_threads.intersection(thread_name):
            return False
            
        if not self.Threads[thread_name].is_alive():
            return False
        
        del self.Threads[thread_name]
        self.Activated_threads.remove(thread_name)
        self.Thread_count -= 1
        
        return True