from NorseCourse import app

@app.route("/")
def default():
	return "Welcome!"