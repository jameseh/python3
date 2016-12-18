#python3 scripts




## apodw.py

### Download and set the the lastest APOD (Astronomy Picture of the Day) from http://apod.nasa.gov, as wallpaper with feh, pass if the APOD is already in library.

#### Usage:
```Depends on feh, and third party module requests. Intended to be automatically ran daily.```





## findf.py

###Find all files in recursively from [DIRECTORY_PATH], sort and display the [NUMBER_OF_FILES] specified.

####Usage:
```./findf.py [DIRECTORY_PATH] [NUMBER_OF_FILES] [OPTIONAL] ...```
####Example:
```./findf.py /home 10 --pd /dev,/sys,/proc --ere 'regex'```

#####Mandatory args:
```
[DIRECTORY_PATH]       - Positional argument, full path of directory so search.
[NUMBER_OF_FILES]      - Positional argument, number of files to display.
```

#####Optional args:
```
--mre                  - Display only filenames or paths matching regex.
--ere                  - Exclude all filenames or paths matching regex.

--pd                   - Pass if directory starts with.
--pf                   - Pass if file ends with.
--pdre                 - Pass if directory matches regex.
--pfre                 - Pass if file matches regex.

--sd                   - Search only in directories starting with.
--sf                   - Show only files ending with.
--sdre                 - Search only directories matching regex.
--sfre                 - Show only files matching regex.
````
