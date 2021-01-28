import tkinter

class Application:
    
    def __init__(self, master):
        self.master = master
        master.title("Prerequisite Checker")
    
    
    

def main():
    root = tkinter.Tk()
    app = Application(root)
    
    
if __name__ == "__main__":
    main()
