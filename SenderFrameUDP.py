from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import numpy as np
import cv2 as cv
import time
import struct
 
class Client(DatagramProtocol):

    def __init__(self, targethost, targetport):
        self.target = targethost,targetport
        print("Target id", self.target)
    
    def datagramReceived(self, data, addr):
        dr=0
        if addr == self.target and dr==0:
            reactor.callInThread(self.send_message)
            dr=1
        print(data.decode('utf-8'))


    
    def send_message(self):
        global height,width,buf,PktSayi,codex,code 
        global cap
        globals()
        while(cap.isOpened()):            
            
            ret, frame = cap.read()
            frame=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            d = frame.flatten ()
            d=d.reshape(PktSayi,buf)
            
            self.transport.write(code, self.target)
            
            for i in range(PktSayi):
                globals()['r'+str(i)]=d[i]
                globals()['r'+str(i)]=globals()['r'+str(i)].tostring()
                self.transport.write(globals()['r'+str(i)], self.target)
                #time.sleep(0.0038)                
            self.transport.write(codex, self.target)
            #time.sleep(0.001)
   
            
if __name__== '__main__' :
 
    THost="127.0.0.1"
    TPort=51001
    Port=51000

    buf = 5120
    width = 320
    height = 240
    PktSayi=round(((width*height))/buf)

    cap = cv.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    code = 'start'
    code = ('start' + (buf - len(code)) * 'a').encode('utf-8')

    codex = 'start'
    codex = ('start' + (buf - len(codex)) * 'a').encode('utf-8')

    reactor.listenUDP(Port,Client(THost,TPort))
    reactor.run()

  