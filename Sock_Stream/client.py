import cv2
import numpy as np
import socket
import struct
from io import BytesIO
import pickle
import base64

cap = cv2.VideoCapture(0)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.42.238', 5555))
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connected = True

while cap.isOpened():
    try:
        _, frame = cap.read()
        memfile = BytesIO()
        np.save(memfile, frame)
        memfile.seek(0)
        data = memfile.read()
        #print(len(data))

        client_socket.sendall(struct.pack(">L", len(data)) + data)
    except socket.error:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        print('Retrying to Connect To server')
        while not connected:
            try:

            #client_socket.close()
                print('Connecting')
                client_socket.connect(('192.168.42.238', 5555))
                print('Successfull')
                connected = True
            # _, frame = cap.read()
            # memfile = BytesIO()
            # np.save(memfile, frame)
            # memfile.seek(0)
            # data = memfile.read()
            # #print(len(data))

            # client_socket.sendall(struct.pack(">L", len(data)) + data)
            except socket.error:
                pass
client_socket.close()
    # ret, frame = cam.read()
    # result, img_encode = cv2.imencode('.jpg', frame, encode_param)
    # data = zlib.compress(pickle.dumps(frame, 0))
    # img_encode = cv2.imencode('.jpg', frame)
    # img_encode = base64.b64encode(cv2.imencode('.png', frame)[1])
    # data = pickle.dumps(img_encode, 0)
    # size = len(data)
    # print("{}: {}".format(size))
    # # img_counter+=1
    # client_socket.sendall(struct.pack(">L", size) + data)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

cap.release()