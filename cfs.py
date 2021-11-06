"""
This is just a modified version of cpg to work with direct codeforces links.
"""
from sys import argv
from os import chdir, listdir, mkdir, getcwd, system
from bs4 import BeautifulSoup as Bs
from requests import get

# checking if the link was passed as a command line argument
# asking for an input otherwise
if len(argv)>1:
    htm = get(argv[1])
else:
    htm = get(input("Enter the problem link : "))
soup = Bs(htm.text, 'html.parser')

# getting problem name
Name = str(soup.find('div', {'class': 'title'}).string).replace(' ','_')

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
runners = {}
runnersFile = open("cfs.txt", 'r')
line = runnersFile.readline()
while line:
    line = line.strip()
    if not (line.startswith('#') or len(line) < 2):
        ext, comp, run,vim = line.split(':')
        runners[ext.strip()] = {'compile': comp.strip().replace(
            'NAME', Name), 'run': run.strip().replace('NAME', Name),'vim' : vim.strip()}
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

# making the problem's code file and copying the template to it
codeFile = open(code['filename'], 'w')
codeFile.write(code['filecontents'])
codeFile.close()

# getting testcase data from the request
tcases = [str(i).replace('<pre>', '').replace(
    '</pre>', '').strip('<br/>').strip().split('<br/>') for i in soup.find_all('pre')]

rcfile = open('rcfile','w')
for i in range(1,5):
    rcfile.write('silent! unmap <F%d>\nmap <F%d> :w <CR> :!'%(i,i)+runners[code['extension']]['vim']+' < stdin%d.txt <CR>\n'%(i))
rcfile.close()

runScript = open('run.sh','w')
runScript.write("set -e\n")
runScript.write(runners[code['extension']]['compile']+"\n")
runScript.write("set +e\n")


c = 1
for i in range(0,len(tcases),2):
    f1 = open("stdin%d.txt"%(c),'w')
    f1.write('\n'.join(tcases[i]))
    f1.close()
    f2 = open("stdout%d.txt"%(c),'w')
    f2.write('\n'.join(tcases[i+1])+'\n')
    f2.close()
    runScript.write("echo \"TEST %d\" | tee%stimings.txt\n"%(c,' -a ' if c!=1 else ' '))
    runScript.write("{ time timeout 5 %s < stdin%d.txt > out%d.txt ; } 2>&1 | sed -n 2p | tee -a timings.txt\n"%(runners[code['extension']]['run'],c,c))
    runScript.write("comm stdout%d.txt out%d.txt\n"%(c,c))
    c+=1
runScript.close()

# calling gvim to open the directory with the files also opened
# change this to suit your texteditor or ide
# system('code . '+code['filename'])
system('gvim %s'%(code['filename']))

# TODO: call the dog here