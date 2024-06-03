import os
import datetime
from flask import Flask, request, render_template, session, redirect
import pymysql


app = Flask(__name__)
app.secret_key = "events"
conn = pymysql.connect(host="localhost", user="root", password="Luther@1234", db="event_management_system")
cursor = conn.cursor()
admin_username = "admin"
admin_password = "admin"


APP_ROOT = os.path.dirname(__file__)
APP_ROOT = APP_ROOT + "/static"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin_login1", methods=['post'])
def admin_login1():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == admin_username and password == admin_password:
        session['role'] = "admin"
        return redirect("/admin_home")
    else:
        return render_template("msg.html", message="invalid login details")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/view_host")
def view_host():
    cursor.execute("select * from event_host")
    event_hosts = cursor.fetchall()
    return render_template("view_host.html", event_hosts=event_hosts)


@app.route("/verify_host")
def verify_host():
    event_host_id = request.args.get("event_host_id")
    cursor.execute("update event_host set status = 'Verified' where event_host_id = '"+str(event_host_id)+"'")
    conn.commit()
    return redirect("/view_host")


@app.route("/add_places")
def add_places():
    return render_template("add_places.html")


@app.route("/add_places1", methods=['post'])
def add_places1():
    name = request.form.get("name")
    address = request.form.get("address")
    cursor.execute("insert into places(name,address) values('"+str(name)+"', '"+str(address)+"')")
    conn.commit()
    return {"message": " place added successfully"}


@app.route("/get_places")
def get_places():
    cursor.execute("select * from places")
    places = cursor.fetchall()
    return render_template("view_places.html", places=places)


@app.route("/add_event_types")
def add_event_types():
    return render_template("add_event_types.html")


@app.route("/add_event_types1", methods=['post'])
def add_event_types1():
    event_type = request.form.get("event_type")
    picture = request.files.get("picture")
    path = APP_ROOT + "/event_type/" + picture.filename
    picture.save(path)
    cursor.execute("insert into event_type(event_type,event_type_pic) values('"+str(event_type)+"', '"+str(picture.filename)+"')")
    conn.commit()
    return redirect("add_event_types")


@app.route("/get_event_types")
def get_event_types():
    cursor.execute("select * from event_type")
    event_types = cursor.fetchall()
    return render_template("get_event_types.html", event_types=event_types)


@app.route("/view_donations")
def view_donations():
    cursor.execute("select * from booking where donations > '0' ")
    bookings = cursor.fetchall()
    return render_template("view_donations.html", bookings=bookings, get_customer_by_customer_id=get_customer_by_customer_id)


@app.route("/taxes_and_fees")
def taxes_and_fees():
    cursor.execute("select * from booking")
    bookings = cursor.fetchall()
    return render_template("taxes_and_fees.html", bookings=bookings, get_customer_by_customer_id=get_customer_by_customer_id)


def get_customer_by_customer_id(customer_id):
    cursor.execute("select * from customer where customer_id='"+str(customer_id)+"'")
    customers = cursor.fetchall()
    return customers[0]


@app.route("/event_host_login")
def event_host_login():
    return render_template("event_host_login.html")


@app.route("/event_host_login1", methods=['post'])
def event_host_login1():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from event_host where email = '" + str(email) + "' and password = '" + str(password) + "'")
    if count > 0:
        event_host = cursor.fetchall()
        status = event_host[0][6]
        if status == 'Verified':
            session["event_host_id"] = event_host[0][0]
            session['role'] = "event_host"
            return redirect("/event_host_home")
        else:
            return render_template("msg.html", message="Your Account is not Verified")
    else:
        return render_template("msg.html", message="Invalid Login Details")


@app.route("/event_host_home")
def event_host_home():
    event_host_id = session["event_host_id"]
    cursor.execute("select * from event_host where event_host_id='"+str(event_host_id)+"' ")
    event_host = cursor.fetchall()
    return render_template("event_host_home.html", event_host=event_host[0])


@app.route("/add_events")
def add_events():
    cursor.execute("select * from places")
    places = cursor.fetchall()
    cursor.execute("select * from event_type ")
    event_types = cursor.fetchall()
    return render_template("add_events.html", places=places, event_types=event_types)


