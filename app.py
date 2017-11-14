import sys
import os
import json
import datetime
import random
import time
from time import strptime, mktime, sleep
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, render_template

from os.path import dirname, exists

from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

class TailHandler(FileSystemEventHandler):
    
    def __init__(self, path, ws):
        self.path = path
        self.file = open(path, 'r')
        self.pos = 0
        self.time = []
        self.wss = ws
        self.print_line()

    def close(self):
        self.file.close()

    def print_line(self):
        self.file.seek(self.pos)
        time_dict = {}
        for block in iter(lambda: self.file.readline(), ''):
            if(block.find("ExecutionTime") > -1):
                time_dict["ExecutionTime"] = float(block.split(" ")[2])
                if(len(time_dict.keys()) == 2):
                    print(time_dict)
                    self.time.append(time_dict);
                time_dict = {}
                
                width = 100
                if(len(self.time) > width):
                    # print(self.time)
                    y1 = self.time[-width]["Time"]
                    x1 = self.time[-width]["ExecutionTime"]
                    y2 = self.time[-1]["Time"]
                    x2 = self.time[-1]["ExecutionTime"] 
                    # print(y2)
                    # print(y1)
                    # print(y2-y1)
                    end_time = (x2-x1)/(y2-y1)*(float(sys.argv[2]) - y1) + x1
                    end_datetime = (self.start_datetime + datetime.timedelta(seconds = end_time))

                    print("ET: ", mktime((self.start_datetime + datetime.timedelta(seconds = x2)).timetuple()), "time", y2)
                    print("ET: ", str(datetime.timedelta(seconds = x2)), "time", y2)
                    self.wss.send(json.dumps([
                        {"time": mktime((self.start_datetime + datetime.timedelta(seconds = x2)).timetuple()), "y":y2, "end_time": str(end_datetime)} ,
                                        ]))
                    print("excepted end time: ", end_time)
                    print("reaming time: ", end_time - x2)
                        
            elif(block.find("Time") > -1):
                try:
                    time_dict["Time"] = float(block.split(" ")[2][:-1])
                except:
                    time = block[:-1].split(":")
                    hour = int(time[1])
                    minute = int(time[2])
                    second = int(time[3])
                    self.start_time = datetime.time(hour,minute,second)
                    self.start_datetime = datetime.datetime.combine(self.start_date, self.start_time)
            elif(block.find("Date") > -1):
                date = block[:-1].split(":")[1].split(" ")
                year = int(date[3])
                month = strptime(date[1],'%b').tm_mon
                day = int(date[2])
                self.start_date = datetime.date(year, month, day)
                print(self.start_date)
        self.pos = self.file.tell()

    def on_modified(self, event):
        if event.is_directory or self.path != event.src_path:
            return
        self.print_line()

def tail_like(path, ws):
    observer = PollingObserver()
    handler = TailHandler(path, ws)
    observer.schedule(handler, dirname(path))
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        handler.close()
    observer.join()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/publish')
def publish():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        tail_like(app.config.get('file_path'), ws)
        # while True:
        #     t = int(time.mktime(datetime.datetime.now().timetuple()))
        #     ws.send(json.dumps([{"time": t, "y": random.random() * 1000},
        #                         {"time": t, "y": random.random() * 1000}]))
        #     time.sleep(1)
    return

if __name__ == '__main__':
    app.debug = True
    app.config['file_path'] = sys.argv[1]
    app.config['end_time'] = sys.argv[2]
    server = pywsgi.WSGIServer(('localhost', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
