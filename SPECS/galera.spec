Name:           galera
Version:        25.3.32
Release:        1%{?dist}
Summary:        Synchronous multi-master wsrep provider (replication engine)

License:        GPLv2
URL:            http://galeracluster.com/

# Actually, the truth is, we do use galera source tarball provided by MariaDB on
# following URL (without macros):
#   https://archive.mariadb.org/mariadb-10.3.26/galera-25.3.31/src/galera-25.3.31.tar.gz

Source0:        http://releases.galeracluster.com/source/%{name}-%{version}.tar.gz

Source1:        garbd.service
Source2:        garbd-wrapper

Patch0:         galera-python3.patch

BuildRequires:  boost-devel check-devel openssl-devel python3-scons systemd gcc-c++ asio-devel
Requires:       nmap-ncat


Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
Galera is a fast synchronous multi-master wsrep provider (replication engine)
for transactional databases and similar applications. For more information
about wsrep API see http://launchpad.net/wsrep. For a description of Galera
replication engine see http://www.codership.com.


%prep
%setup -q
%patch0 -p1

%build
%{set_build_flags}

# Print help:
#   scons-3 --help
#   scons-3 -H

# Possibly usefull arguments:
#   --debug=findlibs
#   --debug=stacktrace
#   --warn=all
#   debug=0

%ifarch i686
scons-3 %{?_smp_mflags} strict_build_flags=0
%else
scons-3 %{?_smp_mflags} strict_build_flags=1
%endif



%install
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/garbd.service
install -D -m 755 %{SOURCE2} %{buildroot}%{_sbindir}/garbd-wrapper
install -D -m 755 garb/garbd %{buildroot}%{_sbindir}/garbd
install -D -m 755 libgalera_smm.so %{buildroot}%{_libdir}/galera/libgalera_smm.so
install -D -m 644 garb/files/garb.cnf %{buildroot}%{_sysconfdir}/sysconfig/garb
install -D -m 644 COPYING %{buildroot}%{_docdir}/galera/COPYING
install -D -m 644 chromium/LICENSE %{buildroot}%{_docdir}/galera/LICENSE.chromium
install -D -m 644 asio/LICENSE_1_0.txt %{buildroot}%{_docdir}/galera/LICENSE.asio
install -D -m 644 scripts/packages/README %{buildroot}%{_docdir}/galera/README
install -D -m 644 scripts/packages/README-MySQL %{buildroot}%{_docdir}/galera/README-MySQL


%post
/sbin/ldconfig
%systemd_post garbd.service

%preun
%systemd_preun garbd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart garbd.service


%files
%config(noreplace,missingok) %{_sysconfdir}/sysconfig/garb
%dir %{_docdir}/galera
%dir %{_libdir}/galera
%{_sbindir}/garbd
%{_sbindir}/garbd-wrapper
%{_unitdir}/garbd.service
%{_libdir}/galera/libgalera_smm.so
%doc %{_docdir}/galera/COPYING
%doc %{_docdir}/galera/LICENSE.asio
%doc %{_docdir}/galera/LICENSE.chromium
%doc %{_docdir}/galera/README
%doc %{_docdir}/galera/README-MySQL


%changelog
* Tue Mar 23 2021 Michal Schorm <mschorm@redhat.com> - 25.3.32-1
- Rebase to 25.3.32

* Tue Nov 10 2020 Michal Schorm <mschorm@redhat.com> - 25.3.31-1
- Rebase to 25.3.31
  Resolves: #1731289, #1856812

* Thu Jul 18 2019 Michal Schorm <mschorm@redhat.com> - 25.3.26-1
- Rebase to 25.3.26
  Resolves: #1687879
  Resolves: #1657220

* Mon Jul 16 2018 Honza Horak <hhorak@redhat.com> - 25.3.23-5
- Require asio also on rhel

* Fri Jul 13 2018 Honza Horak <hhorak@redhat.com> - 25.3.23-4
- Add explicit gcc-c++ BR
- Use python3-scons

* Fri Jul 13 2018 Honza Horak <hhorak@redhat.com> - 25.3.23-3
- Do not require asio on rhel

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 25.3.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 16 2018 Michal Schorm <mschorm@redhat.com> - 25.3.23-1
- Update to 25.3.23

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 25.3.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 24 2017 Honza Horak <hhorak@redhat.com> - 25.3.22-1
- Update to 25.3.22

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 25.3.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 25.3.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 25.3.16-4
- Rebuilt for Boost 1.64

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 25.3.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 18 2017 Jonathan Wakely <jwakely@redhat.com> - 25.3.16-2
- Use asio-devel instead of bundled asio library

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 25.3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 22 2016 Mike Bayer <mbayer@redhat.com> - 25.3.16-1
- Update to 25.3.16

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 25.3.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 25.3.12-3
- Rebuilt for Boost 1.60

* Wed Sep 30 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 25.3.12-2
- Remove use of -mtune=native which breaks build on secondary architectures

* Fri Sep 25 2015 Richard W.M. Jones <rjones@redhat.com> - 25.3.12-1
- Update to 25.3.12.
- Should fix the build on 32 bit ARM (RHBZ#1241164).
- Remove ExcludeArch (should have read the BZ more closely).

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 25.3.10-5
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 25.3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 25.3.10-3
- rebuild for Boost 1.58

* Wed Jul 08 2015 Ryan O'Hara <rohara@redhat.com> - 25.3.10-2
- Disable ARM builds (#1241164, #1239516)

* Mon Jul 06 2015 Ryan O'Hara <rohara@redhat.com> - 25.3.10-1
- Update to version 25.3.10

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 25.3.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 25.3.5-10
- Rebuild for boost 1.57.0

* Thu Nov 27 2014 Richard W.M. Jones <rjones@redhat.com> - 25.3.5-9
- Add aarch64 support.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 25.3.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 25.3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 25.3.5-6
- Rebuild for boost 1.55.0

* Wed Apr 30 2014 Dan Horák <dan[at]danny.cz> - 25.3.5-5
- set ExclusiveArch

* Thu Apr 24 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.5-4
- Use strict_build_flags=0 to avoid -Werror
- Remove unnecessary clean section

* Thu Apr 24 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.5-3
- Include galera directories in file list
- Set CPPFLAGS to optflags

* Wed Apr 23 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.5-2
- Fix client certificate verification (#1090604)

* Thu Mar 27 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.5-1
- Update to version 25.3.5

* Mon Mar 24 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.3-2
- Add systemd service

* Sun Mar 09 2014 Ryan O'Hara <rohara@redhat.com> - 25.3.3-1
- Initial build
