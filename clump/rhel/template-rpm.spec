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
clump list-files %{buildroot} > clump-list-files-output.txt

%clean
rm -rf %{buildroot}

%files -f clump-list-files-output.txt
%defattr(-,root,root,-)

%changelog
$changelog
