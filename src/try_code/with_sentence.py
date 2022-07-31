
class WriteToFile:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def __enter__(self):
        self.file_obj = open(self.file_path, mode="w")
        print('enter')
        return self.file_obj
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            self.file_obj.close()

class WriteAText:
    def __init__(self):        
        print('init')
    
    def __enter__(self):
        print('enter')
        text = 'A test text'
        return text
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')

    
def write_hello_file():
    # __enter__ method from WriteToFile class return a file object    
    with WriteToFile("try_code/hello.txt") as file:        
        file.write("Hello, World  !!!")        
    

def print_a_text():
    # __enter__ method from WriteAText class return a string    
    with WriteAText() as text:
        print ( text )
    print( text + ' out of with' )
    

write_hello_file()
print_a_text()
