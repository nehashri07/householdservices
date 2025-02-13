from flask import Flask, flash, render_template, request, url_for, redirect
from .models import *
from flask import current_app as app
from datetime import date, datetime
from sqlalchemy import func
import matplotlib.pyplot as plt

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        uname = request.form.get("user_name")
        pwd = request.form.get("password")
        
        
        # Check if user exists
        usr = User.query.filter_by(email=uname).first()
        p_usr= Professional.query.filter_by(email=uname).first()
        if (usr and usr.password == pwd) or (p_usr and p_usr.password == pwd):
            print("Password matches")
            if p_usr  and not usr:
                return redirect(url_for("pro_dashboard",name=uname))
            if (usr.id == 1):
                
                return redirect(url_for("admin_dashboard",name=uname))
            else:
                return redirect(url_for("user_dashboard",name=uname))
        else:
            print("Password does not match")
            return render_template("login.html", msg="Invalid user credentials...")

    return render_template("login.html", msg="")

@app.route("/register", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uname = request.form.get("user_name")
        pwd = request.form.get("password")
        fname = request.form.get("full_name")
        address = request.form.get("address")
        pin = request.form.get("pin_code")

       
        usr = User.query.filter_by(email=uname).first()
        if usr:
            return render_template("register.html", msg="Sorry, this email is already registered!")
        
       
        new_usr = User(email=uname, password=pwd, full_name=fname, address=address, pin_code=pin)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html", msg="Registration successful, please log in.")

    return render_template("register.html")

@app.route("/proregister",methods=["POST","GET"])
def prosignup():
    if request.method == "POST":
        pname = request.form.get("pro_name")
        pwd = request.form.get("password")
        fname = request.form.get("full_name")
        address = request.form.get("address")
        pin = request.form.get("pin_code")
        service = request.form.get("service_name")
        experience = request.form.get("experience")
        phone_number = request.form.get("phone_no")
        
        pro = Professional.query.filter_by(email=pname).first()
        if pro:
            return render_template("proregister.html", msg="Sorry, this email is already registered!")
        
        new_pro = Professional(email=pname, password=pwd, full_name=fname, address=address, pin_code=pin, service_name=service, experience=experience, phone_no=phone_number    )
        db.session.add(new_pro)
        db.session.commit()
        return render_template("login.html", msg="Registration successful, please log in.")

    return render_template("proregister.html")



#common route for admindash
@app.route("/admin/<name>")
def admin_dashboard(name):
    professional=get_pros()
    service=get_services()
    user=get_users()
    service_request=get_service_request()
    return render_template("admindash.html",name=name,service=service,professional=professional,user=user, service_request=service_request)

@app.route("/user/<name>")
def user_dashboard(name):
    service=get_services()
  
    service_request=get_service_request()
    return render_template("userdash.html",name=name, service=service , service_request=service_request)

@app.route("/pro/<name>")
def pro_dashboard(name):
    service_request=get_service_request()
    return render_template("prodash.html",name=name,service_request=service_request)


@app.route("/add_services/<name>", methods=["POST","GET"])
def add_services(name):
    if request.method == "POST":
        
        sname = request.form.get("service_name")
        description = request.form.get("description")
        base_price = request.form.get("base_price")
        new_service=Service(service_name=sname, description=description, base_price=base_price)
        db.session.add(new_service)
                
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("add_service.html", name=name)
@app.route("/admin/search/<name>", methods=["GET","POST"])
def search(name):
    if request.method=="POST":
        search_txt= request.form.get("search_txt")
        by_service= search_by_service(search_txt)
        by_professionals= search_by_professional(search_txt)
        by_users=search_by_user(search_txt)
        if by_service or by_professionals or by_users :
            return render_template("admindash.html", name=name, service=by_service,professional=by_professionals, user=by_users)
       

    return redirect(url_for("admin_dashboard",name=name))

@app.route("/user/search/<name>", methods=["GET","POST"])
def user_search(name):
    if request.method=="POST":
        search_txt= request.form.get("search_txt")
        by_service= search_by_service(search_txt)
        by_professionals= search_by_professional(search_txt)
        by_users=search_by_user(search_txt)
        if by_service or by_professionals or by_users :
            return render_template("userdash.html", name=name, service=by_service,professional=by_professionals, user=by_users)
       

    return redirect(url_for("user_dashboard",name=name))


@app.route("/admin_summary/<name>")
def admin_summary(name):
    plot=get_service_request_summary()
    plot.savefig("./static/images/service_request_summary.jpeg")
    plot.clf()
    return render_template("admin_summary.html",name=name)

@app.route('/edit_service/<id>/<name>', methods=['GET', 'POST'])
def edit_service(id, name):
    s = get_service(id)
    if request.method == 'POST':
        service_name = request.form.get("service_name")
        base_price = request.form.get("base_price")
        description = request.form.get("description")
        s.service_name=service_name
        s.base_price=base_price
        s.description=description
        print("yes")
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))  # Redirect to services page
    return render_template('edit_service.html', service=s, name=name)

