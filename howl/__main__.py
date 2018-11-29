from .application import monitor, app

monitor.start()
app.run(host='0.0.0.0')
