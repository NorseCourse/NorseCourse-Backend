from NorseCourse import app

@app.route("/hello")
def hello():
	return "Hello, world!"