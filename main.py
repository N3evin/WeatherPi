"""
Created by N3evin
An application that display time and weather information for Raspberry Pi
"""

from tkinter import *
import urllib3, json, threading, datetime, certifi

class main():

    # Config
    location = "Melbourne, Clayton" # {Country} or {Country, City} without parenthesis.
    url = "https://query.yahooapis.com/v1/public/yql?q="
    weatherRefresh = 300 # in seconds, default 5 minutes


    def __init__(self):
        # Variables
        self.cityString = None
        self.currentTempString = None
        self.weatherImage = None
        self.currentTempString = None
        self.weatherLastUpdateString = None
        self.content = None

        # Thread variables
        self.weatherThread = threading.Timer(0, None)
        self.timeThread = threading.Timer(0, None)


        # Initialized the frame.
        self.top = Tk()
        self.top.attributes('-fullscreen',True) # Set to fullscreen
        self.top.config(cursor="none", bg="black")
        self.top.title("WeatherPi v0.1") # Title of app
        self.top.protocol('WM_DELETE_WINDOW', self.stop) # When close, stop all thread
        self.top.geometry("480x320")

        # Configure the weight, so that widget will be centered.
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

        # Update weather and run
        self.updateWeather()
        self.run()


    # Retrieve weather from url and update weather.
    def updateWeather(self):
        # Reading weather info
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        query = """select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"""" + self.location + """\")&format=json"""
        query = query.replace(" ","%20")
        output = http.request('GET', self.url+query)
        self.content = json.loads(output.data.decode('utf-8'))

    # Get the icon image for the weather
    def getIcon(self):
        icon = PhotoImage(file="./images/" + self.content["query"]["results"]["channel"]["item"]["condition"]["code"] + ".png")
        return icon

    # Initial run start up.
    def run(self):

        # Display Current Time
        self.currentTimeString = StringVar()
        currentTime = Label(self.top, textvariable=self.currentTimeString, font=("Pixeled", 25, "bold"), fg="white", bg="black")
        currentTime.grid(row=0,column=0)
        self.currentTimeString.set(datetime.datetime.now().strftime("%H:%M:%S %p"))

        # Display Location Name
        self.cityString = StringVar()
        cityName = Label(self.top, textvariable=self.cityString, fg="white", bg="black", font=(None , 15, "bold"))
        cityName.grid(row=1,column=0)
        self.cityString.set(self.location)

        # Display Current Temperature
        self.currentTempString = StringVar()
        currentTemp = Label(self.top, textvariable=self.currentTempString, fg="white", bg="black", font=(None , 15, "bold"))
        currentTemp.grid(row=2,column=0)

        # Display weather images
        icon = self.getIcon()
        self.weatherImage = Label(self.top, image=icon, bg="black")
        self.weatherImage.image = icon
        self.weatherImage.grid(row=3,column=0)

        # Display Weather Last Update
        self.weatherLastUpdateString = StringVar()
        weatherLastUpdate = Label(textvariable=self.weatherLastUpdateString, fg="white", bg="black", font=(None, 10, "bold"), anchor="se")
        weatherLastUpdate.grid(row=4,column=0)

        # refresh data
        self.refreshWeather()
        self.refreshTime()

        self.top.mainloop()

    # Refresh weather data
    def refreshWeather(self):
        self.updateWeather()

        # Update icon
        icon = self.getIcon()
        self.weatherImage.configure(image=icon)
        self.weatherImage.image = icon

        # Update temperature text
        temp = float(float(self.content["query"]["results"]["channel"]["item"]["condition"]["temp"])-32)/1.8
        self.currentTempString.set("Current Temperature: " + str(float("{0:.2f}".format(temp))) + " °C")

        # Update weather last update
        self.weatherLastUpdateString.set("Last update: " +  str(datetime.datetime.now().strftime("%H:%M:%S %p")))

        # Refresh Weather
        self.weatherThread = threading.Timer(self.weatherRefresh, self.refreshWeather)
        self.weatherThread.start()

    # Refresh Time info
    def refreshTime(self):
        # Set Time
        self.currentTimeString.set(datetime.datetime.now().strftime("%I:%M:%S %p"))

        # Refresh Time
        self.timeThread = threading.Timer(1, self.refreshTime)
        self.timeThread.start()

    # Kill all threads
    def stop(self):
        self.weatherThread.cancel()
        self.timeThread.cancel()
        self.top.destroy()

if __name__ == "__main__":
    main()