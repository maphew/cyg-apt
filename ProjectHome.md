**cyg-apt is similar to apt-get. You can use it install and remove packages from the Cygwin command prompt:**

```
$ cyg-apt install gdb
...
$ gdb
...
(gdb)
```

It has many other package management features. It requires a base install of Cygwin, Cygwin Python and gnupg.

cyg-apt is not the official installer (setup.exe) -- it is an experimental project. While it appears to work well within its limitations, there may be issues that have not been identified. See LimitationsAndWorkarounds. It is intended primarily as a helper for managing user-land packages, not as a tool for maintaining the Cygwin system.

### Installation ###
Please refer to GettingStarted.

### Dependencies: ###
  * Cygwin base packages
  * Python 2.5 (the current Cygwin Python.)
See the wiki for more details.

### Commands: ###
```
  * ball - print tarball name
  * buildrequires - print buildrequires: for package
  * download - download package
  * filelist - installed files
  * find - package containing file
  * help - help COMMAND
  * install - download and install packages with dependencies
  * list - installed packages
  * md5 - check md5 sum
  * missing - print missing dependencies
  * new - list new (upgradeable) packages in distribution
  * purge - purge packages from the system
  * remove - uninstall packages
  * requires - print requires: for package
  * search - search package list
  * show - print information for package
  * source - download/unpack source tarball
  * upgrade - all installed packages: use with caution
  * url - print tarball url
  * version - print installed version
```
Many thanks to Jan Nieuwenhuizen who wrote the original cyg-apt script.
