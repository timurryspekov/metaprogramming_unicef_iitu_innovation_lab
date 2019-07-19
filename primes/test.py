class A:
    token = None
    def set_token(self, token):
        A.token = token

    def __init__(self, name, desctiption=None):
        self.name = name
        self.desctiption = desctiption
    
    def start(self):
        print(f"task {self.name} started")

        

