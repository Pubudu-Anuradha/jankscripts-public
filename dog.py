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
        global eventCount, codeIsRunning
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
                    if system(config[-1]) == 0:
                        print("Program ran without errors!")
                    else:
                        print("*"*20)
                    codeIsRunning = False
                # conf file changes stop the dog completely 
                # so be careful not to change conf if not necessary
                elif(event.src_path.endswith('.conf')):
                    print("Config file change detected... Aborting...")
                    global terminate
                    terminate = True


animstring = '\\|/-\\|-'
anim = ['\r' + c for c in animstring]
animstate = [0, len(animstring)]

if __name__ == '__main__':
    codeIsRunning = False
    terminate = False
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    try:
        while not terminate:
            time.sleep(0.5)
            if not codeIsRunning:
                print(anim[animstate[0]], end='Dog is running...')
                animstate[0] += 1
                animstate[0] %= animstate[1]
        else:
            observer.stop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
