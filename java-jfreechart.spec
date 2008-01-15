# TODO
# - -demo not built
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
#
Summary:	Charts Generation library
Summary(pl.UTF-8):	Biblioteka do generowania wykresów
Name:		jfreechart
Version:	1.0.7
Release:	0.1
License:	LGPL
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/jfreechart/%{name}-%{version}.tar.gz
# Source0-md5:	4967a55ef939ae60a18cd865e846f4cc
URL:		http://www.jfree.org/jfreechart/
BuildRequires:	ant
BuildRequires:	jcommon >= 1.0.12
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	junit
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	servlet
BuildRequires:	xml-commons-apis
Requires:	jcommon >= 0.9.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Free Java class library for generating charts.

%description -l pl.UTF-8
Wolnodostępna biblioteka klas Javy do generowania wykresów.

%package demo
Summary:	Demo for %{name}
Summary(pl.UTF-8):	Przykład użycia biblioteki %{name}
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jcommon
Requires:	servlet

%description demo
Demo for %{name}.

%description demo -l pl.UTF-8
Przykład użycia biblioteki %{name}.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja Javadoc do biblioteki %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc do biblioteki %{name}.

%prep
%setup -q
# remove all binary libs
find . -name '*.jar' | xargs rm -v

%build
%ant -f ant/build.xml \
	-Djunit.jar=%{_javadir}/junit.jar \
	-Djcommon.jar=%{_javadir}/jcommon.jar \
	-Dservlet.jar=%{_javadir}/servlet.jar \
	-Dgnujaxp.jar=%{_javadir}/xml-commons-apis.jar \
	-Dbuildstable=true -Dproject.outdir=. -Dbasedir=. \
	compile %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
install %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
#install %{name}-%{version}-demo.jar $RPM_BUILD_ROOT%{_javadir}

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc README.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar

%if 0
#somewhy not built
%files demo
%defattr(644,root,root,755)
%{_javadir}/%{name}-%{version}-demo.jar
%{_javadir}/%{name}-demo.jar
%endif

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
