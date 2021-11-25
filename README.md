# Jankscripts

# WIP

Some scripts I use for generating template code for programming challenges.  

## What do they do

### dog

Uses a file called `.conf` to run a command(in my case, compiling and executing code) in response to changes in the files you are editing.  
Inspired by Typescript's --watch.  
**IMPORTANT**  
dog requires the python module `Watchdog` which can be installed with `pip install watchdog`  
![gif demosteation of dog](https://github.com/Pubudu-Anuradha/jankscripts-public/blob/main/dog.gif?raw=true)
### cpg

Makes a directory with a code template of your choosing from premade templates and starts your favorite editor. It will ask you to enter a name for he problem but you can also have the name as a command line argument.  
This directory will also contain the `.conf` file for the dog script and by default, the dog script will be called in the shell you run the script in.  
![gif demosteation of cpg](https://github.com/Pubudu-Anuradha/jankscripts-public/blob/main/cpg.gif?raw=true)

### cfs

cpg on roids. This works directly with codeforces links. It extracts the testcases from the codeforces link and also makes a bash script to test them all.  
**IMPORTANT**  
cfs requires the python module `Beautiful Soup` which can be installed with `pip install beautifulsoup4`
![gif demosteation of cfs](https://github.com/Pubudu-Anuradha/jankscripts-public/blob/main/cfs.gif?raw=true)

## Usage

To use any of the scripts, I recommend you use pyinstaller [`pip install pyinstaller`] and making executables of the scripts you want to use with `pyinstaller script.py -F` where script.py is obviously the name of the script. Then moving the templates directory and the executables to a directory that is in your computer's PATH(The executables will be generated in a directory called **dist/** you can add that directory to PATH and move the templates directory there as well).  

You MUST read the source code before doing this and modify it to suit your needs.  

the codes rely on **templates** directory to get the templates as well as the code running instructions.  
This **templates** directory should be on the same directory as your executables. It should contain all your template code files as well as the runners.txt file and the run.json file whcich are used for the generation of script and config files. The specifics on how to customize the scripts are available in the source code.  

Your final directory structure should look something like this.  

- dist/
  - cpg.exe
  - cfs.exe
  - dog.exe
  - templates/
    - template.cpp
    - template.py
    - runners.txt
    - run.json
