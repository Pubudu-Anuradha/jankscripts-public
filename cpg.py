"""
make a folder called tamplates on the same directory as the python file or executable.
THe folder should include you code templates and a runners.txt file
the runners.txt file should have the command that compiles and/or runs your code in the following format

.fileExtension : Command NAME.fileExtension <stdin.txt | tee stdout.txt : time timeout 5 Command NAME.fileExtension <stdin.txt | tee stdout.txt

Spacing doesn't matter but NAME should be replace the filename arguments(leave the extension), example := testfile.cpp => NAME.cpp
examples are available in templates/runners.txt
"""
"""IMPORTANT if you make an executable, the templates directory MUST BE ON THE SAME DIRECTORY AS THE EXECUTABLE"""

from sys import argv
from os import chdir, listdir, mkdir, getcwd, system

# saving current working directory for later
wd = getcwd()

# saving given name from command line argument or asking for a name if that doesn't exist
Name = None
if len(argv)>1:
    Name = argv[1]
else:
    Name = input("Enter a name for the problem : ").strip().replace(' ','_')
    while Name == '':
        Name = input("Enter a valid name for te problem : ").strip().replace(' ','_')

# finding the template directory path from the location of the executible or python script
templatePath = argv[0][:-7] if "cpg.exe" in argv[0] else argv[0][:-
                                                                 6] if "cpg.py" in argv[0] else None
templatePath += "templates/"

# changing working directory to templates. should thow an error if it doesn't exist
# ALL DIRECTORY CHANGES  DONE LIKE THIS ARE ONLY VALID IN THE PROGRAM. THE RUNNING SHELL IS NOT AFFECTED
chdir(templatePath)

# processing the runners file
# runners is a dictionary with the script contents and the command mapped to the file extension
runners = {}
runnersFile = open("runners.txt", 'r')
line = runnersFile.readline()
while line:
    line = line.strip()
    if not (line.startswith('#') or len(line) < 2):
        ext, com, scr = line.split(':')
        runners[ext.strip()] = {'command': com.strip().replace(
            'NAME', Name), 'script': scr.strip().replace('NAME', Name)}
    line = runnersFile.readline()
# print(runners)

# getting the names of all template files with a corresponding extension in runners.txt
templatenames = [fileName for fileName in listdir() if '.' +
                 fileName.split('.')[-1] in runners]

# printing "MeNu".. should be self explanatory
print("---------------------------------")
print("|          -TEMPLATES-          |")
print("---------------------------------")
for i in range(len(templatenames)):
    print(i, templatenames[i], sep=" => ")
print("---------------------------------")
choice = int(input("Enter template number : "))
while choice < 0 or choice >= len(templatenames):
    print("That's an invalid choice")
    choice = int(input("Enter a valid template number : "))

print(templatenames[choice], "was chosen")

# getting relevant information about the chosen template
code = {'extension': '.'+templatenames[choice].split('.')[-1]}
code['filename'] = Name+code['extension']
code['filecontents'] = open(templatenames[choice], 'r').read()


# back to the launched directory
chdir(wd)
mkdir(Name) # making new directory for the problem
chdir(Name) # changing to that directory

# making .conf file for the dog runner
conf = open(".conf", 'w')
conf.write(code['filename'] + '\n' +
           'stdin.txt\n'
           + runners[code['extension']]['command']+'\n'
           )
conf.close()

# making the script defined in runners.txt
timeScript = open('time.sh', 'w')
timeScript.write(runners[code['extension']]['script'])
timeScript.close()

# making the problem's code file and copying the template to it
codeFile = open(code['filename'], 'w')
codeFile.write(code['filecontents'])
codeFile.close()

# making stdin and stdout files
for i in ['stdin.txt', 'stdout.txt']:
    f = open(i, 'w')
    f.close()

# calling vscode to open the directory with the files also opened
# change this to suit your texteditor or ide
system('code . '+code['filename']+' stdin.txt stdout.txt')

# TODO : make the dog runner
# system('dog')
