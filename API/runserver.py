# Allows us to run API locally, although it is still making connections to the remote MySQL server.
# Test for alter
from API import app
app.debug = True
app.run()