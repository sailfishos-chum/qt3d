%global qt_version 5.15.14

Summary: Qt5 - Qt3D QML bindings and C++ APIs
Name:    opt-qt5-qt3d
Version: 5.15.14
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://doc.qt.io/qt-5/licensing.html
License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: %{name}-%{version}.tar.bz2

%{?opt_qt5_default_filter}

BuildRequires: make
BuildRequires: opt-qt5-rpm-macros >= %{qt_version}
BuildRequires: opt-qt5-qtbase-static >= %{qt_version}
BuildRequires: opt-qt5-qtbase-private-devel
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel
BuildRequires: opt-qt5-qtimageformats
BuildRequires: opt-qt5-qtxmlpatterns-devel
Requires: opt-qt5-qtimageformats%{?_isa} >= %{qt_version}
Requires: opt-qt5-qtdeclarative >= %{qt_version}
Requires: opt-qt5-qtbase-gui >= %{qt_version}

%description
Qt 3D provides functionality for near-realtime simulation systems with
support for 2D and 3D rendering in both Qt C++ and Qt Quick applications).

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream


%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%define _lto_cflags %{nil}

export QTDIR=%{_opt_qt5_prefix}
touch .git

%{opt_qmake_qt5}

# have to restart build several times due to bug in sb2
%make_build  -k || chmod -R ugo+r . || true
%make_build

# bug in sb2 leading to 000 permission in some generated plugins.qmltypes files
chmod -R ugo+r .

%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.GPL* LICENSE.LGPL*
%{_opt_qt5_libdir}/libQt53DQuick.so.5*
%{_opt_qt5_libdir}/libQt53DInput.so.5*
%{_opt_qt5_libdir}/libQt53DQuickRender.so.5*
%{_opt_qt5_libdir}/libQt53DRender.so.5*
%{_opt_qt5_libdir}/libQt53DCore.so.5*
%{_opt_qt5_libdir}/libQt53DLogic.so.5*
%{_opt_qt5_libdir}/libQt53DQuickInput.so.5*
%{_opt_qt5_libdir}/libQt53DExtras.so.5*
%{_opt_qt5_libdir}/libQt53DAnimation.so.5*
%{_opt_qt5_libdir}/libQt53DQuickAnimation.so.5*
%{_opt_qt5_libdir}/libQt53DQuickScene2D.so.5*
%{_opt_qt5_libdir}/libQt53DQuickExtras.so.5*
%{_opt_qt5_qmldir}/Qt3D/
%{_opt_qt5_qmldir}/QtQuick/Scene3D/
%{_opt_qt5_qmldir}/QtQuick/Scene2D/
%{_opt_qt5_plugindir}/renderers/
%{_opt_qt5_plugindir}/sceneparsers/
%{_opt_qt5_plugindir}/renderplugins/
%{_opt_qt5_plugindir}/geometryloaders/

%files devel
%{_opt_qt5_bindir}/qgltf
%{_opt_qt5_libdir}/libQt53DQuick.so
%{_opt_qt5_libdir}/libQt53DQuick.prl
%{_opt_qt5_libdir}/cmake/Qt53DQuick
%{_opt_qt5_includedir}/Qt3DQuick
%{_opt_qt5_libdir}/pkgconfig/Qt53DQuick.pc
%{_opt_qt5_libdir}/libQt53DInput.so
%{_opt_qt5_libdir}/libQt53DInput.prl
%{_opt_qt5_libdir}/cmake/Qt53DInput
%{_opt_qt5_includedir}/Qt3DInput/
%{_opt_qt5_libdir}/pkgconfig/Qt53DInput.pc
%{_opt_qt5_libdir}/libQt53DCore.so
%{_opt_qt5_libdir}/libQt53DCore.prl
%{_opt_qt5_libdir}/cmake/Qt53DCore/
%{_opt_qt5_includedir}/Qt3DCore/
%{_opt_qt5_libdir}/pkgconfig/Qt53DCore.pc
%{_opt_qt5_libdir}/libQt53DQuickRender.so
%{_opt_qt5_libdir}/libQt53DQuickRender.prl
%{_opt_qt5_libdir}/cmake/Qt53DQuickRender/
%{_opt_qt5_includedir}/Qt3DQuickRender/
%{_opt_qt5_libdir}/pkgconfig/Qt53DQuickRender.pc
%{_opt_qt5_libdir}/libQt53DRender.so
%{_opt_qt5_libdir}/libQt53DRender.prl
%{_opt_qt5_libdir}/cmake/Qt53DRender/
%{_opt_qt5_includedir}/Qt3DRender/
%{_opt_qt5_libdir}/pkgconfig/Qt53DRender.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/*.pri
%{_opt_qt5_libdir}/libQt53DLogic.so
%{_opt_qt5_libdir}/libQt53DLogic.prl
%{_opt_qt5_includedir}/Qt3DLogic/
%{_opt_qt5_libdir}/cmake/Qt53DLogic
%{_opt_qt5_libdir}/pkgconfig/Qt53DLogic.pc
%{_opt_qt5_libdir}/libQt53DQuickInput.so
%{_opt_qt5_libdir}/libQt53DQuickInput.prl
%{_opt_qt5_includedir}/Qt3DQuickInput/
%{_opt_qt5_libdir}/cmake/Qt53DQuickInput
%{_opt_qt5_libdir}/pkgconfig/Qt53DQuickInput.pc
%{_opt_qt5_libdir}/libQt53DExtras.so
%{_opt_qt5_libdir}/libQt53DExtras.prl
%{_opt_qt5_libdir}/cmake/Qt53DExtras
%{_opt_qt5_includedir}/Qt3DExtras
%{_opt_qt5_libdir}/pkgconfig/Qt53DExtras.pc
%{_opt_qt5_libdir}/libQt53DQuickExtras.so
%{_opt_qt5_libdir}/libQt53DQuickExtras.prl
%{_opt_qt5_libdir}/cmake/Qt53DQuickExtras
%{_opt_qt5_includedir}/Qt3DQuickExtras
%{_opt_qt5_libdir}/pkgconfig/Qt53DQuickExtras.pc
%{_opt_qt5_libdir}/libQt53DAnimation.so
%{_opt_qt5_libdir}/libQt53DAnimation.prl
%{_opt_qt5_libdir}/cmake/Qt53DAnimation
%{_opt_qt5_includedir}/Qt3DAnimation
%{_opt_qt5_libdir}/pkgconfig/Qt53DAnimation.pc
%{_opt_qt5_libdir}/libQt53DQuickAnimation.so
%{_opt_qt5_libdir}/libQt53DQuickAnimation.prl
%{_opt_qt5_libdir}/cmake/Qt53DQuickAnimation
%{_opt_qt5_includedir}/Qt3DQuickAnimation
%{_opt_qt5_libdir}/pkgconfig/Qt53DQuickAnimation.pc
%{_opt_qt5_libdir}/libQt53DQuickScene2D.so
%{_opt_qt5_libdir}/libQt53DQuickScene2D.prl
%{_opt_qt5_libdir}/cmake/Qt53DQuickScene2D
%{_opt_qt5_includedir}/Qt3DQuickScene2D
%{_opt_qt5_libdir}/pkgconfig/Qt53DQuickScene2D.pc
