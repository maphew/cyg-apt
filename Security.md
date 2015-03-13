## Summary: ##

**cyg-apt-1.0.6-1** and above performs signature verifications for setup.ini files it downloads. This is the same behaviour as setup.exe. Verification provides some protection against theoretical bad mirrors hosting malware versions of Cygwin packages. The protection can be subverted by an attacker with access to your Cygwin installation.

If you are not the sole user of your Cygwin installation, install cyg-apt as the most privileged user.

|In line with setup.exe, the -X option disables signature verification.|
|:---------------------------------------------------------------------|

## Details: ##

cyg-apt 1.0.6-1 and above requires the Cygwin gnupg package to be installed. Upon installation, cyg-apt adds Cygwin's public key to the gpg keyring.

cyg-apt uses Cygwin's public key to verify the contents of downloaded setup.ini files. This file lists md5sum values for available packages. A rouge server will be able to generate md5sum for a malware version of a package and edit its' setup.ini -- but without access to Cygwin's private key the altered file will not pass signature verification.

|Signing of new, clean, setup.ini files on  servers with Cygwin's public key is part of the Cygwin package distribution system.|
|:-----------------------------------------------------------------------------------------------------------------------------|

cyg-apt performs signature verification using gpg, matching successful results against an inbuilt Cygwin key signature. To do so:
```
$cyg-apt update
```
Downloads:
  * setup.ini
  * setup.ini.sig
(A GPG formatted DSA signature.)

This scheme can be subverted in numerous ways by an attacker with access to a Cygwin installation: gpg could be replaced with a dummy .exe, cyg-apt could be edited not perform verification, and so on. Then again, with access the attacker could just as easily just install the malware directly.

If your install is secure, signing provides increased security againsts bad Cygwin mirrors.