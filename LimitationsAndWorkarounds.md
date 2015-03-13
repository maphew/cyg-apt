In practice these packages are few in number, mostly present when cyg-apt is installed and not affected by most cyg-apt commands. There are workarounds:
  1. Use setup.exe to handle the package. Note recent versions have some command line functionality: they allow you to install/upgrade packages on the command line.
```
setup-1.7.exe -q -P python
```
  1. run cyg-apt from a Windows cmd shell as detailed below.

## Services -- running processes ##

If a package is associated with a running process, the process will not be changed when the package is changed. For this reason it is best to stop all services and processes associated with a package before removing or upgrading it.

# Details #
The packages cyg-apt cannot change _under Cygwin_ are:
```
$cat .cyg-apt
...
barred = "python cygwin base-cygwin coreutils bash zlib libreadline"
```

These packages are termed "barred" packages and you will be warned if you attempt to remove or install them. You can, however, change almost all of them by running cyg-apt from a Windows cmd shell. The exception is the "cygwin" package -- see below.

To run cyg-apt from a cmd shell you will need Windows Python (not the same as Cygwin python.)

|http://www.python.org/download/releases/2.6.2/|
|:---------------------------------------------|

(cyg-apt hasn't been tested under the upcoming Python 3.0. But then again Cygwin is back in the misty 2.5 days :D )
  * Copy cyg-apt to your Cygwin home directory
  * Open a DOS box
  * Navigate to your home directory
  * Update package with -f (force) flag

## Example: upgrading zlib to a new release: ##
```
$ cd ~
$ copy /usr/bin/cyg-apt .
start->run->cmd
C:\Documents and Settings\chrisc> e:
E:\> cd E:\cygwin_1_7\home\chrisc
E:\cygwin_1_7\home\chrisc>
E:\cygwin_1_7\home\chrisc> python cyg-apt --help
cyg-apt [OPTION]... COMMAND [PACKAGE]...
Configuration: E:/cygwin_1_7/home/chrisc/.cyg-apt
    Commands:
...
E:\cygwin_1_7\home\chrisc>python cyg-apt install zlib
cyg-apt: NOT installing zlib: cyg-apt is dependent on this package under Cygwin.
Use -f to override but proceed with caution.

E:\cygwin_1_7\home\chrisc>python cyg-apt -f install zlib
E:/home/application_data/cygwin_1_7/http%3a%2f%2fmirror.internode.on.net%2fpub%2
fcygwin%2f/release-2/zlib/zlib-1.2.3-10.tar.bz2
b518ce6051d0ca46985d3cd04aa83439  zlib-1.2.3-10.tar.bz2
b518ce6051d0ca46985d3cd04aa83439  zlib-1.2.3-10.tar.bz2
installing zlib 1.2.3-10
```

## Modifying "cygwin" package is not possible without hacking cyg-apt ##
The above method will work on all packages expect "cygwin". cyg-apt uses mount.exe from the "cygwin" package to get the mount table. If you must use cyg-apt to modify the package "cygwin" you will need to hack it to provide an accurate canned output from mount.

## Warning ##
The -f flag is a safety catch: I recommend great caution when updating the Cygwin core packages. It is possible that the official setup.exe may carry out undocumented actions when updating the Cygwin core which cyg-apt will not emulate.

## Symbolic Links and the "coreutils" package ##
cyg-apt will recreate symbols links in packages unless it doesn't have access to Cygwin "ln", which can happen if you uninstall coreutils. If ln isn't available it falls back to creating copies of files.