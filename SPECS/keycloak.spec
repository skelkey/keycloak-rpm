%define debug_package %{nil}

Name: keycloak
Version: 10.0.2
Release: 1%{?dist}
Summary: SSO, Identity and Access Management software

License: ASL 2.0
URL: https://www.keycloak.org/
Source0: https://downloads.jboss.org/%{name}/{%version}/%{name}-%{version}.tar.gz
Source1: %{name}.service

%description
Keycloak is an open source software product to allow single sign-on with
Identity Management and Access Management aimed at modern applications
and services

%prep
%setup -c

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 %{buildroot}/opt
install -d -m 0755 %{buildroot}/opt/%{name}
tar --strip-components=1 -C %{buildroot}/opt/%{name} -xvf %{SOURCE0}
install -m O755 %{name} %{buildroot}/opt
install -d -m 0755 %{buildroot}%{_unitdir}
install -m O644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service


%pre
/usr/bin/getent group %{name} > /dev/null || /usr/sbin/groupadd -r %{name}
/usr/bin/getent passwd %{name} > /dev/null || /usr/sbin/useradd -r -d /opt/%{name} -s /sbin/nologin -g %{name} %{name}

%files
%defattr(-,%{name},%{name},-)
%attr(-,{%name},%{name}) /opt/%{name}
%attr(-,root,root) %{_unitdir}/%{name}.service

%changelog
* Mon Jun 15 2020 Edouard Camoin <edouard.camoin@gmail.com> 10.0.2-1
  - Initial specfile
