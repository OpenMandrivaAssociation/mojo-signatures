
%undefine _compress
%undefine _extension
%global _duplicate_files_terminate_build 0
%global _files_listed_twice_terminate_build 0
%global _unpackaged_files_terminate_build 0
%global _nonzero_exit_pkgcheck_terminate_build 0
%global _use_internal_dependency_generator 0
%global __find_requires /bin/sed -e 's/.*//'
%global __find_provides /bin/sed -e 's/.*//'

Epoch:          1
Name:		mojo-signatures
Version:	1.1
Release:	0.11.svn11457.1
License:	GPLv3+
Source0:	mojo-signatures-1.1-0.11.svn11457.0-omv2014.0.noarch.rpm

URL:		https://abf.rosalinux.ru/openmandriva/mojo-signatures
BuildArch:	noarch
Summary:	mojo-signatures bootstrap version
#Requires:	javapackages-bootstrap
Requires:	jpackage-utils
Requires:	maven
Provides:	mojo-signatures = 1.1-0.11.svn11457.0:2014.0
Provides:	mvn(org.codehaus.mojo.signature:java15) = 1.1-SNAPSHOT
Provides:	mvn(org.codehaus.mojo.signature:java15:pom:) = 1.1-SNAPSHOT
Provides:	mvn(org.codehaus.mojo.signature:java16) = 1.1-SNAPSHOT
Provides:	mvn(org.codehaus.mojo.signature:java16:pom:) = 1.1-SNAPSHOT

%description
mojo-signatures bootstrap version.

%files
/usr/share/java/mojo-signatures
/usr/share/java/mojo-signatures/java15-1.1.signature
/usr/share/java/mojo-signatures/java15.signature
/usr/share/java/mojo-signatures/java16-1.1.signature
/usr/share/java/mojo-signatures/java16.signature
/usr/share/maven-fragments/mojo-signatures
/usr/share/maven-poms/JPP.mojo-signatures-java15.pom
/usr/share/maven-poms/JPP.mojo-signatures-java16.pom
/usr/share/maven-poms/JPP.mojo-signatures-parent.pom

#------------------------------------------------------------------------
%prep

%build

%install
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -id
