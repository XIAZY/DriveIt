__If you just want to run this app, download complied executable files for Mac and Windows [here](https://github.com/XIAZY/DriveIt/releases)!__

Icon designed by [Maxim Basinski](http://www.flaticon.com/authors/maxim-basinski), licensed by CC 3.0 BY.
# DriveIt
DriveIt is a new crawler supports multiple websites, for now it supports 

- [ck101](http://comic.ck101.com) (卡提諾×揪漫畫)

- [DM5](http://www.dm5.com) (动漫屋)

- [DMZJ](http://www.dmzj.com) (动漫之家)

- [E-hentai gallery](http://g.e-hentai.org/)

## Overview
This project is still under development. More features will be added later.
## Usage
Simply run it with ```Python 3```. You may need to install some dependencies from PyPi. Make sure to install a JavaScript runtime before you start (like ``Node.js`` or Microsoft's ``JScript`` comes  with Windows).

```
sudo pip3 install PyExecJS beautifulsoup4 requests
```
Then you should be able to run it happily. To simply start, type 
```
python3 driveit.py <FlyleafURL>
```
Advanced usage:

```
usage: driveit.py [-h] [-l LATEST] [-t THREAD] url

A multithreading comic crawler.

positional arguments:
  url                   URL of the comic's cover page

optional arguments:
  -h, --help            show this help message and exit
  -l LATEST, --latest LATEST
                        Download latest x chapters from origin
  -t THREAD, --thread THREAD
                        Number of threads. Default to be 1
```

For example:
![eg](https://i.imgur.com/VXW0oGB.png)

Or if you prefer GUI to CLI:
```
python3 driveit-gui.py
```
Note you need to have PyQt5 installed to use the GUI version. For Mac users, you can install it via
```
brew install pyqt5
```
For example:
![eg_gui](https://i.imgur.com/MbBQ26L.png)

It can automatically creates subfolders followed by __chapters__, fetched picture will be stored in the proper location. For instance, _chapter 1 page 1_ will be stored in ```/name of the comic/Chapter 1/1.jpg```.

__Complied versions for Mac and Windows are available under [Releases](https://github.com/XIAZY/DriveIt/releases).__

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

- Sometimes you will receive `connection reset` if you try to fetch comics from eHentai if you are in Mainland China. Use a global VPN or Proxychains instead.

- Personally, I'll recommend you to fetch comics from DMZJ. For me this website is the fastest one.
## License

Copyright 2016 XIAZY

Licensed under the WTFPL License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.wtfpl.net/
