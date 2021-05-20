from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import cv2 as cv
import numpy as np
import struct, time, socket, threading


class Client(DatagramProtocol):
    def __init__(self, targethost, targetport):        
        self.server = targethost,targetport
        print("Target id", self.server)
    
    def startProtocol(self):
        self.transport.write("ready".encode('utf-8'),self.server)

    def datagramReceived(self, data, addr):
        globals()
        global code,codex,start,frame
        global chunks,Gortt,PktSayi


        if data.startswith(code):
            start = True
            chunks=[]
        elif data.startswith(codex):
            start = False
            
        if (len(chunks)<PktSayi):
            if(start):
                chunks.append(data)    


        if len(chunks)==PktSayi:
            byte_frame = b''.join(chunks)
            frame = np.frombuffer(byte_frame, dtype=np.uint8).reshape(height, width)


def Goruntule():
    global frame
    globals()
    while True:
        print(len(frame))
        if len(frame)>0:
            cv.imshow('recv', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break        

if __name__== '__main__' :
    buf = 5120
    width = 320
    height = 240
    code = b'start'
    codex = b'stop'
    PktSayi=round(((width*height))/buf)
    frame=np.array([])
    chunks = []
    Gortt=[]
    start=False
    THost="127.0.0.1"
    TPort=51000
    Port=51001
    protocolThread = threading.Thread(target=Goruntule)
    protocolThread.daemon=True
    protocolThread.start()
    reactor.listenUDP(Port,Client(THost,TPort))
    reactor.run()

