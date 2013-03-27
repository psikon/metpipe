class fileHandler:

    def __init__(self, typ, status, origin, destination, path,format, parameter):
        self.__typ = typ
        self.__status = status
        self.__origin = origin
        self.__destination = destination
        self.__path = path
        self.__format = format
        self.__parameter = parameter

    def __del__(self):
        pass
    
    def getType(self):
        return self.__typ
    
    def getStatus(self):
        return self.__status
    
    def getOrigin(self):
        return self.__origin
    
    def getDestination(self):
        return self.__destination
    
    def getPath(self):
        return self.__path
    
    def getFormat(self):
        return self.__format
    
    def getParameter(self):
        return self.__parameter
    
    def setType(self, typ):
        self.type = typ
        
    def setStatus(self, status):
        self.__status = status
        
    def setOrigin(self, origin):
        self.__origin = origin
    
    def setDestination(self, destination):
        self.__destination = destination
    
    def setPath(self, path):
        self.__path = path
    
    def setFormat(self, format):
        self.__format = format
    
    def setParameter(self, parameter):
        self.__parameter = parameter
