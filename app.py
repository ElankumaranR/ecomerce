from flask import Flask, render_template, redirect, request, flash,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:7339650722@localhost/shop'
app.config['SECRET_KEY'] = '11111111111'
app.config['UPLOAD_FOLDER'] = 'D:\\python project\\ecomerce\\static\\images'

admin = 'elan@gmail.com'
database_password = 'elan@2005'

db = SQLAlchemy(app)

class AdminUser(UserMixin):
    id = -1 
    email = admin
    is_admin = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    if user_id == "-1":
        return AdminUser() 
    return Customer.query.get(int(user_id)) 



class SignUpForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=3)])
    email = StringField(validators=[DataRequired(), Length(min=4)])
    password1 = PasswordField(validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign up')


class LogInForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Log in')



class ShopItemsForm(FlaskForm):
    
    name = StringField('Name of item', validators=[DataRequired()])
    current_price = IntegerField(validators=[DataRequired()])
    previous_price = IntegerField(validators=[DataRequired()])
    remaining = IntegerField(validators=[NumberRange(min=1)])
    quantity = IntegerField(validators=[DataRequired(), NumberRange(min=1)])
    update_cart = SubmitField('Update')
    add_item = SubmitField('Add item')


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(100))
    cart_items = db.relationship('CartItem', backref='cartItems', uselist=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Customer %r>' % self.id


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    current_price = db.Column(db.Integer, nullable=False)
    previous_price = db.Column(db.Integer, nullable=False)
    remaining = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(255))
    def __repr__(self):
        return '<Item %r>' % self.id

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    item_name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<CartItem %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def login():
    email = None
    password = None
    form = LogInForm()
    if form.validate_on_submit():
        if admin==form.email.data and database_password==form.password.data:
            admin_user = AdminUser()
            login_user(admin_user)
            return redirect('/shopitems/')
        else:
            customer = Customer.query.filter_by(email=form.email.data).first()
            if customer:
                if check_password_hash(customer.password_hash, form.password.data):
                    login_user(customer)
                    return redirect('/amazon/')
                else:
                    flash('Wrong password!! Try again...', category='error')
            else:
                flash('Account does not exit...Create one from the sign up page...', category='error')

            form.email.data = ''
            form.password.data = ''
    return render_template('login.html', email=email, password=password, form=form)


@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    email = None
    username = None
    password1 = None
    password2 = None
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data
        if password1 == password2:
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = password2
            try:
                db.session.add(new_customer)
                db.session.commit()
 
                flash('Account created successfully', category='success')
                return redirect('/')
            except Exception as e:
                print(e)
                flash('There was an error adding the new account', category='error')
        form.email.data = ''
        form.username.data = ''
        form.password1.data = ''
        form.password2.data = ''
    return render_template('signup.html', email=email, username=username, password1=password1, password2=password2, form=form)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def log_out():
    logout_user()
    flash('Thank you for shopping with us...', category='success')
    return redirect('/')


@app.route('/customers', methods=['POST', 'GET'])
@login_required
def customer_display():
    customers = Customer.query.order_by(Customer.date_joined).all()
    return render_template('customers.html', customers=customers)

@app.route('/removecustomer/<int:id>')
def remove_customer(id):
    customer_to_remove = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer_to_remove)
        db.session.commit()
        return redirect('/customers')
    except:
        return 'There was an error removing that customer'


@app.route('/amazon/', methods=['GET', 'POST'])
@login_required
def amazon():
    items = Item.query.order_by(Item.date_added).all()
    items_list = [item for item in items]
    return render_template('shop.html', items_list=items_list)

@app.route('/shopitems/', methods=['GET', 'POST'])
@login_required
def shop_items():
    if request.method == 'POST':
        name = request.form.get('name')
        current_price = request.form.get('current_price')
        previous_price = request.form.get('previous_price')
        remaining = request.form.get('remaining')
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                image_url = "../static/images/"+filename

            else:
                image_url = None
        else:
            image_url = None

        new_item = Item(name=name, current_price=current_price, previous_price=previous_price, remaining=remaining, image_url=image_url)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/shopitems/')
        except:
            flash('There was an error adding a new shop item', category='error')
    items = Item.query.order_by(Item.date_added).all()
    return render_template('shopitems.html', items=items)

@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Item.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/shopitems/')
    except:
        return 'There was an error deleting that item'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.current_price = request.form.get('current_price')
        item.previous_price = request.form.get('previous_price')
        item.remaining = request.form.get('remaining')
        item.image=request.files['image'].read()
        try:
            db.session.commit()
            return redirect('/shopitems/')
        except:
            return 'There was an error updating that item'
    else:
        return render_template('update.html', item=item)

@app.route('/addtocart/<int:id>', methods=['POST', 'GET'])
def add_to_cart(id):
    item = Item.query.get_or_404(id)
    new_cart_item = CartItem()
    new_cart_item.item_name = item.name
    new_cart_item.price = item.current_price
    new_cart_item.quantity = 1
    new_cart_item.customer_link = current_user.id
    try:
        db.session.add(new_cart_item)
        db.session.commit()
        return redirect('/amazon/')
    except:
        return 'Item not added'


@app.route('/updatecart/<int:id>', methods=['POST', 'GET'])
@app.route('/updatecart/<int:id>', methods=['POST', 'GET'])
def update_item(id):
    item = CartItem.query.get_or_404(id)
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        if quantity:
            try:
                item.quantity = int(quantity)
                db.session.commit()
                flash('Quantity updated successfully!', category='success')
                return redirect(url_for('cart'))  
            except Exception as e:
                db.session.rollback()
                flash('There was an error updating your cart', category='error')
    return render_template('updatecart.html', item=item)



@app.route('/remove/<int:id>', methods=['POST', 'GET'])
def remove_item(id):
    item_to_remove = CartItem.query.get_or_404(id)
    try:
        db.session.delete(item_to_remove)
        db.session.commit()
        return redirect('/cart/')
    except:
        return 'Item not deleted'

@app.route('/cart/', methods=['POST', 'GET'])
def cart():
    items = CartItem.query.filter_by(customer_link=current_user.id).all()
    total, quantity_total = 0, 0
    for item in items:
        quantity_total = quantity_total + item.quantity
        value = item.price * item.quantity
        total = total+value
    return render_template('cart.html', items=items, total=total, quantity_total=quantity_total)


@app.route('/payment', methods=['POST', 'GET'])
def payment():
    if request.method == 'POST':
        CartItem.query.delete()
        db.session.commit()
        return "Thank you for shopping with us <a href='/amazon/'>Back To Home</a>"
    return render_template('payment.html')


@app.route('/search', methods=['GET'])
def search_items():

    search_query = request.args.get('item')

    if not search_query:
        items = Item.query.order_by(Item.date_added).all()
    else:
        items = Item.query.filter(Item.name.ilike(f'%{search_query}%')).order_by(Item.date_added).all()

    return render_template('search.html', items_list=items, search_query=search_query)
if __name__ == '__main__':
    app.run(debug=True)
