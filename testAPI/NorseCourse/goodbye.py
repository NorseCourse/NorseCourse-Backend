from NorseCourse import app

@app.route("/goodbye")
def goodbye():
	return "Goodbye, world!"