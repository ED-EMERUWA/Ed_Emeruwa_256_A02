
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length
import json
from wtforms.validators import InputRequired, NumberRange
from wtforms import DateField

with open('./data/init.json', 'r') as whole_file:
        file_content = json.load(whole_file)
        PIZZA_TYPES =file_content["type"]
        CRUST_TYPES =file_content["crust"]
        SIZE_OPTIONS = file_content["size"]

class PizzaOrderForm(FlaskForm):
    type = SelectField("Pizza Type", choices=[(t, t) for t in PIZZA_TYPES], validators=[InputRequired()])
    crust = SelectField("Crust Type", choices=[(c, c) for c in CRUST_TYPES], validators=[InputRequired()])
    size = SelectField("Size", choices=[(s, s) for s in SIZE_OPTIONS], validators=[InputRequired()])
    quantity = IntegerField("Quantity", validators=[InputRequired(), NumberRange(min=1, message="Must be at least 1")])
    order_date = DateField("Delivery Date", format='%Y-%m-%d', validators=[InputRequired()])
    submit = SubmitField("Place Order")