@app.route("/add_events1", methods=['post'])
def add_events1():
    event_title = request.form.get("event_title")
    event_pic = request.files.get("event_pic")
    path = APP_ROOT + "/event/" + event_pic.filename
    event_pic.save(path)
    start_date_time = request.form.get("start_date_time")
    start_date_time = start_date_time.replace("T", " ")
    event_date = datetime.datetime.strptime(start_date_time, '%Y-%m-%d %H:%M')
    event_date = event_date.strftime("%Y-%m-%d")
    end_date_time = request.form.get("end_date_time")
    description = request.form.get("description")
    cost_per_person = request.form.get("cost_per_person")
    event_host_id = session['event_host_id']
    event_type_id = request.form.get("event_type_id")
    place_id = request.form.get("place_id")
    layout = request.form.get("layout")
    number_of_tickets = request.form.get("number_of_tickets")
    cursor.execute("insert into event(event_title,event_pic,event_date,start_date_time,end_date_time,description,cost_per_person,event_host_id,event_type_id,places_id,layout,number_of_tickets) values('"+str(event_title)+"','"+str(event_pic.filename)+"','"+str(event_date)+"','"+str(start_date_time)+"','"+str(end_date_time)+"','"+str(description)+"','"+str(cost_per_person)+"','"+str(event_host_id)+"','"+str(event_type_id)+"', '"+str(place_id)+"','"+str(layout)+"', '"+str(number_of_tickets)+"')")
    conn.commit()
    return render_template("msg.html", message="Event Added Successfully")


@app.route("/view_events")
def view_events():
    cursor.execute("select * from event_type")
    event_types = cursor.fetchall()
    return render_template("view_events.html", event_types=event_types)


@app.route("/get_events")
def get_events():
    event_type_id = request.args.get("event_type_id")
    event_title = request.args.get("event_title")
    btn_selected = request.args.get("btn_selected")
    query = ''
    if btn_selected == 'history':
        if event_type_id == '':
            query = "select * from event where event_title like '%"+str(event_title)+"%' and event_date<now()"
        else:
            query = "select * from event where event_title like '%"+str(event_title)+"%' and event_date<now() and event_type_id = '"+str(event_type_id)+"' "
    elif btn_selected == 'today':
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if event_type_id == '':
            query = "select * from event where event_title like '%"+str(event_title)+"%' and event_date='"+str(today)+"'"
        else:
            query = "select * from event where event_title like '%"+str(event_title)+"%' and event_date='"+str(today)+"' and event_type_id = '"+str(event_type_id)+"' "
    elif btn_selected == 'future':
        if event_type_id == '':
            query = "select * from event where event_title like '%"+str(event_title)+"%' and event_date>now()"
        else:
            query = "select * from event where event_title like '%"+str(event_title)+"%'and event_date>now() and event_type_id = '"+str(event_type_id)+"' "
    cursor.execute(query)
    events = cursor.fetchall()
    events = list(events)
    events.reverse()
    return render_template("get_events.html", events=events, btn_selected=btn_selected, get_avg_rating_by_event_id=get_avg_rating_by_event_id, get_event_host_by_event_host_id=get_event_host_by_event_host_id)


def get_avg_rating_by_event_id(event_id):
    cursor.execute("select avg(rating) as average_rating from review_rating where booking_id in(select booking_id from booking where event_id = '" + str(event_id) + "')")
    rating = cursor.fetchall()
    return rating[0]


def get_event_host_by_event_host_id(event_host_id):
    cursor.execute("select * from event_host where event_host_id='"+str(event_host_id)+"'")
    event_host = cursor.fetchall()
    return event_host[0]


@app.route("/view_review_rating")
def view_review_rating():
    event_id = request.args.get("event_id")
    cursor.execute("select * from review_rating where booking_id in(select booking_id from booking where event_id = '" + str(event_id) + "')")
    reviews = cursor.fetchall()
    cursor.execute("select * from event where event_id = '" + str(event_id) + "'")
    events = cursor.fetchall()
    return render_template("view_review_rating.html", get_customer_by_customer_id=get_customer_by_customer_id,get_customer_id_by_booking_id=get_customer_id_by_booking_id, reviews=reviews, events=events, get_event_host_by_event_host_id=get_event_host_by_event_host_id, get_avg_rating_by_event_id=get_avg_rating_by_event_id)


def get_customer_id_by_booking_id(booking_id):
    cursor.execute("select * from booking where booking_id = '"+str(booking_id)+"'")
    booking = cursor.fetchall()
    return booking[0]


@app.route("/add_coupons")
def add_coupons():
    return render_template("add_coupons.html")


