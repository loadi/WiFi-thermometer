import sys
from server import start_server

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[2].isdigit():
            start_server(host=sys.argv[1], port=sys.argv[2])
        else:
            print("Wrong port!")
    else:
        start_server()
