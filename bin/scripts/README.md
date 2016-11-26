# python3 scripts



## FindLargest.py

###Find all files in recursively from [DIRECTORY_PATH], sort and display the [NUMBER_OF_FILES] specified.

####Usage:
```./FindLargest.py [DIRECTORY_PATH] [NUMBER_OF_FILES] [OPTIONAL] ...```
####Example:
```./FindLargest.py /home 10 --pd=/dev,/sys,/proc --pf=".tbz2" --ere='^.+somepattern+.$'```

#####Mandatory args:
```
[DIRECTORY_PATH]                           - Positional argument, full path of directory so search.
[NUMBER_OF_FILES]                          - Positional argument, number of files to display.
```

#####Optional args:
```
--pd                                       - Pass if directory starts with (full path).
--pf                                       - Pass if file ends with.
--pdre                                     - Pass if directory matches regex.
--pfre                                     - Pass if file matches regex.
--mre                                      - Display only filenames or paths matching regex.
--ere                                      - Exclude all filenames or paths matching regex.
````
