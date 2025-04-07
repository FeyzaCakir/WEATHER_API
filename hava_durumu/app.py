from flask import Flask, redirect, url_for, render_template, request, session
import requests
import firebase_admin
from firebase_admin import credentials, auth
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from firebase_admin import auth
import pyrebase
import os
from firebase_admin import credentials, auth
from dotenv import load_dotenv

app = Flask(__name__)

#.env yükle
load_dotenv()

cred=credentials.Certificate(r"C:\Users\feyza\Documents\weather.json")
firebase_admin.initialize_app(cred)

app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE")
print(app.secret_key)

class RegisterForm(FlaskForm):
    email= StringField("E-mail", validators=[DataRequired(),Email()])
    password= PasswordField("Şifre", validators=[DataRequired()])
    submit= SubmitField("Kaydol")

class LoginForm(FlaskForm):
    email= StringField("E-mail", validators=[DataRequired(),Email()])
    password= PasswordField("Şifre", validators=[DataRequired()])
    submit= SubmitField("Giriş")   

config = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "projectId": os.getenv("PROJECT_ID"),
    "storageBucket": os.getenv("STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID"),
    "measurementId": os.getenv("MEASUREMENT_ID"),
    "databaseURL": os.getenv("DATABASE_URL")
}

firebase= pyrebase.initialize_app(config)
auth_pyrebase= firebase.auth()

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    error = None
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = auth.create_user(email=email, password=password)
            return redirect(url_for("login"))
        except Exception as e:
            error = f"Böyle bir hesap mevcut!"
    
    return render_template("register.html", form=form, error=error)

import firebase_admin
from firebase_admin import auth

@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            # Firebase Admin ile kullanıcıyı doğrula
            user = auth.get_user_by_email(email)  # Kullanıcıyı email ile bul
            try:
                # Kullanıcıyı pyrebase ile giriş yapmaya çalış (şifre doğrulaması için)
                user = auth_pyrebase.sign_in_with_email_and_password(email, password)

                # Firebase ID Token al (Kimlik doğrulama için önemli!)
                user_info = auth_pyrebase.get_account_info(user['idToken'])

                if user_info:
                    session["user"] = user["email"]  # idToken yerine email saklanıyor!
                    return redirect(url_for("home"))
                else:
                    error = "Hatalı giriş!"
            except Exception as e:
                print("Firebase giriş hatası:", e)
                error = "Kullanıcı adı veya şifre hatalı!"
                
        except auth.UserNotFoundError:
            error = "Böyle bir hesap yok!"  # Kayıtlı olmayan kullanıcı

    return render_template("login.html", form=form, error=error)


# Çıkış Yapma
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



#API WEATHER
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

#API COUNTRY
COUNTRY_API_KEY= os.getenv("COUNTRY_API_KEY")


headers = {
  'X-CSCAPI-KEY': COUNTRY_API_KEY
}



def get_countries():
    url_country = "https://api.countrystatecity.in/v1/countries"
    response = requests.get(url_country, headers=headers)
    
    if response.status_code == 200:
        countries = response.json()
        return countries  # Burada listeyi gerçekten döndürmeliyiz
    
    print("API Yanıt Hatası:", response.text)  # Hata varsa ekrana yazdır
    return []  # API başarısız olduğunda boş liste dönmeli


def get_states(country_code):
    url_states = f"https://api.countrystatecity.in/v1/countries/{country_code}/states"
    response = requests.get(url_states, headers=headers)

    if response.status_code == 200:
        return response.json()  # Eyalet listesini döndür
    return []

def get_cities(country_code, state_code):
    url_cities = f"https://api.countrystatecity.in/v1/countries/{country_code}/states/{state_code}/cities"
    response = requests.get(url_cities, headers=headers)

    if response.status_code == 200:
        return response.json()  # Şehir listesini döndür
    return []

    
def get_weather(city_name):
    url_weather = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=tr"
    response = requests.get(url_weather)


    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ API Hatası! Kod: {response.status_code}, Mesaj: {response.text}")

    return None


@app.route("/home", methods=["GET", "POST"])
def home():
    countries = get_countries()
    states = []
    cities = []
    weather = None

    selected_country = request.form.get("country")
    selected_state = request.form.get("state")
    selected_city = request.form.get("city")

    if selected_country:
        states = get_states(selected_country)

    if selected_country and selected_state:
        cities = get_cities(selected_country, selected_state)

    if selected_city:
        weather = get_weather(selected_city)

    return render_template("home.html", countries=countries, states=states, cities=cities, weather=weather, selected_country=selected_country, selected_state=selected_state)


if __name__ == "__main__":
    app.run(debug=True, port=5000)