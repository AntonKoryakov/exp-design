from channels.routing import route_class
from .consumers import Task1Tracker, Task2Tracker

channel_routing = [
    route_class(Task1Tracker, path=Task1Tracker.url_pattern),
    route_class(Task2Tracker, path=Task2Tracker.url_pattern),
]
