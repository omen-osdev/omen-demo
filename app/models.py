# Model that represents an instance
# Port is the port for the novnc
# startup_time is the timestamp in seconds since the epoch

class InstanceModel:
    def __init__(self, port, startup_time):
        self.port = port
        self.startup_time = startup_time