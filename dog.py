import sys
from os import system
import time
from watchdog.observers import Observer
eventCount = 0


# reading .conf file
config = open('./.conf', 'r').read().strip().split('\n')
print(config)
# a class to handle file modification events from watchdog


class event_handler:
    def dispatch(event):
        global eventCount, codeIsRunning # variables for eventCount logic and to stop the infinite print when a command is running
        # events seem to come in 3 at a time in my system,
        # if your dog runs commands more than once or doesn't run the commands at all,
        # you should remove or adjust the eventCount logic
        eventCount += 1
        if eventCount % 3 == 0:
            # checking whether the modified file is in the conf file
            for i in config[:-1]:
                if(event.src_path.endswith(i)):
                    print()
                    codeIsRunning = True
                    system(config[-1])
                    print("*"*20)
                    codeIsRunning = False
                # conf file changes stop the dog completely 
                # so be careful not to change conf if not necessary
                elif(event.src_path.endswith('.conf')):
                    print("Config file change detected... Aborting...")
                    global terminate
                    terminate = True

# some basic "AnImAtIoN" to see whether the dog is working properly. 
# depending on your terminal emulator, this may or may not work properly. 
# remove it if you don't like it.
animstring = '\\|/-\\|-'
anim = ['\r' + c for c in animstring]
animstate = [0, len(animstring)]

if __name__ == '__main__':
    codeIsRunning = False
    terminate = False
    # initializing and starting the file change observer from the watchdog package
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    try: # running the observer until a KeyboardInterrupt (Ctrl+C)
        while not terminate:
            time.sleep(0.5)
            if not codeIsRunning: # printing the animation until a change to the conf file is detected
                print(anim[animstate[0]], end='Dog is running...')
                animstate[0] += 1
                animstate[0] %= animstate[1]
        else:
            observer.stop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    # observer stopped and the thread is joined