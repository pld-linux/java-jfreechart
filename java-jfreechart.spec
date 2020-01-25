# TODO
# - -demo not built
# - build/package experimental classes (?)

# Conditional build:
%bcond_without	javadoc		# don't build javadoc


%define		srcname		jfreechart
Summary:	Charts Generation library
Summary(pl.UTF-8):	Biblioteka do generowania wykresów
Name:		java-jfreechart
Version:	1.0.7
Release:	1
License:	LGPL
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/jfreechart/%{srcname}-%{version}.tar.gz
# Source0-md5:	4967a55ef939ae60a18cd865e846f4cc
URL:		http://www.jfree.org/jfreechart/
BuildRequires:	ant
BuildRequires:	java-jcommon
BuildRequires:	java-junit
BuildRequires:	java-servletapi
BuildRequires:	jdk
BuildRequires:	java-xml-commons
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-jcommon
Requires:	java-xml-commons
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Free Java class library for generating charts.

%description -l pl.UTF-8
Wolnodostępna biblioteka klas Javy do generowania wykresów.

%package demo
Summary:	Demo for %{srcname}
Summary(pl.UTF-8):	Przykład użycia biblioteki %{srcname}
Group:		Development/Languages/Java
Requires:	%{srcname} = %{version}-%{release}
Requires:	jcommon
Requires:	servlet

%description demo
Demo for %{srcname}.

%description demo -l pl.UTF-8
Przykład użycia biblioteki %{srcname}.

%package javadoc
Summary:	Javadoc for %{srcname}
Summary(pl.UTF-8):	Dokumentacja Javadoc do biblioteki %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc do biblioteki %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}
# remove all binary libs
find . -name '*.jar' | xargs rm -v

%build
JUNIT_JAR=$(find-jar junit)
JCOMMON_JAR=$(find-jar jcommon)
SERVLET_JAR=$(find-jar servlet-api)
XML_COMMONS_APIS_JAR=$(find-jar xml-commons-apis)

%ant -f ant/build.xml \
	-Djunit.jar=$JUNIT_JAR \
	-Djcommon.jar=$JCOMMON_JAR \
	-Dservlet.jar=$SERVLET_JAR \
	-Dgnujaxp.jar=$XML_COMMONS_APIS_JAR \
	-Dbuildstable=true -Dproject.outdir=. -Dbasedir=. \
	compile %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
install %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar
#install %{srcname}-%{version}-demo.jar $RPM_BUILD_ROOT%{_javadir}

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc README.txt
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if 0
#somewhy not built
%files demo
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-%{version}-demo.jar
%{_javadir}/%{srcname}-demo.jar
%endif

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
