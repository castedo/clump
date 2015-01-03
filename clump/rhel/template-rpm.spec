Summary:        $summary
Name:           $name
Version:        $version
Release:        $release.0%{?dist}
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
%{__python2} -m "clump.rpmlistfiles" %{buildroot} $unlistfiles > clump-out.txt

%clean
rm -rf %{buildroot}

%files -f clump-out.txt
%defattr(-,root,root,-)

%changelog
$changelog
