#!/bin/bash
VERSION="1.0.2"
SOURCES_ARH="Mouse-lock-$VERSION.tar.gz"

sed -i "s/^Version:.*$/Version:        $VERSION/" mouse_lock.spec

if [ -d "./rpmbuild" ]; then
    rm -rf ./rpmbuild
fi

rpmdev-setuptree
cp ~/rpmbuild/ -r ./

tar -czf $SOURCES_ARH ./autolock.py ./main.py ./main.ui ./backend.py ./mouselock ./mouselock-gui
cp mouse_lock.spec rpmbuild/SPECS/
cp $SOURCES_ARH rpmbuild/SOURCES/

rpmbuild -ba rpmbuild/SPECS/mouse_lock.spec && echo -e "You can find .rpm file at \033[32m./rpmbuild/RPMS/x86_64/\033[0m"

rm $SOURCES_ARH

cp ./rpmbuild/RPMS/x86_64/Mouse-lock* ./
