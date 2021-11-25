"""
This is just a modified version of cpg to work with direct codeforces links.
"""
from sys import argv
from os import chdir, listdir, mkdir, getcwd, system
from bs4 import BeautifulSoup as Bs
from requests import get
from json import loads
# checking if the link was passed as a command line argument
# asking for an input otherwise
if len(argv) > 1:
    htm = get(argv[1])
else:
    htm = get(input("Enter the problem link : "))
soup = Bs(htm.text, 'html.parser')

# getting problem name
Name = str(soup.find('div', {'class': 'title'}).string).replace(' ', '_')

# saving current working directory for later
wd = getcwd()


# finding the template directory path from the location of the executible or python script
templatePath = argv[0][:-7] if "cfs.exe" in argv[0] else argv[0][:-
                                                                 6] if "cfs.py" in argv[0] else None
templatePath += "templates/"

# changing working directory to templates. should thow an error if it doesn't exist
# ALL DIRECTORY CHANGES  DONE LIKE THIS ARE ONLY VALID IN THE PROGRAM. THE RUNNING SHELL IS NOT AFFECTED
chdir(templatePath)

# processing the runners file
# runners is a dictionary with the script contents and the command mapped to the file extension
# runners = {}
# runnersFile = open("cfs.txt", 'r')
# line = runnersFile.readline()
# while line:
#     line = line.strip()
#     if not (line.startswith('#') or len(line) < 2):
#         ext, comp, run,vim = line.split(':')
#         runners[ext.strip()] = {'compile': comp.strip().replace(
#             'NAME', Name), 'run': run.strip().replace('NAME', Name),'vim' : vim.strip()}
#     line = runnersFile.readline()
runners = loads(open('run.json', 'r').read())
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
mkdir(Name)  # making new directory for the problem
chdir(Name)  # changing to that directory

###############################################################################
# making .conf file for the dog runner, remove if unnecessary
conf = open(".conf", 'w')
conf.write(code['filename'] + '\n' +
           'stdin.txt\n'
           + runners[code['extension']
                     ]['dogcommand'].replace('NAME', Name)+'\n'
           )
conf.close()
###############################################################################

# making the problem's code file and copying the template to it
codeFile = open(code['filename'], 'w')
codeFile.write(code['filecontents'])
codeFile.close()

# getting testcase data from the request
tcases = [str(i).replace('<pre>', '').replace(
    '</pre>', '').replace('<br/>','\n').strip().split() for i in soup.find_all('pre')]
    
##################################################################
# This section is specific to the way I use gvim. Use it if you like, Remove it if you dont.
rcfile = open('rcfile', 'w')
for i in range(1, 5):
    rcfile.write('silent! unmap <F%d>\nmap <F%d> :w <CR> :!' % (
        i, i)+runners[code['extension']]['run']+' < stdin%d.txt <CR>\n' % (i))
rcfile.write('silent! unmap <F5>\nmap <F5> :w <CR> '+' && '.join(
    [runners[code['extension']]['compile'], runners[code['extension']]['run']])+' <CR>')
rcfile.close()
##################################################################

##################################################################
# runscript creates a bash script that runs all the testcases against your code and compares them to the answers. 
runScript = open('run.sh', 'w')
runScript.write("set -e\n")
runScript.write(runners[code['extension']]['compile'].replace(
    '%<', Name).replace('%', Name+code['extension'])+"\n")
runScript.write("set +e\n")
# remove this section and the runscript portion from the next loop if you don't need this script
##################################################################

c = 1
for i in range(0, len(tcases), 2):
    f1 = open("stdin%d.txt" % (c), 'w')
    f1.write('\n'.join(tcases[i]))
    f1.close()
    f2 = open("stdout%d.txt" % (c), 'w')
    f2.write('\n'.join(tcases[i+1])+'\n')
    f2.close()
    runScript.write("echo \"TEST %d\" | tee%stimings.txt\n" %
                    (c, ' -a ' if c != 1 else ' '))
    runScript.write("%s < stdin%d.txt > out%d.txt\n" %
                    (runners[code['extension']]['scriptline'].replace('NAME', Name), c, c))
    runScript.write("comm stdout%d.txt out%d.txt\n" % (c, c))
    c += 1
runScript.close()

# calling gvim to open the directory with the files also opened
# remove/change the following to suit your texteditor or ide
# this calls gvim, which is the editor I use.
# system('gvim %s'%(code['filename']))

# this calls vscode
system('code . '+code['filename'])

# Calling the dog, remove if unnecessary
system('dog')