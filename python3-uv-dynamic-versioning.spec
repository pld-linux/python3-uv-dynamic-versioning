#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	uv-dynamic-versioning
Summary:	Dynamic versioning based on VCS tags for uv/hatch projects
Summary(pl.UTF-8):	Dynamiczne wersjonowanie na podstawie znaczników VCS dla projektów uv/hatch
Name:		python3-%{module}
Version:	0.14.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/uv-dynamic-versioning/
Source0:	https://files.pythonhosted.org/packages/source/u/uv-dynamic-versioning/uv_dynamic_versioning-%{version}.tar.gz
# Source0-md5:	31b72e92d7109418ce8cfbcdf0abb042
URL:		https://github.com/ninoseki/uv-dynamic-versioning
BuildRequires:	python3-build
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
%if %{with tests}
BuildRequires:	git-core
BuildRequires:	python3-dunamai >= 1.26.1
BuildRequires:	python3-dunamai < 1.27
BuildRequires:	python3-git
BuildRequires:	python3-hatchling >= 1.28
BuildRequires:	python3-hatchling < 2
BuildRequires:	python3-jinja2 >= 3.0
BuildRequires:	python3-jinja2 < 4
BuildRequires:	python3-pytest
BuildRequires:	python3-tomlkit >= 0.13
BuildRequires:	python3-tomlkit < 1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dynamic versioning based on VCS tags for uv/hatch projects. It is a
Hatch build plugin: a version source deriving the project version from
VCS tags (via dunamai) and a metadata hook substituting the version
into dependency specifications.

%description -l pl.UTF-8
Dynamiczne wersjonowanie na podstawie znaczników VCS dla projektów
uv/hatch. Jest to wtyczka budowania Hatcha: źródło wersji, określające
wersję projektu na podstawie znaczników VCS (przy użyciu modułu
dunamai), oraz hak metadanych, wstawiający wersję do specyfikacji
zależności.

%prep
%setup -q -n uv_dynamic_versioning-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
install -d test-home
export HOME=$(pwd)/test-home
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=test@example.com
export GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=test@example.com
# tests tag the current directory's repository, expecting an upstream checkout
git init -q
git add -A
git commit -q -m sdist
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md docs/*.md
%attr(755,root,root) %{_bindir}/uv-dynamic-versioning
%{py3_sitescriptdir}/uv_dynamic_versioning
%{py3_sitescriptdir}/uv_dynamic_versioning-%{version}.dist-info
