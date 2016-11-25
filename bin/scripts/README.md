# python3 scripts



## FindLargest.py

###Find all files in recursively from [DIRECTORY PATH], sort and display the [NUMBER OF FILES] specified.

####Usage:
```./FindLargest.py [DIRECTORY PATH] [NUMBER OF FILES] [OPTIONAL] ...```
####Example:
```./FindLargest.py /home 10 --pd=/dev,/sys,/proc --ere='^.+somepattern+.$'```

#####Mandatory args:
```
[DIRECTORY]                                - Positional argument, full path of directory so search.
[NUMBER_OF_FILES]                          - Positional argument, number of files to display.
```

#####Optional args:
```
--pd                                       - Pass if directory starts with.
--pf                                       - Pass if file ends with.
--pdre                                     - Pass if directory matches regex.
--pfre                                     - Pass if file matches regex.
--mre                                      - Display only filenames or paths matching regex.
--ere                                      - Exclude all filenames or paths matching regex.
````
