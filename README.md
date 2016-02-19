# DriveIt
DriveIt is a new crawler supports multiple websites, for now it supports http://comic.ck101.com and http://www.dm5.com
## Overview
This project is still under development. However, you can still run it with ```Python 3``` and it will work fine. More features will be added later.
## Usage
Simply run it with ```Python 3```. You may need to install some dependencies from PyPi.
```
sudo pip3 install Naked beautifulsoup4
```
Then you should be able to run it happily. To start, type 
```
python3 driveit.py
```
and input the site address of the flyleaf when asked.

For example:
![eg](http://i.imgur.com/Yex2M61.png)

Or if you prefer GUI to CLI:
```
python3 driveit-gui.py
```
Note you need to have PyQt5 installed to use the GUI version. For Mac users, you can install it via
```
brew install pyqt5
```
For example:
![eg_gui](http://i.imgur.com/OCl92j5.png)

It can automatically creates subfolders followed by __chapters__ or __volumes__, fetched picture will be stored in the proper location. For instance, _chapter 1 page 1_ will be stored in ```/name of the comic/Chapter 1/1.jpg```.

New websites can be easily supported. I'm now working on it.
## By The Way
- Reading-driven development. Update frequency may be unstable depends on how far I read.

- Note that the ck101 website is blocked in Mainland China. You may need a global VPN or Proxychains to fetch comics from it.

## License

Copyright 2016 XIAZY

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
