@echo.
@echo.
join.py Adversity.txt Antisocial.txt Extreme-Measures.txt Adversity-Combined.txt
@echo.
@echo.
SortFilters.py Adversity.txt
SortFilters.py Antisocial.txt
SortFilters.py Extreme-Measures.txt
SortFilters.py Adversity-Combined.txt
@echo.
@echo Finished sorting...
@echo.
perl addChecksum.pl Adversity.txt
perl addChecksum.pl Antisocial.txt
perl addChecksum.pl Extreme-Measures.txt
perl addChecksum.pl Adversity-Combined.txt
@echo.
@echo Finished adding checksum
@echo.
cmd /k
@echo.
@echo.

