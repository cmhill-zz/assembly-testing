class Read:

    def __init__(self):
        self.pos = -1;
        self.pnext = -1;
        self.contig = -1
        self.len = -1
        self.final = False;
        

    def getPos(self):
        if(self.final):
            return self.pos
        else:
            return -1

    def getPNext(self):
        if(self.final):
            return self.pnext;
        else:
            return -1;

    def getContig(self):
        if(self.final):
            return self.contig
        else:
            return -1;

    def getLen(self):
        if(self.final):
            return self.len
        else:
            return -1;
        
    
    def setPos(self, position):
        if(not self.final):
            self.pos = position;
    
    def setPNext(self, position):
        if(not self.final):
            self.pnext = position;

    def setContig(self, name):
        if(not self.final):
            self.contig = name

    def setLen(self, length):
        if(not self.final):
            self.len = length

    def setFinal(self):
        self.final = True;


