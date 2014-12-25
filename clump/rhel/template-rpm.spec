Summary:        $summary
Name:           $name
Version:        $version
Release:        1%{?dist}
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
$buildarch
$sources
$requires

%description
$description

%prep
$prep

%build
$build

%install
rm -rf %{buildroot}
$install
clmp-files-list %{buildroot} > clmp-files-list-output.txt

%clean
rm -rf %{buildroot}

%files -f clmp-files-list-output.txt
%defattr(-,root,root,-)

%changelog
$changelog
