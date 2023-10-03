from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import os
from dotenv import load_dotenv
import csv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRETKEY")


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    url = URLField('Location (Google Maps URL)', validators=[DataRequired(), URL()])
    open = StringField('Opening Time', validators=[DataRequired()])
    close = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[('☕', '☕'), ('☕☕', '☕☕'), ('☕☕☕', '☕☕☕'),
                                                          ('☕☕☕☕', '☕☕☕☕'), ('☕☕☕☕☕', '☕☕☕☕☕')])
    wifi_rating = SelectField('Wifi Rating', choices=[('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'),
                                                          ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')])
    power_rating = SelectField('Power Rating', choices=[('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'),
                                                      ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        data_points = form.data
        data_list = [data_points[key] for key in data_points]
        print(data_list)
        with open("cafe-data.csv", encoding="utf-8", mode="a", newline="") as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerow(data_list[:7])
        form.cafe.data = ""
        form.url.data = ""
        form.close.data = ""
        form.open.data = ""
        form.coffee_rating.data = ""
        form.wifi_rating.data = ""
        form.power_rating.data = ""
        return render_template('add.html', form=form)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding='utf-8', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
