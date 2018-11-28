from . import app, monitor

if __name__ == '__main__':
    monitor.start()
    app.run(host='0.0.0.0')
