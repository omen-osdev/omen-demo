# Model that represents an instance
# Port is the port for the novnc
# startup_time is the timestamp in seconds since the epoch

import asyncio
import time


class InstanceModel:
    def __init__(self, port, startup_time):
        self.port = port
        self.startup_time = startup_time
    
    async def check_and_shutdown(self, limit_in_seconds):
        while True:
            current_time = int(time.time())
            if current_time - self.startup_time > limit_in_seconds:
                from .instance import delete_instance
                print("Shutting down container!")
                delete_instance(self.port)
                break
            await asyncio.sleep(20) # checking time limits 3 times per minute(every 20s) 