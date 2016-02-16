# Allows us to run API locally, although it is still making connections to the remote MySQL server.

from API import app
app.debug = True
app.run()