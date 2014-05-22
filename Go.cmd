REM publish.py
hg pull -u
@echo.
SortFilters.exe Adversity.txt
SortFilters.exe Antisocial.txt
SortFilters.exe Extreme-Measures.txt
perl addChecksum.pl Adversity.txt
perl addChecksum.pl Antisocial.txt
perl addChecksum.pl Extreme-Measures.txt
@echo.
hg commit -m "%*"
hg push
@echo.
hg heads