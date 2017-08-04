#!/usr/bin/env perl

use strict;

use Data::Dumper;
use Cwd qw(abs_path realpath getcwd);
use Getopt::Std;
use File::Spec;

sub cleanup{
	my $tmproot = shift;
	return 1 if not defined($tmproot) or $tmproot eq "";
	system("rm -rf $tmproot");
}

sub help{
	print "Usage: get-release.pl -d <destination_directory> [-c <cache_dir>] <release_name>
		where: <destination_directory> - release will be installed into \"<destination_directory>/<release_name>\"
			<cace_directory> - a place where cache data will be stored
			<release_name> - name of the release to be installed, e.g., AtlasOffline_21.0.19_x86_64-slc6-gcc49-opt\n
		Example:
			get-release.sh -d /lustre/atlas/proj-shared/csc108/app_dir/atlas_app/atlas_rel/release-test/  AtlasOffline_21.0.19_x86_64-slc6-gcc49-opt\n\n";
}

my $yumdir = './etc/yum.repos.d/';

# ========

my %options=();
getopts("hd:t:", \%options);

if(defined($options{h})){
	help;
	exit 0;
}


if(not defined($options{d})){
	print "Destination directory not specified\n";
	exit 1;
}

if(not defined($options{t})){
	print "Temporary directory not specified\n";
	exit 1;
}

my $relname = $ARGV[0];
#my $dstdir = $ARGV[1] || "destroot";
my $dstdir = "$options{d}/$relname";
#my $dldir = $ARGV[2] || "test";
my $dldir = "$options{t}/rpms";
#my $tmproot = $ARGV[3] || "tmp";
my $tmproot = "$options{t}/tmp";

if(not defined($relname)){
	print "No release name specified (e.g.: AtlasOffline_21.0.19_x86_64-slc6-gcc49-opt)\n";
	exit 0;
}
# ========

$dstdir = File::Spec->rel2abs($dstdir);
$dldir = File::Spec->rel2abs($dldir);
$tmproot = File::Spec->rel2abs($tmproot);
my $tmp = File::Spec->rel2abs($options{t});
my $urls_file = "$tmp/urls.list";

print "Installing $relname using $dstdir with temporary data in: $tmp\n";
print "Now reading local yum configuration\n";

opendir DIR, $yumdir; 
my @files = grep(/\.repo/,readdir DIR);
closedir DIR;

my %prefixes = {};

foreach my $file (@files){
	open my $fh, '<:encoding(UTF-8)', "$yumdir/$file" or die;
	my $prefix = "";
	my $baseurl = "";
	while (my $line = <$fh>) {
		if ($line =~ /name=/) {
			$baseurl='';
			$prefix='';
		}
		if ($line =~ /baseurl=/) {
			$line =~ s/^\s+|\s+$//g;
			$line =~ s/baseurl=//;
			$baseurl = $line; 
		}
		if ($line =~ /prefix=/) {
			$line =~ s/^\s+|\s+$//g;
			$line =~ s/prefix=//;
			$prefix = $line; 
		}
		if($prefix ne "" and $baseurl ne ""){
			$prefixes{$baseurl} = $prefix;
			$baseurl='';
			$prefix='';
		}
	}
	close $fh;
}
#print Dumper(\%prefixes);

# making directories
system("mkdir -p $dldir $dstdir $tmproot");

# yumdownload
print "Config read. Resolving packages.\n";
#print "yumdownloader -c $ENV{PWD}/etc/yum.conf --urls --resolve AtlasOffline_21.0.19_x86_64-slc6-gcc49-opt > ./urls.txt";
my $extraPackages = "AtlasSetup CMake_3.6.0_Linux-x86_64-0-0";
print("yumdownloader -q -c $ENV{PWD}/etc/yum.conf --urls --resolve $relname $extraPackages > $urls_file");
system("yumdownloader -q -c $ENV{PWD}/etc/yum.conf --urls --resolve $relname $extraPackages > $urls_file");
# 		or die("Unable to find release or resolve dependencies, check release name or network connectivity");
 
# parse url list, create prefix files
my @packages = ();

open my $fh, $urls_file;
while (my $line=<$fh>){
	chomp $line;
	my @pkg = ($line, '', ''); # link, prefix, file
	if($line =~ m/([^\/]+$)/){
		$pkg[2] = $1;
	}
	foreach my $k (keys %prefixes){
		if( index($line,$k) != -1){
			$pkg[1] = $prefixes{$k};
			last;
		}
	}
	push @packages, \@pkg;
}
close $fh;

chdir $tmproot;

print getcwd() . "\n";
print "$tmproot\n";

foreach my $pkg (@packages){
	my $fname = @$pkg[2];
	my $url = @$pkg[0];
	my $prefix = @$pkg[1];
	system("wget -O $dldir/$fname $url"); # or die("Failed to download $fname");
	print("wget -O $dldir/$fname $url"); # or die("Failed to download $fname");
	#my $relocation_root = `rpm -qip $dldir/$fname | grep Relocations | sed -n -e 's/\s*Relocations\s*:\s*//' -e 's!^/!!'`;
	my $relocation_root = `rpm -qp --queryformat "[%{prefixes}]" $dldir/$fname | sed -e 's!^/!!'`;
	
	# installing
	system("rpm2cpio $dldir/$fname | cpio -imdv");	
	system("mkdir -p $dstdir/$prefix/");
	print "Making:  $dstdir/$prefix/\n";
	#print("rpm2cpio $dldir/$fname | cpio -imdv\n");	
	system("cp -r ./$relocation_root/* $dstdir/$prefix/");
	print("cp -r ./$relocation_root/* $dstdir/$prefix/");
	#print("mv $relocation_root/* $dstdir/$prefix/\n");
	# cleanup tmproot
	#if(getcwd() ne $tmproot){
	#	print getcwd() . "!=$tmproot -> LAST!";
	#	last;
	#}
	print "Cleaning TMPROOT";
	system("rm -rf ./*");
	#last;
}

print "Cleaning up before exit";
#cleanup;
