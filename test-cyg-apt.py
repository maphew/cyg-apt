#!/bin/python
import unittest
import pdb
import os
import tarfile

class TestCygApt(unittest.TestCase):

    def setUp(self):
        print "In setUp"


    def testinstall(self):
        os.system("cyg-apt remove joe");
        self.confirm_remove_clean("joe")
        os.system("cyg-apt install joe");
        self.confirm_installed("joe");
        #self.assert_(0)
        
   
    def assert_file_exists(self, f):
        if os.path.isfile(f):
            self.assert_(os.path.exists(f) is True)
    
    def assert_file_doesnt_exist(self, f):
        if os.path.isfile(f):
            self.assert_(os.path.exists(f) is False)    
    
    def tar_do(self, tarball, fn):
        """ Applies fn to each file in a tarfile"""
        if tarfile.is_tarfile(tarball):
            input_tarfile = tarfile.open(tarball)
            contents = input_tarfile.getnames()
            contents = ["/" + f for f in contents]
            for f in contents:
                fn(f)
        else:
            print sys.argv[0] + ": " + options.tarfile +\
            " is not a tarfile."    

        
    def confirm_remove_clean(self, package):
        """ Confirms that no files or configuration file state exists for a package that has been subject to cyg-apt remove. """
        
        # First confirm all the files from the tarball are gone
        # TODO create a small model test package to use rather than joe
        tarball = "testdata/joe-3.7-1.tar.bz2"
        if tarfile.is_tarfile(tarball):
            input_tarfile = tarfile.open(tarball)
            contents = input_tarfile.getnames()
            contents = ["/" + f for f in contents]
            for f in contents:
                if os.path.isfile(f):
                     self.assert_(os.path.exists(f) is False)
        else:
            print sys.argv[0] + ": " + options.tarfile +\
            " is not a tarfile."    
            
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
        

    def confirm_installed(self, package):
        """ Confirms that a package is installed: the tarball files are 
        present, the package is represented in installed.db, if a postinstall script is present it's in the .done form, the filelist file exists and is correct."""
        tarfile_name = "/e/home/application_data/cygwin/http%3a%2f%2fmirror.internode.on.net%2fpub%2fcygwin%2f/release/joe/joe-3.5-2.tar.bz2"
        self.tar_do(tarfile_name, self.assert_file_exists)
        
if __name__ == '__main__':
    unittest.main()
