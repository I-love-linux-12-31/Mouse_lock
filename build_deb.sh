#!/bin/bash

VERSION="1.0.1"
PACKAGE_NAME="mouse-lock"
SOURCES_ROOT=$(pwd)

BUILD_DIR=$(mktemp -d)
cd $BUILD_DIR

mkdir -p $PACKAGE_NAME-$VERSION/DEBIAN
mkdir -p $PACKAGE_NAME-$VERSION/usr/bin
mkdir -p $PACKAGE_NAME-$VERSION/usr/share/applications

cp $SOURCES_ROOT/autolock.py $PACKAGE_NAME-$VERSION/opt/Mouse-lock/
cp $SOURCES_ROOT/main.py $PACKAGE_NAME-$VERSION/opt/Mouse-lock/
cp $SOURCES_ROOT/main.ui $PACKAGE_NAME-$VERSION/opt/Mouse-lock/
cp $SOURCES_ROOT/backend.py $PACKAGE_NAME-$VERSION/opt/Mouse-lock/
cp $SOURCES_ROOT/mouselock $PACKAGE_NAME-$VERSION/usr/bin/
cp $SOURCES_ROOT/mouselock-gui $PACKAGE_NAME-$VERSION/usr/bin/

cat > $PACKAGE_NAME-$VERSION/DEBIAN/control << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Kuznetsov Yaroslav <yaroslav.12.31.dev@gmail.com>
Description: Application for playing games with broken mouse lock.
EOF

fakeroot dpkg-deb --build $PACKAGE_NAME-$VERSION

mv $PACKAGE_NAME-$VERSION.deb $SOURCES_ROOT/$PACKAGE_NAME-$VERSION.deb

cd $SOURCES_ROOT
rm -rf $BUILD_DIR

echo -e "Your .deb file: \033[32m$SOURCES_ROOT/$PACKAGE_NAME-$VERSION.deb\033[0m"