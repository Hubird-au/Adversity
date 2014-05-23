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
addChecksum.py Adversity.txt
addChecksum.py Antisocial.txt
addChecksum.py Extreme-Measures.txt
addChecksum.py Adversity-Combined.txt
@echo.
@echo Finished adding checksum
@echo.
cmd /k
@echo.
@echo.

