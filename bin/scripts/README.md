#python3 scripts




## fetch_apod.py

### Fetch APOD from apod.nasa.gov.

#### Usage: Meant to be used on a systemd timer or cron to run daily.




## set_wallpaper_apod.py

### Set walpaper with feh to the last APOD downloaded.

#### Usage: Depends on feh, intended to be started when you start your wm or de.




## FindLargest.py

###Find all files in recursively from [DIRECTORY_PATH], sort and display the [NUMBER_OF_FILES] specified.

####Usage:
```./FindLargest.py [DIRECTORY_PATH] [NUMBER_OF_FILES] [OPTIONAL] ...```
####Example:
```./FindLargest.py /home 10 --pd /dev,/sys,/proc --ere 'regex'```

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
