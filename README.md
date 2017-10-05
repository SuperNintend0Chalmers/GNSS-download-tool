# GNSS-download-tool

This tool will download RINEX data from the NOAA CORS database to the
directory.


To download a file, the python script is needed 
to be called in the following manner:
```angular2html
grab.py -b <BasesationID> -s <StartTime> -e <endTime>
grab.py --base <BasesationID> --start <StartTime> --end <endTime>
```
***

####Example

```
grab.py -b nybp -s 2017-10-04T00:00:00Z -e 2017-10-04T04:00:00Z
```


`grab.py` calls the python script, this is to be 
followed by series of 
tags and data for the script to run


`-b` is the tag used to input the **basestation ID**, in the above example it is 
basesation **nybp**

`-s` is the tag used to input the **Start Time**, this need to be
entered in ISO8061 format (YYYY-mm-dd __T__ HH:MM:ss __Z__). For the above 
example the start time is **2017-10-04T00:00:00Z**

`-e` is the tag used to input the **End Time**, this need to be
entered in ISO8061 format (YYYY-mm-dd __T__ HH:MM:ss __Z__). For the above 
example the end time is **2017-10-04T04:00:00Z**

---
##Requirements
Please be advised that, **teqc** needs to 
installed system wide **i.e (in system PATH)** for 
this tool to work. Future updates to this tool will detect if teqc is 
installed, and if not  present. The install will download and install the tool in system path.

Currently teqc can be downloaded for a variety of operating environment, 
please visit the following [link](https://www.unavco.org/software/data-processing/teqc/teqc.html)