@app.route('/delete_service/<id>/<name>', methods=['POST'])
def delete_service(id,name):
    service = get_service(id)
    if service:
        db.session.delete(service)
        db.session.commit()
   
    return redirect(url_for('admin_dashboard', name=name))  # Redirect to services page
  # Redirect to services page
@app.route('/delete_pro/<id>/<name>', methods=['POST'])
def delete_pro(id,name):
    pro = get_pro(id)
    if pro:
        db.session.delete(pro)
        db.session.commit()
   
    return redirect(url_for('admin_dashboard', name=name))  # Redirect to services page
  # Redirect to services page
@app.route('/delete_usr/<id>/<name>', methods=['POST'])
def delete_usr(id,name):
    usr = get_user(id)
    if usr:
        db.session.delete(usr)
        db.session.commit()
   
    return redirect(url_for('admin_dashboard', name=name))  # Redirect to services page


def get_services():
     Services= Service.query.all()
     return Services
def get_service_request():
     service_req = ServiceRequest.query.all()

     return service_req

def get_service(id):
     service = Service.query.filter_by(id=id).first()
     return service
def get_pro(id):
     pro = Professional.query.filter_by(id=id).first()
     return pro
def get_pros():
     pros= Professional.query.all()
     return pros
def get_users():
     usr= User.query.all()
     return usr
def get_user(id):
     usr = User.query.filter_by(id=id).first()
     return usr
def search_by_service(search_txt):
    if not search_txt:
        return []
    services = Service.query.filter(Service.service_name.ilike(f'%{search_txt}%')).all()
    return services

def search_by_professional(search_txt):
    if not search_txt:
        return []
    professionals = Professional.query.filter(Professional.full_name.ilike(f'%{search_txt}%')).all()
    return professionals

def search_by_user(search_txt):
    if not search_txt:
        return []
    usr = User.query.filter(User.full_name.ilike(f'%{search_txt}%')).all()
    return usr


def get_service_request_summary():
    Service = get_service_request()
    
    summary = {}
    for s in Service:
        if s.rating is not None:
            summary[s.id] = s.rating
        else:
            summary[s.id] = 0

    x_names = list(summary.keys())
    y_names = list(summary.values())

    fig, ax = plt.subplots()
    ax.bar(x_names, y_names, color="blue", width=0.8)
    ax.set_xlabel("Services")
    ax.set_ylabel("Ratings")

    return fig  # Return the figure object
@app.route('/professional_dashboard/<int:pro_id>')
def professional_dashboard(pro_id):
    # Retrieve all pending service requests for the professional
    pending_requests = ServiceRequest.query.filter_by(pro_id=None, status="Requested").all()  # Filter by "Requested" status
    
    return render_template('prodash.html', requests=pending_requests, pro_id=pro_id)

@app.route('/accept_request/<id>', methods=['GET', 'POST'])
def accept_request(id):
    request = ServiceRequest.query.get(id)
    if request:
        request.status = "Approved"
        # Assign the professional to the request
        request.pro_id = request.pro_id
        db.session.commit()
        return redirect(url_for('professional_dashboard', pro_id=request.pro_id))  # Redirect back to dashboard
    
    return "Request not found", 404

@app.route('/reject_request/<int:request_id>/<name>', methods=['GET', 'POST'])
def reject_request(request_id,name):
    request = ServiceRequest.query.get(request_id)
    if request:
        request.status = "Rejected"
        db.session.commit()
        return redirect(url_for('professional_dashboard', pro_id=request.pro_id, name=name))  # Redirect back to dashboard
    
    return "Request not found", 404



# chat

@app.route("/book_service/<sid>/<name>",methods=["GET","POST"])
def book_ticket(sid,name):
    if request.method=="POST":
       
        date= request.form.get("date")
        
        new_ticket=ServiceRequest(status="Pending",user_id=name,s_id=sid,pro_id=0,date=date)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for("user_dashboard",name=name))

    
    service=Service.query.filter_by(id=sid).first()
    user=User.query.filter_by(email=name).first()
  
    
    return render_template("book_service.html",uid=user.id,sid=sid,name=name, service=service)

@app.route("/close_service/<name>",methods=["GET","POST"])
def close_ticket(sid,name):
    if request.method=="POST":
       
        date= request.form.get("date")
        
        new_ticket=ServiceRequest(status="Completed",user_id=name,s_id=sid,pro_id=0,date=date)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for("user_dashboard",name=name))

    
    service=Service.query.filter_by(id=sid).first()
    user=User.query.filter_by(email=name).first()
  
    
    return render_template("close_service.html",uid=user.id,sid=sid,name=name, service=service)