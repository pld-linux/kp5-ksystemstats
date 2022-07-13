#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.25.3
%define		qtver		5.15.2
%define		kpname		ksystemstats
Summary:	ksystemstats
Name:		kp5-%{kpname}
Version:	5.25.3
Release:	1
License:	BSD Clause 2
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	8896a1fc39e94124061cea7de71fe52a
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.0
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 5.82
BuildRequires:	kf5-kcoreaddons-devel >= 5.85.0
BuildRequires:	kf5-kdbusaddons-devel >= 5.82
BuildRequires:	kf5-kio-devel >= 5.82
BuildRequires:	kf5-networkmanager-qt-devel >= 5.82
BuildRequires:	kf5-solid-devel >= 5.85.0
BuildRequires:	kp5-libksysguard-devel
BuildRequires:	libnl-devel
BuildRequires:	udev-devel

BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	qt5-qmake
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KSystemStats is a daemon that collects statistics about the running
system.

%prep
%setup -q -n %{kpname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	..
%ninja_build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_iconsdir}/{breeze-dark,breeze}
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kstatsviewer
%attr(755,root,root) %{_bindir}/ksystemstats
%{systemduserunitdir}/plasma-ksystemstats.service
%{_libdir}/qt5/plugins/ksystemstats
%{_datadir}/dbus-1/services/org.kde.ksystemstats.service
