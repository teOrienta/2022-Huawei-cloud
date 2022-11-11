import traceback

def verify_connection(func):
    def execute_method(self, *args, **kwargs):
        if not self.is_connected: 
            print("DATABASE NOT CONNECTED")
            return False
        
        try:
            result = func(self, *args, **kwargs)
        except:
            traceback.print_exc()
            result = None
        
        return result
    return execute_method