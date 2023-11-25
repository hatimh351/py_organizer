from Organizer import Organizer
import sys


if '__main__' == __name__:
    if (len(sys.argv) != 2):
        print("Config file wasn't provided")
        exit(1)
    obj = Organizer(sys.argv[-1])
    obj.monitoring()