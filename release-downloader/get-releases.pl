#!/usr/bin/env perl

use strict;

use Data::Dumper;
use Cwd qw(abs_path realpath getcwd);

sub cleanup{
	system("rm -f *.rpm");
}

my $yumdir = './etc/yum.repos.d/';
my $urls_file = 'urls.list';

# ========
my $relname = $ARGV[0];
my $dstdir = $ARGV[1] || "destroot";
my $dldir = $ARGV[2] || "test";
my $tmproot = $ARGV[3] || "tmp";
# ========

$dstdir = realpath $dstdir;
$dldir = realpath $dldir;
$tmproot = realpath $tmproot;

system("mkdir destroot test tmp");

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

# yumdownload
print "Resolving packages:\n\n";
#print "yumdownloader -c $ENV{PWD}/etc/yum.conf --urls --resolve AtlasOffline_21.0.19_x86_64-slc6-gcc49-opt > ./urls.txt";
my $extraPackages = "AtlasSetup CMake_3.6.0_Linux-x86_64-0-0";
system("yumdownloader -q -c $ENV{PWD}/etc/yum.conf --urls --resolve AtlasOffline_21.0.15_x86_64-slc6-gcc49-opt $extraPackages > ./urls.list");
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

print getcwd . "\n";

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
	last if getcwd() ne $tmproot;
	print "Cleaning TMPROOT";
	system("rm -rf ./*");
	#last;
}
