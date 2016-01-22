# DriveIt
Driveit is a new crawler supports multiple websites, for now it supports http://comic.ck101.com and http://www.dm5.com
## Overview
This project is still under development. However, you can still run it with ```Python 3``` and it will work fine. More features will be added later.
## Usage
Simply run it with ```Python 3```. You may need to install some dependencies from PyPi.
```
sudo pip3 install nodejs
```
Then you should be able to run it happily. To start, type 
```
python3 driveit.py
```
and input the site address of the flyleaf when asked.

For example:
![eg](http://i.imgur.com/Yex2M61.png)

It can automatically creates subfolders followed by __chapters__ and __volumes__, fetched picture will be stored in the proper location. For example, _chapter 1 page 1_ will be stored in ```/name of the comic/1/1.jpg```, while _volume 5 page 6_ will be stored in ```/name of the comic/V5/6.jpg```.

New websites can be easily supported. I'm now working on it.
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
