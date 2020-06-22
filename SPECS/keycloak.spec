%define debug_package %{nil}
%define __jar_repack %{nil}
%define __brp_ldconfig %{nil}

Name:        keycloak
Version:     10.0.2
Release:     1%{?dist}
Summary:     SSO, Identity and Access Management software

License:     ASL 2.0
URL:         https://www.keycloak.org/
Source0:     https://downloads.jboss.org/%{name}/{%version}/%{name}-%{version}.tar.gz
Source1:     %{name}.service
Source2:     wildfly.conf
Source3:     launch.sh

Provides:    java-headless >= 1:1.8

%description
Keycloak is an open source software product to allow single sign-on with
Identity Management and Access Management aimed at modern applications
and services

%prep
%setup -c

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 %{buildroot}/opt/%{name}
tar --strip-components=1 -C %{buildroot}/opt/%{name} -xvf %{SOURCE0}
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -d -m 0755 %{buildroot}/etc/%{name}
install -m 0644 %{SOURCE2} %{buildroot}/etc/%{name}
install -m 0744 %{SOURCE3} %{buildroot}/opt/%{name}/bin/
install -d -m 0755 %{buildroot}%{_localstatedir}/run/%{name}
chrpath --delete %{buildroot}/opt/keycloak/modules/system/layers/base/org/wildfly/openssl/main/lib/solaris-x86_64/libwfssl.so


%pre
/usr/bin/getent group %{name} > /dev/null || /usr/sbin/groupadd -r %{name}
/usr/bin/getent passwd %{name} > /dev/null || /usr/sbin/useradd -r -d /opt/%{name} -s /sbin/nologin -g %{name} %{name}

%files
%defattr(-,%{name},%{name},-)
%attr(-,root,root) %{_unitdir}/%{name}.service
%attr(-,root,root) /etc/%{name}/wildfly.conf
/opt/%{name}
/opt/%{name}/bin/launch.sh
%{_localstatedir}/run/%{name}

%changelog
* Mon Jun 22 2020 Edouard Camoin <edouard.camoin@gmail.com> 10.0.2-1
  - Factoring file attributes
  - Changing java artifact name

* Thu Jun 18 2020 Edouard Camoin <edouard.camoin@gmail.com> 10.0.2-1
  - Adding requirements for java-openjdk >= 8

* Wed Jun 17 2020 Edouard Camoin <edouard.camoin@gmail.com> 10.0.2-1
  - Adding service configuration file

* Mon Jun 15 2020 Edouard Camoin <edouard.camoin@gmail.com> 10.0.2-1
  - Initial specfile
