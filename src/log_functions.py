import sys, os, time

class Logging:
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
    
    # write standardized informations about the pipeline steps to stdout
    def print_step(self, step_number, step_description, step_name, step_params):
        sys.stdout.write('Step %i - %s: %s \n' % (step_number, step_description, step_name))
        sys.stdout.write('Parameter: %s \n'% (step_params))
    
    # simple function for verbose output
    def print_verbose(self, message):
        sys.stdout.write(message)
    
    # function for the normal compacter output - gives only informations about 
    # the calculation at the moment
    def print_compact(self, message):
        # write line to stdout
        sys.stdout.write(message)
        # jump back to te beginning of the line
        sys.stdout.write('\r')
        # clear the line
        sys.stdout.flush()
    
    # opens a log file for writing
    def open_logfile(self, destination):
        return open(destination, 'w')
    
    # convert the output get from time()-function to human readable output
    def getDHMS(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return "%d days, %d hours, %d minutes, %d seconds" % (days, hours, minutes, seconds)
    
    