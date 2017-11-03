# WeatherPi
[![ghit.me](https://ghit.me/badge.svg?repo=N3evin/WeatherPi)](https://ghit.me/repo/N3evin/WeatherPi)
A weather application make for Raspberry Pi with python and tkinter, using Yahoo weather API.

![Imgur](https://i.imgur.com/q91OW11.jpg)

Weather's icons: [plain weather icons by MerlinTheRed](https://www.deviantart.com/art/plain-weather-icons-157162192)

### Requirements:
* Raspberry Pi
* Python 3.++

### Step 1: Clone repository
```
sudo rm -rf WeatherPi
git clone https://github.com/N3evin/WeatherPi.git
chmod -R 755 WeatherPi
cd WeatherPi/
```

### Step 2: Edit Location
```
sudo nano ./main.py
edit desired location
CTR + c
CTR + x
Y
```

### Step 3: Start the program
```
python3 ./main.py
```