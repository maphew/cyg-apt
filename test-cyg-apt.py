#!/bin/python
import unittest
import pdb
import os
import tarfile
import utilpack
import urllib
import sys
import tarfile
import re
import md5

class TestCygApt(unittest.TestCase):

    def setUp(self):
        self.package_name = "testpkg"
        self.package_name_2 = "testpkg-lib"
        self.relname = "release-2"
        self.cyg_apt_rc_file = ".cyg-apt"
        self.tarname = "testpkg-0.0.1-0.tar.bz2"
        self.tarname_2 = "testpkg-0.0.2-0.tar.bz2"
        self.tarpath = "release-2/testpkg/"                
        self.sourcename = "testpkg-0.0.1-0"
        self.sourcemarker = "mini_mirror/testpkg/build/root/usr/bin/testpkg.exe"
        self.source_unpack_marker = "testpkg-0.0.1-0/usr/bin/testpkg.exe"
        self.version_2_marker = "/etc/ver2_marker"
        self.pre_remove_marker = "/usr/share/doc/testpkg/README"
        self.post_remove_marker = "/usr/share/doc/testpkg"
        self.post_install_script = "/etc/postinstall/testpkg.sh"
        self.post_install_script_done = \
            "/etc/postinstall/testpkg.sh.done"
        self.pre_remove_script = "/etc/preremove/testpkg.sh"
        self.post_remove_script = "/etc/postremove/testpkg.sh"
        self.pre_remove_script_done = "/etc/preremove/testpkg.sh.done"
        self.post_remove_script_done = "/etc/postremove/testpkg.sh.done"
        self.tarfile = "mini_mirror/testpkg/build/release-2/testpkg/" +\
            self.tarname
        self.tarfile_2 = "mini_mirror/testpkg/build/release-2/testpkg/" +\
            self.tarname_2
        self.init_from_dot_cyg_apt()
        self.expected_ballpath = "%s/%s/%s/%s/%s" % \
            (self.opts["cache"],\
            self.mirror_esc,\
            self.relname,\
            self.package_name,\
            self.tarname)
        self.ver = "0.0.1-0"

            
    def init_from_dot_cyg_apt(self):
        self.opts = {}
        rc = file(self.cyg_apt_rc_file).readlines()
        for i in rc:
            k, v = i.split ('=', 2)
            self.opts[k] = eval (v)
        self.mirror_esc = urllib.quote(self.opts["mirror"], "").lower()

    
    def testball(self):
        ballpath = utilpack.popen("cyg-apt ball " + self.package_name)
        ballpath = ballpath.strip()
        # The tarball location is:
        # cache + mirror + releasename + packagename + tarfile_name

        self.assert_(self.expected_ballpath == ballpath)
        
        
    def testdownload(self):
        # First test ability to recognise package that is already 
        #present: download twice to make sure it is there on the second 
        #attempt: independent unittests.
        download_out = \
            utilpack.popen("cyg-apt download " + self.package_name)
        download_out = \
            utilpack.popen("cyg-apt download " + self.package_name)
        download_out = download_out.split("\n")
        self.assert_(download_out[1] == download_out[2])
        self.assert_fyes(self.expected_ballpath)
        
        # Second test: test we can recognise a package is 
        # not present in the cache and download it.
        os.remove(self.expected_ballpath)
        self.assert_fno(self.expected_ballpath)
        download_out = \
            utilpack.popen("cyg-apt download " + self.package_name)
        download_out = download_out.split("\n")
        self.assert_(download_out[1] == download_out[2])
        self.assert_fyes(self.expected_ballpath)
        
    
    def testfilelist(self):
        utilpack.popen("cyg-apt install " + self.package_name)
        filelistout = \
            utilpack.popen("cyg-apt filelist " + self.package_name)
        filelistout = filelistout.split()
        
        if tarfile.is_tarfile(self.expected_ballpath):
            input_tarfile = tarfile.open(self.expected_ballpath)
            contents = input_tarfile.getnames()
            for x,y in zip(filelistout, contents):
                self.assert_(x == y)            
        else:
            # Has test-cyg-apt got the wrong idea about the location of 
            # the tarfile after download?
            self.assert_(False)


    def testfind(self):
        # the find command equates with dpkg -S /path/to/file
        utilpack.popen("cyg-apt install " + self.package_name)
        if tarfile.is_tarfile(self.expected_ballpath):
            input_tarfile = tarfile.open(self.expected_ballpath)
            contents = input_tarfile.getnames()
            found = False
            for f in contents:
                if os.path.isfile("/" + f):
                    found = True
                    break
            if not found:
                self.assert_(False)
            findout =\
                utilpack.popen("cyg-apt find " + "/" + f)
            findout = findout.split()
            out_package_name = findout[0].split(":")[0]
            self.assert_(out_package_name == self.package_name)     
        else:
            self.assert_(False)
            
    def testlist(self):
        exp = re.compile("^([\w\-.]+)(\W+)([0-9a-z.-]+)$")
        utilpack.popen("cyg-apt install " + self.package_name)
        listout = utilpack.popen("cyg-apt list")

        listout = listout.split("\n")
        listout = [x.strip() for x in listout if x.strip()   != ""]
        found_name = None
        found_var = None
        for l in listout:
            groups = exp.search(l)
            if groups:
                name = groups.group(1)
                if name == self.package_name:
                    found_name = name
                    found_ver = groups.group(3)
            else:
                self.assert_(False)
        self.assert_(found_name and found_ver)
        self.assert_(found_ver == self.ver)
        
        
    def testmd5(self):
        utilpack.popen("cyg-apt install " + self.package_name)
        md5out = utilpack.popen("cyg-apt md5 " + self.package_name)
        md5out = md5out.splitlines()
        md5out = [x.split() for x in md5out]
        b = file(self.expected_ballpath,"rb").read()
        m = md5.new()
        m.update(b)
        digest = m.hexdigest()
        self.assert_(digest == md5out[0][0] == md5out[1][0])
        
    
    def testrequires(self):
        # package 2 is a dependency for package
        utilpack.popen("cyg-apt install " + self.package_name)
        requiresout = utilpack.popen("cyg-apt requires "\
            + self.package_name).split()
        self.assert_(self.package_name_2 in requiresout)
        
        
    def testbuildrequires(self):
        # not a great test, but this isn't a great command IMO:
        # there's little facility for separate source dependency tracking in
        # Cygwin, or so it appears.
        utilpack.popen("cyg-apt install " + self.package_name)       
        requiresout = utilpack.popen("cyg-apt buildrequires "\
            + self.package_name).split()
        self.assert_(self.package_name_2 in requiresout)


    def testmissing(self):
        utilpack.popen("cyg-apt install " + self.package_name)
        utilpack.popen("cyg-apt remove " + self.package_name_2)
        missingout = utilpack.popen("cyg-apt missing "\
            + self.package_name).split()
        self.assert_(self.package_name_2 in missingout)
        
    def new_upgrade_test_setup(self, upgrade):
        utilpack.popen("cyg-apt install " + self.package_name)
        setup_ini = self.opts["setup_ini"]
        setup_ini_basename_diff = os.path.basename(setup_ini) + ".diff"
        os.system("/usr/bin/cp " + setup_ini + " " + setup_ini + ".save")
        cmd = "tools/setup_ini_diff_make.py "
        cmd += setup_ini + " "
        cmd += self.package_name + " "
        cmd += "install tarver --field-input "
        cmd += self.tarname + " 0.0.1-0 0.0.2-0"
        #setup_ini_diff_make.py setup-2.ini testpkg install tarver --field-input testpkg-0.0.1-0.tar.bz2 0.0.1-0 0.0.2-0
        os.system(cmd)
        os.system("patch " + setup_ini + " " + setup_ini_basename_diff)
        
        if (upgrade):
            cmd = "tools/setup_ini_diff_make.py "
            cmd += setup_ini + " "
            cmd += self.package_name + " "
            cmd += "install md5 --field-input "
            cmd += self.tarfile_2
            os.system(cmd)
            os.system("patch " + setup_ini + " " + setup_ini_basename_diff)

        
        
    def new_upgrade_test_cleanup(self):
        utilpack.popen("cyg-apt remove " + self.package_name) 
        setup_ini = self.opts["setup_ini"]
        setup_ini_basename_diff = os.path.basename(setup_ini) + ".diff"
        os.system("/usr/bin/mv " + setup_ini + ".save" + " " + setup_ini)
        os.system("/usr/bin/rm " + setup_ini_basename_diff)
        # It's a problem depending on cyg-apt to clean up after these tests
        #utilpack.popen("cyg-apt remove " + self.package_name)
        

    def testnew(self):
        self.new_upgrade_test_setup(False)
        newout = utilpack.popen("cyg-apt new")
        self.new_upgrade_test_cleanup()
        self.assert_(self.package_name in newout)
        
        
    def testupgrade(self):
        self.new_upgrade_test_setup(True)
        upgradeout = utilpack.popen("cyg-apt upgrade")
        self.assert_fyes(self.version_2_marker)
        self.new_upgrade_test_cleanup()
  


    def testshow(self):
        utilpack.popen("cyg-apt install " + self.package_name)
        showout = utilpack.popen("cyg-apt show " + self.package_name)
        self.assert_("testpkg - is a test package" in showout)

        
    def testsource(self):
        utilpack.popen("cyg-apt source " + self.package_name)
        # This may be confusing: the sourcemarker is a file in the  source package
        # build that we need to know is there in the build before we can confidently
        # expect it in the "installed" ie downloaded, unpacked source package from
        # the mini_mirror. It might be less confusing if I hadn't duplicated the
        # files from the "binary" build.
        self.assert_fyes(self.sourcemarker)
        self.assert_fyes(self.sourcename)
        self.assert_fyes(self.source_unpack_marker)
        os.system("/usr/bin/rm -rf " + self.sourcename)
     
        
    def testurl(self):
        os.system("cyg-apt install " + self.package_name);
        urlout = utilpack.popen("cyg-apt url " + self.package_name).strip()
        expect = self.opts["mirror"] + "/" + self.tarpath + self.tarname
        self.assert_(urlout == expect)
        
            
    def testpurge(self):
        os.system("cyg-apt install " + self.package_name);
        self.confirm_installed(self.package_name);        
        utilpack.popen("cyg-apt purge " + self.package_name)
        self.confirm_remove_clean(self.package_name)
        # Purge is a superset of remove clean cleanliness
        self.assert_fno(self.expected_ballpath)
        self.assert_fno(self.post_install_script_done)
        self.assert_fno(self.pre_remove_script_done)
        self.assert_fno(self.post_remove_script_done)
    

    def testinstall_remove(self):
        os.system("cyg-apt remove " + self.package_name);
        self.confirm_remove_clean(self.package_name)
        os.system("cyg-apt install " + self.package_name);
        self.confirm_installed(self.package_name);
        os.system("cyg-apt remove " + self.package_name);
        self.confirm_remove_clean(self.package_name)
        # At the end of this sequence we can expect scripts to reflect
        # the "freshly removed" state. Note we can't expect that after
        # the first remove since we don't know if the package was
        # ever present (or perhaps it was purged)
        self.assert_fyes(self.pre_remove_script_done)
        self.assert_fyes(self.post_remove_script_done) 
        
        
        
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
        f = "/etc/setup/" + package + ".lst.gz"
        self.assert_(os.path.exists(f) is False)

        # Confirm the package is not represented in installed.db
        installed_db = file("/etc/setup/installed.db").readlines()
        for line in installed_db:
            self.assert_(line.split()[0] != package)

        self.assert_fno(self.pre_remove_marker)
        self.assert_fno(self.post_remove_marker)
        self.assert_fno(self.pre_remove_script)
        self.assert_fno(self.post_remove_script)
         
        

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
