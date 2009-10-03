BUILDDIR =  ../build
TARFILE = testpkg-lib-0.0.1-1.tar.bz2
TOOLS = ../../../tools/

all:
	# Create the tarball
	cd $(BUILDDIR)/root ; pwd ; tar --exclude=".svn" -jcf $(TARFILE) *;\
mv $(TARFILE) ../release-2/testpkg-lib;\

	# Copy the default .ini to the build directory
	/usr/bin/cp ../../setup-2.ini ../build

	/usr/bin/cp setup.hint $(BUILDDIR)/release-2/testpkg-lib
	$(TOOLS)md5.sum.py -f ../build/release-2/testpkg-lib/ ../build/release-2/testpkg-lib/md5.sum
	scp ../build/release-2/testpkg-lib/* chrisc@wanda:~/public_html/release-2/testpkg-lib

	$(TOOLS)setup_ini_md5_fix.py ../../setup-2.ini testpkg-lib ../build/release-2/testpkg-lib/testpkg-lib-0.0.1-1.tar.bz2
	patch ../../setup-2.ini testpkg-lib-0.0.1-1.tar.bz2.diff

	scp ../../setup-2.ini chrisc@wanda:~/public_html/setup-2.ini
	/usr/bin/rm -rf testpkg-lib-0.0.1-1.tar.bz2.diff	

clean:
	/usr/bin/rm -f ../build/release-2/testpkg-lib/*
	$(TOOLS)hasfiles.py ../build svn
	/usr/bin/rm -f testpkg-lib-0.0.1-1.tar.bz2.diff
	/usr/bin/rm -f patched.ini
