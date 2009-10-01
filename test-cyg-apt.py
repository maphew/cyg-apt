#!/bin/python
import unittest
import pdb
import os
import tarfile


class TestCygApt(unittest.TestCase):

    def setUp(self):
        self.package_name = "testpkg"
        self.pre_remove_marker = "/usr/share/doc/testpkg/README"
        self.post_remove_marker = "/usr/share/doc/testpkg"
        self.post_install_script = "/etc/postinstall/testpkg.sh"
        self.post_install_script_done = \
            "/etc/postinstall/testpkg.sh.done"
        self.pre_remove_script = "/etc/preremove/testpkg.sh"
        self.post_remove_script = "/etc/postremove/testpkg.sh"
        self.pre_remove_script_done = "/etc/preremove/testpkg.sh.done"
        self.post_remove_script_done = "/etc/postremove/testpkg.sh.done"
        self.tarfile = "mini_mirror/testpkg/build/release-2/testpkg/testpkg-0.0.1-0.tar.bz"

    def testinstall_remove(self):
        os.system("cyg-apt remove " + self.package_name);
        self.confirm_remove_clean(self.package_name)
        os.system("cyg-apt install " + self.package_name);
        self.confirm_installed(self.package_name);
        os.system("cyg-apt remove " + self.package_name);
        self.confirm_remove_clean(self.package_name)
        #self.assert_(0)
   
    def assert_fyes(self, f):
            self.assert_(os.path.exists(f) is True)
    
    def assert_fno(self, f):
            self.assert_(os.path.exists(f) is False)    
    
    def tar_do(self, tarball, fn):
        """ Applies fn to each file in a tarfile"""
        if tarfile.is_tarfile(tarball):
            input_tarfile = tarfile.open(tarball)
            contents = input_tarfile.getnames()
            contents = ["/" + f for f in contents]
            for f in contents:
                if os.path.isfile(f):
                    fn(f)
        else:
            print sys.argv[0] + ": " + options.tarfile +\
            " is not a tarfile."
            self.assert_(0)

        
    def confirm_remove_clean(self, package):
        """ Confirms that no files or configuration file state exists for a package that has been subject to cyg-apt remove. """
        
        self.tar_do(self.tarfile, self.assert_fno)    
            
        # Next confirm that the filelist file is gone
        # Not the original cyg-apt behaviour but setup.exe removes
        # this file, so that's taken as correct behaviour.
        # pdb.set_trace()
        f = "/etc/setup/" + package + ".lst.gz"
        self.assert_(os.path.exists(f) is False)

        # Confirm the package is not represented in installed.db
        installed_db = file("/etc/setup/installed.db").readlines()
        for line in installed_db:
            self.assert_(line.split()[0] != package)
            
        # Confirm that the preremove script has been run
        self.assert_fno(self.pre_remove_marker)
        
        # Confirm that the postremove script has been run
        self.assert_fno(self.post_remove_marker)
        
        # Confirm that the preremove script has been moved
        self.assert_fno(self.pre_remove_script)
        self.assert_fyes(self.pre_remove_script_done)
        
        # Confirm that the postremove script has been moved
        self.assert_fno(self.post_remove_script)
        self.assert_fyes(self.post_remove_script_done)
        
         
        

    def confirm_installed(self, package):
        """ Confirms that a package is installed: the tarball files are 
        present, the package is represented in installed.db, if a postinstall script is present it's in the .done form, the filelist file exists and is correct."""
        
        self.tar_do(self.tarfile, self.assert_fyes)
        
        # Confirm that the postinstall script has run
        self.assert_fyes(self.pre_remove_marker)
        self.assert_fyes(self.post_remove_marker)
        
        # Confirm that the postinstall script has been moved
        self.assert_fno(self.post_install_script)
        self.assert_fyes(self.post_install_script_done)
        
if __name__ == '__main__':
    unittest.main()
