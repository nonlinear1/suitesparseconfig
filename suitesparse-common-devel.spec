%define NAME	SuiteSparse_config
%define	oname	suitesparseconfig
%define	major	4
%define	libname	%mklibname %{oname} %{major}
%define	devname	%mklibname -d %{oname}

Summary:	Configuration file for SuiteSparse packages
Name:		suitesparse-common-devel
Version:	4.2.1
Release:	2
License:	LGPLv2+
Group:		Development/C
Url:		http://www.cise.ufl.edu/research/sparse/UFconfig/
Source0:	http://www.cise.ufl.edu/research/sparse/UFconfig/%{NAME}-%{version}.tar.gz
Patch0:		SuiteSparse_config-4.2.1-increase-default-optimizations.patch
Provides:	ufsparse-common-devel = %{version}-%{release}

%description
UFconfig provides a configuration header file needed by most of the other
packages in SuiteSparse. And static library with few functions.

%package -n	%{libname}
Summary:	Configuration library for SuiteSparse packages
Group:		System/Libraries

%description -n %{libname}
UFconfig provides a configuration header file needed by most of the other
packages in SuiteSparse. And static library with few functions.

%package -n	%{devname}
Summary:	Configuration files for SuiteSparse packages
Group:		Development/C
%rename		%{name}

%description -n %{devname}
UFconfig provides a configuration header file needed by most of the other
packages in SuiteSparse. And static library with few functions.

%prep
%setup -q -n %{NAME}
%patch0 -p1 -b .opts~
chmod -R o+r .

%build
%make CFLAGS="%{optflags}"
ar x lib%{oname}.a
gcc %{ldflags} -shared -Wl,-soname,lib%{oname}.so.%{major} -o \
        lib%{oname}.so.%{version} *.o

%install
for f in *.so*; do
    install -m755 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in *.a; do
    install -m644 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in *.h *.mk; do
    install -m644 $f -D %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{oname}.so.%{version} %{buildroot}%{_libdir}/lib%{oname}.so

%files -n %{libname}
%{_libdir}/lib%{oname}.so.%{major}*

%files -n %{devname}
%doc README.txt
%dir %{_includedir}/suitesparse/
%{_includedir}/suitesparse/*.*
%{_libdir}/lib%{oname}.so
%{_libdir}/lib%{oname}.a
