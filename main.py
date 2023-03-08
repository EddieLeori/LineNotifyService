from lib.utility import *
from line_notify_service import LineNotifyService

if __name__ == "__main__":
    service = LineNotifyService()
    service.run()
    Log('LineNotifyService closed.')