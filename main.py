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
        self.dateString = None
        self.currentTempString = None
        self.currentWeatherImage = None
        self.currentTempString = None
        self.weatherLastUpdateString = None
        self.content = None
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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

    # Get the icon image for the current weather
    def getCurrentIcon(self):
        try:
            icon = PhotoImage(file="./images/" + self.content["query"]["results"]["channel"]["item"]["condition"]["code"] + ".png")
            return icon
        except Exception:
            icon = PhotoImage(file="./images/3200.png")
        return icon

    # Initial run start up.
    def run(self):

        # Display Current Time
        self.currentTimeString = StringVar()
        currentTime = Label(self.top, textvariable=self.currentTimeString, font=("Pixeled", 25, "bold"), fg="white", bg="black")
        currentTime.grid(row=0,column=0, columnspan=2)
        self.currentTimeString.set(datetime.datetime.now().strftime("%H:%M:%S %p"))

        # Display Date
        self.dateString = StringVar()
        dateInfo = Label(self.top, textvariable=self.dateString, fg="white", bg="black", font=(None , 20, "bold"))
        dateInfo.grid(row=1,column=0, columnspan=2)


        # Display Today Temperature
        self.currentTempString = StringVar()
        currentTemp = Label(self.top, textvariable=self.currentTempString, fg="white", bg="black", font=(None, 20, "bold"), justify="left")
        currentTemp.grid(row=2, column=0)

        # Display current weather images
        icon = self.getCurrentIcon()
        self.currentWeatherImage = Label(self.top, image=icon, bg="black")
        self.currentWeatherImage.image = icon
        self.currentWeatherImage.grid(row=2, column=1, padx=30)

        # Display Weather Last Update
        self.weatherLastUpdateString = StringVar()
        weatherLastUpdate = Label(textvariable=self.weatherLastUpdateString, fg="white", bg="black", font=(None, 10, "bold"))
        weatherLastUpdate.grid(row=3,column=0, columnspan=2)

        # refresh data
        self.refreshWeather()
        self.refreshTime()

        self.top.mainloop()

    # Refresh weather data
    def refreshWeather(self):
        self.updateWeather()

        # Update current icon
        icon = self.getCurrentIcon()
        self.currentWeatherImage.configure(image=icon)
        self.currentWeatherImage.image = icon

        # Update current temperature text
        temp = float(float(self.content["query"]["results"]["channel"]["item"]["condition"]["temp"]) - 32) / 1.8
        highTemp = float(float(self.content["query"]["results"]["channel"]["item"]["forecast"][0]["high"]) - 32) / 1.8
        lowTemp = float(float(self.content["query"]["results"]["channel"]["item"]["forecast"][0]["low"]) - 32) / 1.8
        self.currentTempString.set("Current: " + str(int(temp)) + "°\nHigh: " + str(int(highTemp)) + "°\nLow: " + str(int(lowTemp)) + "°")

        # Update weather last update
        self.weatherLastUpdateString.set("Last update: " +  str(datetime.datetime.now().strftime("%I:%M:%S %p")))

        # Refresh Weather
        self.weatherThread = threading.Timer(self.weatherRefresh, self.refreshWeather)
        self.weatherThread.start()

    # Refresh Time info
    def refreshTime(self):
        # Update  Time
        self.currentTimeString.set(datetime.datetime.now().strftime("%I:%M:%S %p"))

        # Update date
        day = datetime.datetime.today().weekday()
        self.dateString.set(self.days[day] + ", " + datetime.datetime.now().strftime("%d/%m/%Y"))

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