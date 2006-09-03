Summary:	PEX extension library
Summary(pl):	Biblioteka rozszerzenia PEX
Name:		XFree86-PEX
Version:	4.3.0
Release:	1
License:	MIT
Group:		X11/Libraries
# PEX directories extracted from X430src-{1,3,4,6,7}.tgz:
# xc/fonts/PEX
# xc/lib/PEX5
# xc/programs/Xserver/PEX5
# xc/doc/specs/PEX5
# xc/doc/hardcopy/PEX5
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	bbfef5d0e822f033aa621ead56020bc8
Patch0:		%{name}-miscstruct.patch
URL:		http://www.xfree86.org/
BuildRequires:	XFree86-Xserver-devel > 4.3.99.902-0.1
BuildRequires:	XFree86-devel >= 4.3.0
Requires:	XFree86-libs >= 4.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
PEX extension library.

%description -l pl
Biblioteka rozszerzenia PEX.

%package devel
Summary:	PEX extension headers
Summary(pl):	Pliki nag³ówkowe rozszerzenia PEX
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	XFree86-devel >= 4.3.0

%description devel
PEX extension headers.

%description devel -l pl
Pliki nag³ówkowe rozszerzenia PEX.

%package static
Summary:	PEX extension static library
Summary(pl):	Statyczna biblioteka rozszerzenia PEX
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
PEX extension static library.

%description static -l pl
Statyczna biblioteka rozszerzenia PEX.

%package doc
Summary:	PEX extension documentation
Summary(pl):	Dokumentacja do rozszerzenia PEX
Group:		X11

%description doc
PEX extension documentation.

%description doc -l pl
Dokumentacja do rozszerzenia PEX.

%package -n XFree86-module-PEX
Summary:	PEX extension module
Summary(pl):	Modu³ rozszerzenia PEX
Group:		X11
%{requires_eq_to XFree86-modules XFree86-Xserver-devel}

%description -n XFree86-module-PEX
PEX extension module for X server.

%description -n XFree86-module-PEX -l pl
Modu³ rozszerzenia PEX dla X serwera.

%package -n XFree86-fonts-PEX
Summary:	PEX fonts
Summary(pl):	Fonty PEX
Group:		X11

%description -n XFree86-fonts-PEX
PEX fonts for PEX extension.

%description -n XFree86-fonts-PEX -l pl
Fonty PEX do rozszerzenia PEX.

%prep
%setup -q
%patch0 -p1

%build
cd xc/lib/PEX5
ln -s .. X11
imake -DUseInstalled -I/usr/X11R6/lib/X11/config \
	-DNormalLibPex=YES \
	-DSharedLibPex=YES \
	-DDebugLibPex=NO \
	-DProfileLibPex=NO \
	-DSharedPexReqs="-L/usr/X11R6/lib -lX11 -lm"
%{__make} \
	CDEBUGFLAGS="%{rpmcflags} -I." \
	SOPEXREV="6.0"

cd ../../programs/Xserver/PEX5
for f in `find . -name Imakefile`; do
cd `dirname $f`
imake -DUseInstalled -I/usr/X11R6/lib/X11/config \
	-DPexDipexDefines="/**/" \
	-DPexDdpexDefines="/**/" \
	-DPexShmIPC=YES \
	-DPexPhigsDefines="/**/" \
	-DPexClientDefines="-DPEX_SI_PHIGS"
cd -
done
%{__make} depend \
	TOP=/usr/X11R6/include/X11/Xserver \
	EXTRA_INCLUDES="-I/usr/X11R6/include/X11/Xserver -I/usr/X11R6/include/X11"

%{__make} \
	TOP=/usr/X11R6/include/X11/Xserver \
	CDEBUGFLAGS="%{rpmcflags} -I/usr/X11R6/include/X11"

cd ../../../fonts/PEX
xmkmf
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C xc/lib/PEX5 install \
	DESTDIR=$RPM_BUILD_ROOT \
	SOPEXREV="6.0"

%{__make} -C xc/programs/Xserver/PEX5 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C xc/fonts/PEX install \
	DESTDIR=$RPM_BUILD_ROOT

find xc/doc/hardcopy -name Imakefile | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/X11/PEX5

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files doc
%defattr(644,root,root,755)
%doc xc/doc/hardcopy/PEX5/*

%files -n XFree86-module-PEX
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/modules/extensions/libpex5.a

%files -n XFree86-fonts-PEX
%defattr(644,root,root,755)
%{_fontsdir}/PEX
