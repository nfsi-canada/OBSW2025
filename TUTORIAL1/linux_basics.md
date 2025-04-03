# Linux basics

Linux is a UNIX-based operating system, like MacOS but unlike Windows (which is a DOS-based OS). Although it has a well developed GUI for navigation, the attraction of Linux is in its simple syntax when interacting with the filesystem and running codes via a Terminal. This tutorial will show you how to navigate the filesystem on a Linux workstation and run codes using commands.

> Note: The instructions below are taken from https://web.njit.edu/~alexg/courses/cs332/OLD/F2020/hand3f20/Linux-Tutorial.pdf

### Navigating the filesystem

The first step after login is to open a Terminal window. To do this, right-click using the mouse and go to `Open Terminal here`. This will open a Terminal that looks like:



When you first open the Terminal, your current working directory is your `Desktop` directory. Normally, it would be your Home directory, but in CO-501 the workstations are configured to point to `~/Desktop` upon opening a Terminal. This can be seen on the screenshot above, in blue. To navigate to your Home directory (referred to as `~`), simply type:

```
cd
```

Now your terminal should point to `~`. Your home directory has the same name as your user-name, for example, `audetpa`, and it is where your personal files and subdirectories are saved.

To find out what is in your home directory type:

```
ls
```

The `ls` command lists the contents of your current working directory.
However, it does not cause all the files in your home directory to be listed, but only
those ones whose name does not begin with a dot (.) Files beginning with a dot (.) are
known as hidden files and usually contain important program configuration
information. They are hidden because you should not change them unless you are
familiar with Linux.

To list all files in your home directory including those whose names begin with a dot,
type

```
ls -a
```

`ls` is an example of a command which can take options: `-a` is an example of an option.
The options change the behaviour of the command. There are online manual pages
that tell you what options a particular command can take, and how each option
modifies the behaviour of the command. For instance, to list all files with their size in human-readable format, type

```
ls -alh
```

To navigate toe one of the directories on your Home folder, you must use the `cd` command followed by the folder name

```
cd Desktop
```

Followed by `ls` to see its content. To move one folder backward, type 

```
cd ..
```

### Making directories

We will now make a subdirectory in your home directory to hold the files you will be
creating and using in the course of this tutorial. To make a subdirectory called unixstuff
in your current working directory type

```
mkdir testfolder
```

To see the directory you have just created, type `ls`. Then to change directory and go into `testfolder`, type

```
cd testfolder
```

You can create a new folder inside `testfolder`

```
mkdir subfolder
cd subfolder
ls
```

Because we just created it, it's empty. Let's put a blank file there so we have something to display

```
touch newfile.txt
ls
```

The file `newfile.txt` should now be in your `subfolder` directory - at this point it's just an empty file. 

There are two ways to return to your Home directory from here

1 - Type `cd` by itself. This always takes you back to your Home folder.
2 - Type `cd ../..`. This means "go back by two folders", which is your Home directory.

### Paths

Now that we are familiar with the navigation, it's useful to look at how Paths are defined. A Path is simply the position in the filesystem tree of a particular folder or file. For instance, from your Home directory, type

```
pwd
```

This should show the path to your Home directory from the "root" directory on the computer, e.g., `/Users/home/audetpa`.

You can also navigate to the `subfolder` by typing its Path, relative to your position. For instance, from your Home directory, type

```
cd testfolder/subfolder
```

Or, you could check out the content of a folder from your Home directory by typing its Path

```
cd
ls testfolder/subfolder
```

### Viewing/editing text files

Up to now, we created an empty file called `testfile.txt`. Let's put one line of text in it, then we'll see how to view its content from the terminal. First, type

```
echo "Hello world" > testfile.txt
```

The command `echo` types out a string, and we re-directed it to the file `testfile.txt`. To view the content of `testfile.txt`, you can type

```
cat testfile.txt
```

This allows you to parse a file quickly, without opening it using an application. Most of the time, though, we will want to open files to edit them. There are several applications available on the Linux workstations in CO-501. For instance, the simplest one might be `mousepad`, e.g.

```
mousepad testfile.txt
```

This opens the Mousepad application (a simple text editor) with the content of `testfile.txt`. Another one is

```
geany testfile.txt
```

With these text editors, you can modify the text and save it.

### Copying files and directories

`cp file1 file2` is the command which makes a copy of `file1` in the current working
directory and calls it `file2`.

What we are going to do now is to take a file stored in an open access area of the file
system, and use the `cp` command to copy it to your `testfolder `directory.

First, change to your `subfolder` directory.

```
cd ~/testfolder/subfolder
```

Then type

```
cp testfile.txt testfile2.txt
```

Directories can also be copied with the `cp` command, but it’s necessary to add the
option `–R` to do so. This option means ‘recursive’ and will copy the contents of the
directory as well as the directory itself, for example

```
cp
cp -R testfolder testfolder2
```

This creates a full copy of `testfolder` and renames it `testfolder2`. You now have a duplicate of `testfolder` on your Home directory.

### Moving files and directories

The move command has a variety of similar but subtly different uses. It can be used
to move a file to a different location (i.e. a different directory). It can also be used to
move multiple files to a different directory. It can also be used to rename a file or a
directory. For example:

```
cd
touch newfile.txt
mv newfile.txt testfolder/subfolder/.
```

This would move `newfile.txt` from the current directory into `subfolder`. Similarly, if you had many files in your current directory, you could type

```
mv file1 file2 file3 directory1/
```

This would move `file1`, `file2` and `file3` from the current directory into `directory1`.

```
mv file1 file2
```

This would rename `file1` as `file2`.

```
mv directory1/ directory2/
```

This would rename a directory. Finally,

```
mv file1 directory/file2
```

This would move and rename a file in one step.

### Removing files and directories

To delete (remove) a file, use the `rm` command. As an example, we are going to create
a copy of the science.txt file then delete it. Inside your `subfolder` directory, type

```
cp testfile.txt tempfile.txt
ls
rm tempfile.txt
ls
```

In order to delete an empty directory you can use the command

```
rmdir directory
```

However this won't remove directories that already have files in them, instead you can
use

```
rm -r directory
```

to recursively delete files in directory (use sparingly - ***there is no Recycle bin!***)