Summary:        $summary
Name:           $name
Version:        $version
Release:        0%{?dist}
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
$buildarch
$sources
$requires

%description
$description

%prep
$prep
mkdir clumpiled
%{__python} -m clump.clumpile

%build
$build

%install
rm -rf %{buildroot}
$install
%{__python} -m clump.rpmlistfiles %{buildroot} > clumpiled/files.txt

%post
$post

%clean
rm -rf %{buildroot}

%files -f clumpiled/files.txt
%defattr(-,root,root,-)

%changelog
$changelog