@app.route("/add_coupons1", methods=['post'])
def add_coupons1():
    coupon_name = request.form.get("coupon_name")
    description = request.form.get("description")
    validity = request.form.get("validity")
    event_host_id = session['event_host_id']
    discount = request.form.get("discount")
    status = 'Active'
    cursor.execute("insert into coupons(coupon_name,description,validity_upto,event_host_id,discount,status) values('"+str(coupon_name)+"', '"+str(description)+"', '"+str(validity)+"', '"+str(event_host_id)+"', '"+str(discount)+"', '"+str(status)+"')")
    conn.commit()
    return redirect("/add_coupons")


@app.route("/get_coupons")
def get_coupons():
    cursor.execute("select * from coupons")
    coupons = cursor.fetchall()
    return render_template("get_coupons.html", coupons=coupons)


@app.route("/active_coupon")
def active_coupon():
    coupon_id = request.args.get("coupon_id")
    cursor.execute("update coupons set status = 'Active' where coupons_id = '"+str(coupon_id)+"'")
    conn.commit()
    return redirect("/add_coupons")


@app.route("/disable_coupon")
def disable_coupon():
    coupon_id = request.args.get("coupon_id")
    cursor.execute("update coupons set status = 'Disabled' where coupons_id = '"+str(coupon_id)+"'")
    conn.commit()
    return redirect("/add_coupons")


@app.route("/event_host_registration")
def event_host_registration():
    return render_template("event_host_registration.html")


@app.route("/event_host_registration1", methods=['post'])
def event_host_registration1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address = request.form.get("address")
    picture = request.files.get("picture")
    status = "Not verified"
    path = APP_ROOT + "/event_host/" + picture.filename
    picture.save(path)
    count = cursor.execute("select * from event_host where email = '"+str(email)+"' or phone = '"+str(phone)+"'")
    if count == 0:
        cursor.execute("insert into event_host(name,email,phone,password,address,status,profile_pic) values('"+str(name)+"','"+str(email)+"','"+str(phone)+"','"+str(password)+"','"+str(address)+"','"+str(status)+"','"+str(picture.filename)+"')")
        conn.commit()
        return render_template("msg.html", message="Registration Successful")
    else:
        return render_template("msg.html", message="Duplicate Details")


@app.route("/customer_login")
def customer_login():
    return render_template("customer_login.html")


@app.route("/customer_login1", methods=['post'])
def customer_login1():
    email = request.form.get("email")
    password = request.form.get("password")
    query = "select * from customer where email ='"+str(email)+"' and password ='"+str(password)+"'"
    count = cursor.execute(query)
    if count != 0:
        customer = cursor.fetchall()
        session['customer_id'] = customer[0][0]
        session['role'] = 'customer'
        return redirect("/customer_home")
    else:
        return render_template("msg.html", message="Invalid Login Details")


@app.route("/customer_home")
def customer_home():
    customer_id = session["customer_id"]
    cursor.execute("select * from customer where customer_id='" + str(customer_id) + "' ")
    customer = cursor.fetchall()
    return render_template("customer_home.html", customer=customer[0])


@app.route("/book_event")
def book_event():
    event_id = request.args.get("event_id")
    cursor.execute("select * from event where event_id='"+str(event_id)+"'")
    event = cursor.fetchall()
    return render_template("book_event.html", event=event[0], is_seats_booked=is_seats_booked, int=int, get_seats_by_event_id=get_seats_by_event_id, get_place_by_place_id=get_place_by_place_id, get_event_host_by_event_host_id=get_event_host_by_event_host_id)


def is_seats_booked(i,event_id):
    query = "select * from booked_seats where seat_numbers = '"+str(i)+"' and booking_id in (select booking_id from booking where event_id ='"+str(event_id)+"' and status='Ticket Booked')"
    print(query)
    count = cursor.execute(query)
    if count == 0:
        return False
    else:
        return True


def get_seats_by_event_id(event_id):
    cursor.execute("select sum(number_of_tickets) from booking where event_id = '"+str(event_id)+"' and status = 'Ticket Booked'")
    booked_seats = cursor.fetchall()
    print(booked_seats)
    booked_seats = booked_seats[0][0]
    cursor.execute("select * from event where event_id = '"+str(event_id)+"'")
    events = cursor.fetchall()
    events = events[0]
    if booked_seats==None:
        return 0, int(events[12])
    remaining_seats = int(events[12])-int(booked_seats)
    return booked_seats, remaining_seats


