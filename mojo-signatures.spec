%{?_javapackages_macros:%_javapackages_macros}
Name:           mojo-signatures
Version:        1.1
Release:        0.11.svn11457.0%{?dist}
Summary:        Mojo API signatures project


License:        MIT
URL:            http://mojo.codehaus.org/

# we are using svn because upstream doesn't provide source tarballs
# and we want to have all available signatures together anyway (just
# in case)
# svn export http://svn.codehaus.org/mojo/trunk/signatures -r11457 mojo-signatures-1.1
# tar caf mojo-signatures-1.1.tar.xz mojo-signatures-1.1
Source0:        %{name}-%{version}.tar.xz

Patch0:         0001-pom.xml-files.patch
BuildArch:      noarch


# specific release required for objectweb-asm dependency in pom.xml
BuildRequires:  animal-sniffer >= 1.6-3
BuildRequires:  jpackage-utils
BuildRequires:  maven-local
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-plugin-cobertura
BuildRequires:  objectweb-asm
BuildRequires:  mojo-parent

# we should probably generate java15 signature with 1.5 jdk, but this
# doesn't work with gcj. The signatures are probably incorrect because
# of this, but at least they exist and noone complained yet :-)


# specific release required for handling "signature" packaging
Requires:       maven
Requires:       jpackage-utils

%description
The API Signatures project contains a number of projects which
generate signatures of various APIs, such as the Java Runtime. These
signatures are generated by and consumed by the Animal Sniffer
project.

%prep
%setup -q
%patch0 -p1

%build
pushd signatures-parent
mvn-rpmbuild install
popd

for sig in java15 java16;do
    pushd $sig
    mvn-rpmbuild install
    popd
done

%install
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadir}/%{name}

install -pm 644 signatures-parent/pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}-parent.pom

for sig in java15 java16;do
   pushd $sig
      install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-$sig.pom
      install -pm 644 target/*signature %{buildroot}%{_javadir}/%{name}/$sig-%{version}.signature
      %add_to_maven_depmap org.codehaus.mojo.signature $sig %{version} JPP/%{name} $sig
   popd
done

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for sig in *-%{version}*; do ln -sf ${sig} `echo $sig| sed "s|-%{version}||g"`; done)


%files
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/%{name}



%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.11.svn11457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1-0.10.svn11457
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-0.9.svn11457
- Remove excessive requires: mojo-parent

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.8.svn11457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-0.7.svn11457
- Port to Java 1.7.0
- Resolves 824417

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.6.svn11457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 9 2011 Alexander Kurtakov <akurtako@redhat.com> 1.1-0.5.svn11457
- Build with maven 3.x.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.4.svn11457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-0.3.svn11457
- Add mojo-parent to Requires

* Thu Sep 30 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-0.2.svn11457
- Add mojo-parent to BRs

* Fri Sep 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-0.1.svn11457
- Initial version of package
