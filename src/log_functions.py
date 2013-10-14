import sys, os, time
    
# write standardized informations about the pipeline steps to stdout
def print_step(step_number, step_description, step_name, step_params):
    
        sys.stdout.write('Step %i - %s: %s \n' % (step_number, step_description, step_name))
        sys.stdout.write('Parameter: %s \n' % (step_params))
    
# simple function for verbose output
def print_verbose(message):
    
    sys.stdout.write(message)
    
# simple print a newline
def newline():
    
    sys.stdout.write(os.linesep)
        
# function for the normal compacter output - gives only informations about 
# the calculation at the moment
def print_compact(message):
    
    # write line to stdout
    sys.stdout.write(message)
    # jump back to te beginning of the line
    sys.stdout.write('\r')
    # clear the line
    sys.stdout.flush()
    
# opens a log file for writing
def open_logfile(destination):
    
    return open(destination, 'w')
     
# check path for exists and filesize
def remove_empty_logfile(path):
    
    if os.path.isfile(path) and os.path.getsize(path) == 0:
        os.remove(path)
        
# convert the output get from time()-function to human readable output
def getDHMS(seconds):
    
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return "%d days, %d hours, %d minutes, %d seconds" % (days, hours, minutes, seconds)
    
# return only the file of a path for better readable output on commandline
def cut_path(path):
    
    tmp = []
    for i in range(len(path)):
        a, b = os.path.split(path[i])
        tmp.append(b)
    return ', '.join(tmp)
    
def print_running_time(actual_time):
    
    sys.stdout.write('processed in ' + getDHMS(time.time() - actual_time) + '\n')
    newline()
    
def skip_msg(skipped_step):
    
    sys.stdout.write('Skipping Step: %s \n' % (skipped_step.upper()))
    newline()
    
