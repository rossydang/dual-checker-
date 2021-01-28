#Manages the server compnent. Use tkinter as a fallback


@app.route('/', methods=["POST", "GET"])
def index():
    
    if request.method == 'POST':
        pass
    return render_template("index.html")    
    #flow of program: 
    #index -> introduction to program
    

    
@app.route('/', methods=["POST", "GET"])
def pickCollege():
    #handles picking a college 
    #optional, add an AP score
    pass

@app.route('/', methods=["POST", "GET"])
def showCouses():
    #show what courses are avalible at a college and its prerequistes
    pass

