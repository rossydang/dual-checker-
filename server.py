#Manages the server compnent. Use tkinter as a fallback


from flask import Flask, request, render_template
app = Flask("dual")

    
@app.route('/', methods=["POST", "GET"])
def pickCollege():
     if request.method == 'POST':
        college_selected = request.form.get("college")
        return college_selected
     return render_template("college.html")

    #handles picking a college 
    #optional, add an AP score

@app.route('/dasd', methods=["POST", "GET"])
def showCouses():
    #show what courses are avalible at a college and its prerequistes
    pass

if __name__ == '__main__':
  
    app.run(debug=True)
