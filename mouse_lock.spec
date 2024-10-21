%define _topdir %(pwd)/rpmbuild
%define debug_package %{nil}
Name:           Mouse-lock
Version:        1.0.1
Release:        1%{?dist}
Summary:        Application for playing games with broken mouse lock.
License:        GPLv3
URL:            https://github.com/I-love-linux-12-31/Mouse_lock
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-xlib
Requires:       python3-pyqt6

%description
Application for playing games with broken mouse lock.

%prep
%setup -q -c

%build
# None

%install
mkdir -p %{buildroot}/opt/%{name}
mkdir -p %{buildroot}%{_bindir}

install -m 644 autolock.py %{buildroot}/opt/%{name}/
install -m 644 main.py %{buildroot}/opt/%{name}/
install -m 644 main.ui %{buildroot}/opt/%{name}/
install -m 644 backend.py %{buildroot}/opt/%{name}/
install -m 755 mouselock %{buildroot}%{_bindir}/
install -m 755 mouselock-gui %{buildroot}%{_bindir}/

%files
/opt/%{name}/autolock.py
/opt/%{name}/main.py
/opt/%{name}/main.ui
/opt/%{name}/backend.py
%{_bindir}/mouselock
%{_bindir}/mouselock-gui

%changelog
* Mon Oct 21 2024 Yaroslav Kuznetsov <yaroslav.12.31.dev@gmail.com> - 1.0
- Initial RPM release