def get_place_by_place_id(places_id):
    cursor.execute("select * from places where places_id = '"+str(places_id)+"'")
    places = cursor.fetchall()
    return places[0]


def get_event_host_by_event_host_id(event_host_id):
    cursor.execute("select * from event_host where event_host_id='"+str(event_host_id)+"'")
    event_hosts = cursor.fetchall()
    return event_hosts[0]


@app.route("/book_event_action", methods=['post'])
def book_event_action():
    customer_id = session['customer_id']
    event_id = request.form.get("event_id")
    cursor.execute("select * from event where event_id = '"+str(event_id)+"'")
    events = cursor.fetchall()
    cursor.execute("select * from coupons where status = 'Active'")
    coupons = cursor.fetchall()
    event = events[0]
    status = 'Payment pending'
    selected_seats = []

    if event[11] == 'non_layout':
        number_of_tickets = request.form.get('number_of_tickets')
        ticket_price = int(number_of_tickets) * int(event[7])

    elif event[11] == 'layout':
        for i in range(1, int(event[12])):
            selected_seat = request.form.get("seat_number"+str(i))
            if selected_seat is not None:
                selected_seats.append(selected_seat)
        number_of_tickets = len(selected_seats)
        ticket_price = int(number_of_tickets) * int(event[7])
    tax = int(ticket_price) * float(0.025)
    convenience_fee = int(ticket_price) * float(0.01)
    total_amount = int(ticket_price) + float(tax) + float(convenience_fee)
    cursor.execute("insert into booking(number_of_tickets,ticket_price,tax,convenience_fee,total_amount,status,event_id,customer_id) values('"+str(number_of_tickets)+"', '"+str(ticket_price)+"', '"+str(tax)+"', '"+str(convenience_fee)+"','"+str(total_amount)+"', '"+str(status)+"', '"+str(event_id)+"', '"+str(customer_id)+"')")
    conn.commit()
    booking_id = cursor.lastrowid
    for selected_seat in selected_seats:
        cursor.execute("insert into booked_seats(booking_id,seat_numbers,status) values('"+str(booking_id)+"','"+str(selected_seat)+"','"+str(status)+"')")
        conn.commit()
    cursor.execute("select * from booking where booking_id='"+str(booking_id)+"'")
    bookings = cursor.fetchall()
    return render_template("book_event_action.html", bookings=bookings, coupons=coupons, int=int, len=len, event=event, number_of_tickets=number_of_tickets, selected_seats=selected_seats, get_place_by_place_id=get_place_by_place_id, get_event_host_by_event_host_id=get_event_host_by_event_host_id)


@app.route("/bill", methods=['post'])
def bill():
    booking_id = request.form.get("booking_id")
    donations = request.form.get("donations")
    coupons_id = request.form.get("coupons_id")
    cursor.execute("update booking set  donations='" + str(donations) + "' where booking_id = '" + str(booking_id) + "' ")
    conn.commit()
    cursor.execute("select * from booking where booking_id ='"+str(booking_id)+"'")
    bookings = cursor.fetchall()
    total_amount = request.form.get("total_amount")
    total_amount = int(total_amount) + int(donations)
    cursor.execute("update booking set total_amount = '"+str(total_amount)+"' where booking_id ='"+str(booking_id)+"'")
    conn.commit()
    if coupons_id is not None:
        cursor.execute("update booking set  coupons_id='" + str(coupons_id) + "' where booking_id = '" + str(booking_id) + "' ")
        conn.commit()
        cursor.execute("select * from coupons where coupons_id ='" + str(coupons_id) + "'")
        coupons = cursor.fetchall()
        print(coupons)
        discount = coupons[0][4]
        discount_amount = int(total_amount) * (int(discount)/int(100))
        payable_amount = int(total_amount) - float(discount_amount)
    else:
        payable_amount = total_amount
    return render_template("bill.html", int=int, bookings=bookings, get_coupon_by_coupons_id=get_coupon_by_coupons_id, payable_amount=payable_amount)


def get_coupon_by_coupons_id(coupons_id):
    cursor.execute("select * from coupons where coupons_id = '"+str(coupons_id)+"' ")
    coupons = cursor.fetchall()
    return coupons[0]


@app.route("/payment")
def payment():
    booking_id = request.args.get("booking_id")
    payable_amount = request.args.get("payable_amount")
    return render_template("payment.html", booking_id=booking_id, payable_amount=payable_amount)


