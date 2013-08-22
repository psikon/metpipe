import sys,os, time

class Logging:
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
    
    def printStep(self, step_number, step_name, step_params):
        sys.stdout.write('Step %i: %s \n' % (step_number,step_name))
        sys.stdout.write('params: %s \n'% (step_params))

        
    def updateCMD(self,message):
        sys.stdout.write(message)
        sys.stdout.write('\r')
        sys.stdout.flush()
    
    def openLogfile(self,destination):
        pass
    
    def writeLogFile(self,message):
        pass
    
    def example(self, message):
        for i in range(100):
            sys.stdout.write(message)
            sys.stdout.write('\r')
            #time.sleep(1)