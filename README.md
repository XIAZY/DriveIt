# DriveIt
DriveIt is a new crawler supports multiple websites, for now it supports 

- [ck101](http://comic.ck101.com) (卡提諾×揪漫畫)

- [DM5](http://www.dm5.com) (动漫屋)

- [DMZJ](http://www.dmzj.com) (动漫之家)

- [E-hentai gallery](http://g.e-hentai.org/)

## Overview
This project is still under development. More features will be added later.
## Usage
__If you just want to use it _clean_ and don't want to install all these dependencies, go to [Releases](https://github.com/XIAZY/DriveIt/releases) for executable releases.__ However, I sincerely hope you can check out the source code and send me a pull request.

Simply run it with ```Python 3```. You may need to install some dependencies from PyPi. Make sure to install a JavaScript runtime before you start (like ``Node.js``).

```
sudo pip3 install PyExecJS beautifulsoup4
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
![eg_gui](http://i.imgur.com/1n8p0L2.png)

It can automatically creates subfolders followed by __chapters__ or __volumes__, fetched picture will be stored in the proper location. For instance, _chapter 1 page 1_ will be stored in ```/name of the comic/Chapter 1/1.jpg```.

New websites can be easily supported. I'm now working on it.
## By The Way

- A flyleaf page means the index page of the comic. For instances:

    - http://comic.ck101.com/comic/7194 is a flyleaf page of ck101
    - http://www.dm5.com/manhua-reclksdysjsh/ is a flyleaf page of DM5
    - http://www.dmzj.com/info/shenshimenlianaizhanzheng.html is a flyleaf page of DMZJ
    - http://g.e-hentai.org/g/932005/0949fb3a8c/ is a flyleaf page of E-hentai gallery

- Reading-driven development. Update frequency may be unstable depends on how far I read.

- Note that the ck101 website is blocked in Mainland China. You may need a global VPN or Proxychains to fetch comics from it.

- If you want to fetch comics from DMZJ, make sure the flyleaf address begins with www.dmzj.com instead of manhua.dmzj.com. The logic to fetch comics from these two domains are different.

- Personally, I'll recommend you to fetch comics from DMZJ. For me this website is the fastest one.
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
