%define major %(echo %{version} |cut -d. -f1)
%define libname %mklibname nana %{major}
%define devname %mklibname -d nana

Name:		nana
Summary:	A C++ GUI library
Version:	1.7.4
Release:	1
Source0:	https://github.com/cnjinhao/nana/archive/v%{version}.tar.gz
Patch0:		nana-1.7.4-find-alsa.patch
Group:		System/Libraries
License:	BSL-1.0
BuildRequires:	cmake
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(alsa)

%description
A C++ GUI library

%package -n %{libname}
Summary:	A C++ GUI library
Group:		System/Libraries

%description -n %{libname}
A C++ GUI library

%files -n %{libname}
%{_libdir}/libnana.so.%{major}*

%package -n %{devname}
Summary:	Development files for the Nana C++ GUI library
Group:		Development/C

%description -n %{devname}
Development files for the Nana C++ GUI library

%files -n %{devname}
%{_includedir}/nana
%{_libdir}/*.so

%prep
%autosetup -p1
# Can't use %%cmake because there's a build/ directory already
%if "%{_lib}" != "lib"
sed -i -e 's,DESTINATION lib,DESTINATION %{_lib},g' build/cmake/install_nana.cmake
%endif
# Fix soname
sed -i -e '/add_library(nana::nana/iset_target_properties(nana PROPERTIES VERSION %{version} SOVERSION %{version})' CMakeLists.txt
cmake \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags}" \
	-DCMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO="%{optflags}" \
	-DCMAKE_MODULE_LINKER_FLAGS_RELWITHDEBINFO="%{optflags}" \
	-DCMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO="%{optflags}" \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DNANA_CMAKE_ENABLE_CONF:BOOL=ON \
	-DNANA_CMAKE_ENABLE_JPEG:BOOL=ON \
	-DNANA_CMAKE_ENABLE_PNG:BOOL=ON \
	-DNANA_CMAKE_INSTALL:BOOL=ON \
	-DNANA_STATIC_STDLIB:BOOL=OFF \
	-DNANA_CMAKE_ENABLE_AUDIO:BOOL=ON \
	-G Ninja

%build
%ninja_build

%install
%ninja_install
