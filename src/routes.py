import server
from sensor import sensor

@server.route("/current", methods=["GET"])
def jsonHandler(request):
    return sensor.getCurrentResponse(), 200, "application/json"

@server.route("/history", methods=["GET"])
def jsonHandler(request):
    return sensor.getHistory(), 200, "application/json"

@server.route("/data", methods=["GET"])
def jsonHandler(request):
    return sensor.getDataResponse(), 200, "application/json"

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