@app.route("/payment1", methods=['post'])
def payment1():
    card_holder_name = request.form.get("card_holder_name")
    card_number = request.form.get("card_number")
    cvv = request.form.get("cvv")
    expiry_date = request.form.get("expiry_date")
    booking_id = request.form.get("booking_id")
    amount = request.form.get("payable_amount")
    status = 'Payment Success'
    cursor.execute("insert into payment(card_holder_name,card_number,status,booking_id,cvv,expiry_date,amount) values('"+str(card_holder_name)+"','"+str(card_number)+"','"+str(status)+"','"+str(booking_id)+"','"+str(cvv)+"','"+str(expiry_date)+"','"+str(amount)+"')")
    conn.commit()
    cursor.execute("update booking set status='Ticket Booked' where booking_id ='"+str(booking_id)+"'")
    conn.commit()
    cursor.execute("update booked_seats set status='Ticket Booked' where booking_id ='" + str(booking_id) + "'")
    conn.commit()
    return render_template("msg.html", message="Ticket Booked successfully")


@app.route("/bookings")
def bookings():
    query = ""
    if session['role'] == 'customer':
        customer_id = session['customer_id']
        query = "select * from booking where customer_id = '"+str(customer_id)+"'"
    elif session['role'] != 'customer':
        event_id = request.args.get("event_id")
        query = "select * from booking where event_id = '"+str(event_id)+"'"
    cursor.execute(query)
    bookings = cursor.fetchall()
    return render_template("bookings.html", bookings=bookings, get_booked_seats_by_booking_id=get_booked_seats_by_booking_id, get_bookings_by_booking_id=get_bookings_by_booking_id, get_event_by_event_id=get_event_by_event_id, get_place_by_place_id=get_place_by_place_id, get_customer_by_customer_id=get_customer_by_customer_id)


def get_booked_seats_by_booking_id(booking_id):
    cursor.execute("select * from booked_seats where booking_id = '"+str(booking_id)+"'")
    booked_seats = cursor.fetchall()
    if(len(booked_seats)) == 0:
        return None
    return booked_seats


def get_bookings_by_booking_id(booking_id):
    cursor.execute("select * from booking where booking_id = '"+str(booking_id)+"'")
    bookings = cursor.fetchall()
    return bookings[0]


def get_event_by_event_id(event_id):
    cursor.execute("select * from event where event_id='"+str(event_id)+"'")
    events = cursor.fetchall()
    return events[0]


def get_customer_by_customer_id(customer_id):
    cursor.execute("select * from customer where customer_id='"+str(customer_id)+"'")
    customer = cursor.fetchall()
    return customer[0]


@app.route("/cancel_booking", methods=['post'])
def cancel_booking():
    booking_id = request.form.get("booking_id")
    cursor.execute("update booking set status = 'Ticket Cancelled' where booking_id ='"+str(booking_id)+"'")
    conn.commit()
    return render_template("msg.html", message="Ticket Cancelled Successfully")


@app.route("/review_rating", methods=['post'])
def review_rating():
    booking_id = request.form.get("booking_id")
    return render_template("review_rating.html", booking_id=booking_id)


@app.route("/review_rating1", methods=['post'])
def review_rating1():
    review = request.form.get("review")
    rating = request.form.get("rating")
    booking_id = request.form.get("booking_id")
    cursor.execute("insert into review_rating(review,rating,booking_id) values('"+str(review)+"', '"+str(rating)+"', '"+str(booking_id)+"')")
    conn.commit()
    return render_template("msg.html", message="Thanks for giving Review&Rating")


@app.route("/customer_registration")
def customer_registration():
    return render_template("customer_registration.html")


@app.route("/customer_registration1", methods=['post'])
def customer_registration1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    gender = request.form.get("gender")
    picture = request.files.get("picture")
    path = APP_ROOT + "/customer/" + picture.filename
    picture.save(path)
    query = "select * from customer where email = '"+str(email)+"' and phone = '"+str(phone)+"'"
    count = cursor.execute(query)
    if count == 0:
        cursor.execute("insert into customer(name,email,phone,password,gender,profile_pic) values('"+str(name)+"','"+str(email)+"','"+str(phone)+"','"+str(password)+"','"+str(gender)+"','"+str(picture.filename)+"')")
        conn.commit()
        return render_template("msg.html", message="Registration Successful")
    else:
        return render_template("msg.html", message="Duplicate Details")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


app.run(debug=True)
