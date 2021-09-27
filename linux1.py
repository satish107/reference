Important
----------------------------------------------------------------
whatis (Description of command)
man # Manual of Command Like man grep
pwd
cd
#-i is used for case insesitive
whoami
hostname


1.File Management Commands
----------------------------------------------------------------

cd ~ # Home dir
ls
ls -l # List all dirs and files
ls -a # List all dirs and files including hidden file
ls -lh # List all dirs and files human readable
ls -al
ls -lR # List all dirs and files Resursively, files in folder and sub folders

touch test.txt # creates a test.txt file
echo "Hello World!" # prints Hello World
echo "Hello World!" > test.txt # Redirect Hello World to test.txt file
cat test.txt # Print Contetnt of text.txt
cat test.txt > test1.txt # Add Contetnt of text1.txt

mkdir test # Create test dir
cp test.txt Test # copy test.txt file to Test dir
rm text.txt # Remove file
rm -R Test/ # Remove Test dir Recursively(delete files or dirs insider Test also)
mv password.txt Test/ # Moves Password.txt file to Test dir
rmdir Test/ # Removes dir if there is nothing in it
mv password.txt test.txt # Rename password.txt to test.txt

2.File & Directory Permissions
----------------------------------------------------------------
u => user
g => group
o => other
a => all
# u or g or o or a or go or ugo... etc
chmod # Allows to change mode and permission of a dir or file
chmod u=rwx test.sh # changes permission for the current user denoted by u
chmod go=rwx test.sh # changes permissions for group and other users
chmod go-wx test.sh # removes permission for group and other users (-wx => minus write and execute)
chmod g+x test.sh # Add execute permission to group
chmod g-x test.sh # Remove execute permission from group

Octal Mode formatter or Binary Mode Formatter
r = 4
w = 2
x = 1
# For rwx we user 4+2+1 that is 7 similarly use it for group and others
chown and chgrp # change ownership or change of the file or folder
chown root test.sh
chgrp root test.sh
groups satish # Group whome you belong

3.grep & Piping
----------------------------------------------------------------
grep "Hello" test.txt # Find Hello in test.txt
grep -i "Hello" test.text # Find Hello in test.txt (Case Sensitive)
cat test.txt | grep "Hello" # Print Content of test.txt and find Hello
ifconfig | grep inet

4. Finding Files With Locate
----------------------------------------------------------------
locate "passwd" | grep "/etc/password"
locate --all "*.conf" | grep "resolve"
locate --all -c proxychains # Count proxychains

5. Enumerating Distribution and karnel Information
----------------------------------------------------------------
hostname # hostname of the computer
sudo vim /etc/hostname # Change hostname of computer
id
lsb_release -a # Details of the system OS
cat /etc/issue # Details of the System
cat /etc/*release # Linux distribution Information
lscpu # Information about CPU
uname -a # Karnel Information
uname -s # karnel name
uname -r #karnel release
uname -p # Information set for processor







