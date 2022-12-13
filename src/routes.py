import server
from sensor import sensor

@server.route("/json", methods=["GET"])
def jsonHandler(request):
    return sensor.getJsonResponse(), 200, "application/json"

@server.route("/history", methods=["GET"])
def jsonHandler(request):
    return sensor.getHistory(), 200, "application/json"

@server.route("/dashboard", methods=["GET"])
def logHandler(request):
    html_file = open("web/html/dashboard.html", "r")
    response = html_file.read()
    html_file.close()
    return response, 200, "text/html"

@server.route("/chart", methods=["GET"])
def logHandler(request):
    html_file = open("web/html/chart.html", "r")
    response = html_file.read()
    html_file.close()
    return response, 200, "text/html"

@server.catchall()
def catchall(request):
    path = "web" + request.path
    fileType = ""
    
    if path[-4] == ".css":
        fileType = "text/css"
    elif path[-3] == ".js":
        fileType = "text/javascript"
    elif path[-5] == ".html":
        fileType = "text/html"
    
    try:
        file = open(path, "r")
        response = file.read()
        file.close()
        return response, 200, fileType
    except:
        return "Not found", 404