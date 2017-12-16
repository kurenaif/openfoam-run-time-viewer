import sys
import os
import json
import datetime
import random
import time
import argparse
from time import strptime, mktime, sleep
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, render_template

from os.path import dirname, exists

from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

class TailHandler(FileSystemEventHandler):
    
    def __init__(self, path, ws):
        # file path
        self.path = path
        self.file = open(path, 'r')
        # read file position
        self.pos = 0
        # [{ExecutionTime, Time}, {ExecutionTime, Time}, ...]
        self.time = []
        # websocket
        self.wss = ws
        # print_line when object is  constructed
        self.print_line()

    def close(self):
        self.file.close()

    def print_line(self):
        self.file.seek(self.pos)
        # {ExecutionTime: value, Time: value}
        time_dict = {}
        for block in iter(lambda: self.file.readline(), ''):
            if(block.find("ExecutionTime") > -1):
                time_dict["ExecutionTime"] = float(block.split(" ")[2])
                if(len(time_dict.keys()) == 2):
                    print(time_dict)
                    self.time.append(time_dict)
                time_dict = {}
                
                # compare with before 100 step
                width = 100
                if(len(self.time) > width):
                    # linear interoplation (using 100step ago time  & now step time)
                    y1 = self.time[-width]["Time"]
                    x1 = self.time[-width]["ExecutionTime"]
                    y2 = self.time[-1]["Time"]
                    x2 = self.time[-1]["ExecutionTime"] 
                    # calc endTime using linear interpolation
                    end_time = (x2-x1)/(y2-y1)*(float(sys.argv[2]) - y1) + x1
                    # float -> datetime
                    end_datetime = (self.start_datetime + datetime.timedelta(seconds = end_time))
                    # send data to websocket
                    self.wss.send(json.dumps([
                        {"time": mktime((self.start_datetime + datetime.timedelta(seconds = x2)).timetuple()), "y":y2, "end_time": str(end_datetime)} ,
                                        ]))
                    # output console
                    print("excepted end time: ", end_datetime)
                    print("reaming time: ", end_time - x2, "sec.")
                        
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
    return

def main(file_path, end_time):
    app.debug = True
    app.config['file_path'] = file_path
    app.config['end_time'] = end_time
    server = pywsgi.WSGIServer(('localhost', 8000), app, handler_class=WebSocketHandler)
    print("server has been started")
    print("please access http://localhost:8000");
    server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict calculation end time')
    parser.add_argument('file_path', help='log file path', type=str)
    parser.add_argument('end_time', help='calculation end time', type=float)
    args = parser.parse_args()
    main(args.file_path, args.end_time)
