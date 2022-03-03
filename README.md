# CS131 Project Sample Grading Script
* Maintained and updated on [CS131 TA Organization Reporitory](https://github.com/CS131-TA-team/CS131-Project-Sample-Grading-Script) since Winter 2020.
* This particular version is for CS131 Winter 22 quarter
* This is not really a grading script because you didn't see any grading
* The evaluation giving you True / False something is somewhat partial credits for each task
* This is the simplest version of the core part of the grading script, but it doesn't contain any real test case
* You may regard it as a super client (who has the power of starting a server) as well.
* You expect a decent score if you see correct results for all the test cases here. But there's no guarantee; feel free to add your own test cases using the API functions. In addition, this script tests the coding part only. You are also expected to write the report as requested in the spec.

## Background
- This is for [UCLA CS131 (**Programming Languages**)](http://web.cs.ucla.edu/classes/winter21/cs131/index.html) [**Project**](http://web.cs.ucla.edu/classes/winter21/cs131/hw/pr.html) (instructor: [Prof. Paul Eggert](http://web.cs.ucla.edu/classes/winter21/cs131/mail-eggert.html))
- This project is on Python, specifically aiming at the use of [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
- To complete the project a Google Map API Key is needed, I tried, in order to get rid of the limit you need payment information attached.



## Usage
* put your ```server.py``` and all other needed ```.py``` files under the [**sample_submission**](./sample_submission) folder
* modify the port number in ```client_basic.py```. Follow [port assignment](https://piazza.com/class/kxxz3gx4ppy4sn?cid=225) 
* could run single evaluation by
    ```shell
    python3 client_basic.py
    ```
* This script has been tested on both mac and linux; not tested on Windows

## Resource and Acknowledgement
- Thanks to previous-year TA, Wenhao and Patricia's code
- Following [discussion online](https://stackoverflow.com/questions/3855127/find-and-kill-process-locking-port-3000-on-mac), to kill the process occupying port 8000 we could run: 
    ```shell
    lsof -ti:8000 | xargs kill
    ```
- To run a script in the background I used *nohup*
- To execute [command line within Python](https://stackoverflow.com/questions/450285/executing-command-line-programs-from-within-python):
    ```shell
    import os
    os.system('sox input.wav -b 24 output.aiff rate -v -L -b 90 48k')
    ```
- Some hint code from previous year is available in this [hint code repo](https://github.com/CS131-TA-team/UCLA_CS131_CodeHelp/tree/master/Python)


## About organizing log files
You might want to have a look at [os.mkdir](https://www.tutorialspoint.com/python/os_mkdir.htm) and [os.path.exists](https://www.geeksforgeeks.org/python-os-path-exists-method/)

## What kind of submission is safe?
If you unzip your files into the [sample_submission](./sample_submission) folder, with no extra effort required (e.g. don't need to create an empty folder manually, etc.), we can always make ```client_basic``` run (I mean if you occupy others' port then it is not guaranteed to work).

