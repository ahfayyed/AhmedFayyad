
import tkinter as tk
import requests

# API للاتصال  OpenWeatherMap
API_KEY = '4e3d474f98cd64dd9b783ab8b77fbf78'  #  API استبدل بمفتاح 
url = 'http://api.openweathermap.org/data/2.5/weather'  # API رابط  

# دالة للحصول على بيانات الطقس
def get_weather():
    city = location_entry.get()  # الحصول على اسم المدينة من المستخدم
    response = requests.get(url, params={'q': city, 'appid': API_KEY, 'units': 'metric'})
    data = response.json()  # تحويل الاستجابة إلى تنسيق JSON

    if response.status_code == 200:
        # استخراج المعلومات المطلوبة من البيانات
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        precipitation = data.get('rain', {}).get('1h', 0)  # هطول المطر

        # تحديث النصوص في الواجهة
        temperature_label.config(text=f"Temperature: {temperature} °C")
        humidity_label.config(text=f"Humidity: {humidity} %")
        wind_speed_label.config(text=f"Wind Speed: {wind_speed} km/h")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        precipitation_label.config(text=f"Precipitation: {precipitation} mm")
    else:
        # في حال عدم العثور على المدينة  
        temperature_label.config(text="Temperature: --")
        humidity_label.config(text="Humidity: --")
        wind_speed_label.config(text="Wind Speed: --")
        pressure_label.config(text="Pressure: --")
        precipitation_label.config(text="Precipitation: --")

# إنشاء نافذة التطبيق الرئيسية
window = tk.Tk()
window.title("WeatherForecast")
window.geometry("600x500")

# إنشاء حقل الإدخال الخاص بالموقع
location_label = tk.Label(window, text="Location :", font=("Helvetica", 15))
location_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

location_entry = tk.Entry(window, font=("Helvetica", 15))
location_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

# إنشاء زر البحث
search_button = tk.Button(window, text="Search", relief="raised", font=("Helvetica", 11), command=get_weather)
search_button.grid(row=0, column=2, sticky="w", padx=10, pady=10)

# إنشاء إطار لعرض تفاصيل الطقس
weather_frame = tk.Frame(window)
weather_frame.grid(row=1, column=0, columnspan=3, pady=20, sticky="ew")  # اجعل الإطار يتجه لليسار

# عرض تفاصيل الطقس
temperature_label = tk.Label(weather_frame, text="Temperature : ", font=("Helvetica", 18))
temperature_label.grid(row=0, column=0, sticky="w", pady=12 , padx=15)

humidity_label = tk.Label(weather_frame, text="Humidity : ", font=("Helvetica", 18))
humidity_label.grid(row=1, column=0, sticky="w", pady=12 , padx=15)

wind_speed_label = tk.Label(weather_frame, text="Wind Speed : ", font=("Helvetica", 18))
wind_speed_label.grid(row=2, column=0, sticky="w", pady=12 , padx=15 )

pressure_label = tk.Label(weather_frame, text="Pressure : ", font=("Helvetica", 18))
pressure_label.grid(row=3, column=0, sticky="w", pady=12 , padx=15)

precipitation_label = tk.Label(weather_frame, text="Precipitation : ", font=("Helvetica", 18))
precipitation_label.grid(row=4, column=0, sticky="w", pady=12 , padx=15)

# ضبط حجم الأعمدة
window.columnconfigure(1, weight=1)  # السماح للعمود الثاني (حقل الإدخال) بالتوسع

# تشغيل التطبيق
window.mainloop()
