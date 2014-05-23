  binmode(FILE);
  binmode(FILE);
  close(FILE);
  close(FILE);
  exit 0;
  local $/;
  my $file = shift;
  my $result = <FILE>;
  my ($file, $contents) = @_;
  open(local *FILE, "<", $file) || die "Could not read file '$file'";
  open(local *FILE, ">", $file) || die "Could not write file '$file'";
  print FILE $contents;
  return $result;
#
#
#
#                                                                           #
#                                                                           #
#                                                                           #
#                                                                           #
#      http://www.apache.org/licenses/LICENSE-2.0
#   perl addChecksum.pl subscription.txt                                    #
# #!/usr/bin/perl
# Calculate new checksum
# Calculate new checksum: remove all CR symbols and empty
# checksums and date and time of last modification to downloadable          #
# Copyright 2011 Wladimir Palant
# distributed under the License is distributed on an "AS IS" BASIS,
# download and checksum mismatches(broken downloads) will be rejected.      #
# Get existing checksum.
# If the old checksum matches the new one bail.
# Insert checksum into the file
# Licensed under the Apache License, Version 2.0 (the "License");
# limitations under the License.
# lines and get an MD5 checksum of the result (base64-encoded,
# Note: your subscription file should be saved in UTF-8 encoding, otherwise #
# Recalculate the checksum as we've altered the date.
# Remove already existing checksum.
# See the License for the specific language governing permissions and
# subscriptions. The checksum will be validated by Adblock Plus on          #
# the generated checksum might be incorrect.                                #
# This is a slightly modified version of the reference script to add        #
# To add a checksum to a subscription file, run the script like this:       #
# Unless required by applicable law or agreed to in writing, software
# Update the date and time.
# without the trailing = characters).
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#############################################################################
#############################################################################
$checksum = md5_base64($checksumData);
$checksumData = $data;
$checksumData =~ s/\n+/\n/g;
$checksumData =~ s/\n+/\n/g;
$checksumData =~ s/\r//g;
$checksumData =~ s/\r//g;
$data =~ /^.*!\s*checksum[\s\-:]+([\w\+\/=]+).*\n/gmi;
$data =~ s/(!.*Updated:\s*)([^\r\n]*)(\r?\n)/$1$dat$3/;
$data =~ s/(\r?\n)/$1! Checksum: $checksum$1/;
$data =~ s/^.*!\s*checksum[\s\-:]+([\w\+\/=]+).*\n//gmi;
$year += 1900; # Year is years since 1900.
die "Usage: $^X $0 subscription.txt\n" unless @ARGV;
elsif ($hour >= 13) {$hour -= 12; }
if ($checksum eq $oldchecksum)
if ($hour == 0)     {$hour = 12;  }
if ($hour >= 12)    {$ampm = "PM";}
my $ampm = "AM";
my $checksum = md5_base64($checksumData);
my $checksumData = $data;
my $dat = sprintf("$mday $months[$mon] $year (%d:%02d:%02d $ampm)", $hour, $min, $sec);
my $data = readFile($file);
my $file = $ARGV[0];
my $oldchecksum = $1;
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
my @months = qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
sub readFile
sub writeFile
use Digest::MD5 qw(md5_base64);
use strict;
use warnings;
writeFile($file, $data);
{
{
{
}
}
}
