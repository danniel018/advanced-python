# Oberver pattern

The Observer pattern is a behavioral pattern where an object (called the subject) maintains a list of dependents (called observers) and automatically notifies them of any state changes. It's essentially a publish-subscribe model.

The pattern establishes a one-to-many dependency. A change in one object (the "Subject") automatically notifies multiple other objects (the "Observers"). This is managed through a subscription mechanism, where observers must explicitly register to receive notifications. The pattern is classified as a behavioral and object pattern. 

## Usage

```python
from abc import ABC, abstractmethod

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, temperature, humidity):
        pass

# Subject (Observable)
class WeatherStation:
    def __init__(self):
        self._observers = []
        self._temperature = 0
        self._humidity = 0
    
    def attach(self, observer):
        """Subscribe an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """Unsubscribe an observer"""
        self._observers.remove(observer)
    
    def notify(self):
        """Notify all observers of state change"""
        for observer in self._observers:
            observer.update(self._temperature, self._humidity)
    
    def set_measurements(self, temperature, humidity):
        """When measurements change, notify observers"""
        self._temperature = temperature
        self._humidity = humidity
        self.notify()

# Concrete Observers
class PhoneDisplay(Observer):
    def update(self, temperature, humidity):
        print(f"Phone Display: {temperature}°C, {humidity}% humidity")

class TVDisplay(Observer):
    def update(self, temperature, humidity):
        print(f"TV Display: Temperature is {temperature}°C")

class WebDashboard(Observer):
    def update(self, temperature, humidity):
        print(f"Web Dashboard: Temp={temperature}°C, Humidity={humidity}%")

# Usage
if __name__ == "__main__":
    # Create subject
    weather_station = WeatherStation()
    
    # Create observers
    phone = PhoneDisplay()
    tv = TVDisplay()
    web = WebDashboard()
    
    # Subscribe observers
    weather_station.attach(phone)
    weather_station.attach(tv)
    weather_station.attach(web)
    
    # Change state - all observers get notified automatically
    print("Weather update 1:")
    weather_station.set_measurements(25, 65)
    
    print("\nWeather update 2:")
    weather_station.set_measurements(28, 70)
    
    # Unsubscribe one observer
    weather_station.detach(tv)
    
    print("\nWeather update 3 (TV unsubscribed):")
    weather_station.set_measurements(22, 60)
```

**Output:**
```
Weather update 1:
Phone Display: 25°C, 65% humidity
TV Display: Temperature is 25°C
Web Dashboard: Temp=25°C, Humidity=65%

Weather update 2:
Phone Display: 28°C, 70% humidity
TV Display: Temperature is 28°C
Web Dashboard: Temp=28°C, Humidity=70%

Weather update 3 (TV unsubscribed):
Phone Display: 22°C, 60% humidity
Web Dashboard: Temp=22°C, Humidity=60%
```