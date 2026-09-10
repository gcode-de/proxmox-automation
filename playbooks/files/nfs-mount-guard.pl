#!/usr/bin/perl

use strict;
use warnings;

my ($vmid, $phase) = @ARGV;

exit 0 unless defined($phase) && $phase eq 'pre-start';
die "NFS mount guard: missing VMID\n" unless defined($vmid) && $vmid =~ /^\d+$/;

my $config_dir = $ENV{'PVE_LXC_CONFIG_DIR'} // '/etc/pve/lxc';
my $config = "$config_dir/$vmid.conf";

open(my $config_fh, '<', $config)
    or die "NFS mount guard: cannot read $config: $!\n";

while (my $line = <$config_fh>) {
    next unless $line =~ /^mp\d+:\s*([^,]+)(?:,|$)/;

    my $source = $1;
    next unless $source =~ m{^/mnt/nas(?:/|$)};

    open(my $findmnt_fh, '-|', '/usr/bin/findmnt', '-n', '-o', 'FSTYPE', '--target', $source)
        or die "NFS mount guard: cannot execute findmnt: $!\n";

    my @fstypes = <$findmnt_fh>;
    close($findmnt_fh);

    die "NFS mount guard: $source for CT $vmid is not backed by NFS; start aborted\n"
        unless grep { /^nfs(?:4)?\s*$/ } @fstypes;
}

close($config_fh);
exit 0;
