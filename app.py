from curses import flash
from api import format_data, get_city_data, get_crime_data, unpack_zipcode
from forms import CityForm

# Unpack the variables directly when calling the function
# overall_crime, crime_specs, violent_crime_rates, property_crime_rates, other_crime_rates, total_violent, total_other, total_property = format_data()

from flask import Flask, redirect, render_template, request


app = Flask(__name__)
app.config['SECRET_KEY'] = "iluvu123"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True


@app.route('/', methods=["GET", "POST"])
def home():

    form = CityForm()

    if form.validate_on_submit():
        city = form.city.data
        state = form.state.data
        zipcode = unpack_zipcode(city, state)
        return redirect(f'/crime-data/{zipcode}')
    return render_template("home.html", form=form)


@app.route('/crime-data/<int:zipcode>')
def show_crime_data(zipcode):
    form = CityForm()
    get_crime_data(zipcode)
    # Call the format_data() function and unpack the returned values
    overall_crime, crime_specs, violent_crime_rates, property_crime_rates, other_crime_rates, total_violent, total_other, total_property = format_data(
        zipcode)

    # Format the crime data for display
    # Unpack the overall crime data
    zipcode = overall_crime['Zipcode']
    overall_grade = overall_crime['Overall Crime Grade']
    violent_grade = overall_crime['Violent Crime Grade']
    property_grade = overall_crime['Property Crime Grade']
    other_grade = overall_crime['Other Crime Grade']
    fact = overall_crime['Fact']
    risk = overall_crime['Risk']
    risk_detail = overall_crime['Risk Detail']

    # Unpack the violent crime rates data
    assault_rate = violent_crime_rates['Violent Crime Rates']['Assault']
    robbery_rate = violent_crime_rates['Violent Crime Rates']['Robbery']
    rape_rate = violent_crime_rates['Violent Crime Rates']['Rape']
    murder_rate = violent_crime_rates['Violent Crime Rates']['Murder']
    total_violent_crime = violent_crime_rates['0']['Total Violent Crime']
    total_violent_crime_score = violent_crime_rates['0']['Total Violent Crime Score']

    # Unpack the property crime rates data
    theft_rate = property_crime_rates['Property Crime Rates']['Theft']
    vehicle_theft_rate = property_crime_rates['Property Crime Rates']['Vehicle Theft']
    burglary_rate = property_crime_rates['Property Crime Rates']['Burglary']
    arson_rate = property_crime_rates['Property Crime Rates']['Arson']
    total_property_crime = property_crime_rates['0']['Total Property Crime']
    total_property_crime_score = property_crime_rates['0']['Total Property Crime Score']

    # Unpack the other crime rates data
    kidnapping_rate = other_crime_rates['Other Crime Rates']['Kidnapping']
    drug_crime_rate = other_crime_rates['Other Crime Rates']['Drug Crimes']
    vandalism_rate = other_crime_rates['Other Crime Rates']['Vandalism']
    identity_theft_rate = other_crime_rates['Other Crime Rates']['Identity Theft']
    animal_cruelty_rate = other_crime_rates['Other Crime Rates']['Animal Cruelty']
    total_other_rate = other_crime_rates['0']['Total Other Rate']
    total_other_score = other_crime_rates['0']['Total Other Score']

    # Pass the formatted crime data to the template
    return render_template('data.html',
                           form=form,
                           zipcode=zipcode,
                           overall_grade=overall_grade,
                           violent_grade=violent_grade,
                           property_grade=property_grade,
                           other_grade=other_grade,
                           fact=fact,
                           risk=risk,
                           risk_detail=risk_detail,
                           assault_rate=assault_rate,
                           robbery_rate=robbery_rate,
                           rape_rate=rape_rate,
                           murder_rate=murder_rate,
                           total_violent_crime=total_violent_crime,
                           total_violent_crime_score=total_violent_crime_score,
                           theft_rate=theft_rate,
                           vehicle_theft_rate=vehicle_theft_rate,
                           burglary_rate=burglary_rate,
                           arson_rate=arson_rate,
                           total_property_crime=total_property_crime,
                           total_property_crime_score=total_property_crime_score,
                           kidnapping_rate=kidnapping_rate,
                           drug_crime_rate=drug_crime_rate,
                           vandalism_rate=vandalism_rate,
                           identity_theft_rate=identity_theft_rate,
                           animal_cruelty_rate=animal_cruelty_rate,
                           total_other_rate=total_other_rate,
                           total_other_score=total_other_score)
