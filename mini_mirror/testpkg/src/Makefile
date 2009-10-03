BUILDDIR =  ../build
TARFILE = testpkg-0.0.1-0.tar.bz2
TOOLS = ../../../tools/

all:
	gcc testpkg.c -o $(BUILDDIR)/root/usr/bin/testpkg
	/usr/bin/cp postinstall-testpkg.sh $(BUILDDIR)/root/etc/postinstall/testpkg.sh
	/usr/bin/cp preremove-testpkg.sh $(BUILDDIR)/root/etc/preremove/testpkg.sh
	/usr/bin/cp postremove-testpkg.sh $(BUILDDIR)/root/etc/postremove/testpkg.sh
	cd $(BUILDDIR)/root ; pwd ; tar --exclude=".svn" -jcf $(TARFILE) *;\
cp $(TARFILE) ../release-2/testpkg;\
mv $(TARFILE) ../release-2/testpkg/testpkg-0.0.1-0-src.tar.bz2
	cp ../../setup-2.ini ../build
	/usr/bin/cp setup.hint $(BUILDDIR)/release-2/testpkg
	$(TOOLS)md5.sum.py -f ../build/release-2/testpkg/ ../build/release-2/testpkg/md5.sum
	scp ../build/release-2/testpkg/* chrisc@wanda:~/public_html/release-2/testpkg
	scp ../build/setup-2.ini chrisc@wanda:~/public_html/
	$(TOOLS)setup_ini_md5_fix.py ../../setup-2.ini testpkg ../build/release-2/testpkg/testpkg-0.0.1-0.tar.bz2
	patch ../../setup-2.ini testpkg-0.0.1-0.tar.bz2.diff
	$(TOOLS)setup_ini_md5_fix.py ../../setup-2.ini testpkg ../build/release-2/testpkg/testpkg-0.0.1-0-src.tar.bz2
	patch ../../setup-2.ini testpkg-0.0.1-0-src.tar.bz2.diff
	scp ../../setup-2.ini chrisc@wanda:~/public_html/setup-2.ini
	/usr/bin/rm -rf testpkg-0.0.1-0-src.tar.bz2.diff
	/usr/bin/rm -rf patched.ini
	/usr/bin/rm -rf testpkg-0.0.1-0.tar.bz2.diff	

clean:
	/usr/bin/rm -f ../build/release-2/testpkg/*
	/usr/bin/rm -f ../build/setup-2.ini
	/usr/bin/rm -f ../build/root/usr/bin/*
	/usr/bin/rm -f ../build/root/etc/postinstall/*
	/usr/bin/rm -f ../build/root/etc/preremove/*
	/usr/bin/rm -f ../build/root/etc/postremove/*
	$(TOOLS)hasfiles.py ../build svn
	/usr/bin/rm -f testpkg-0.0.1-0-src.tar.bz2.diff
	/usr/bin/rm -f testpkg-0.0.1-0.tar.bz2.diff
