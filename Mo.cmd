@echo off
echo.
hg pull -u
echo.
echo.
SortFilters.exe -a Adversity.txt
SortFilters.exe -a Antisocial.txt
SortFilters.exe -a Extreme-Measures.txt
perl addChecksum.pl Adversity.txt
perl addChecksum.pl Antisocial.txt
perl addChecksum.pl Extreme-Measures.txt
hg commit -m "%*"
echo.
hg push
echo.
echo.
hg heads
