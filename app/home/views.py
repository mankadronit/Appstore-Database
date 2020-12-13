# app/home/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, current_user
import MySQLdb
import os
import random


from . import home
from .forms import DeveloperForm, ApplicationForm


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    if current_user:
        return render_template('home/dashboard.html')
    else:
        return render_template('home/index.html', title="Welcome")


@home.route('/home/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")


# developer Views
@home.route('/developers', methods=['GET', 'POST'])
@login_required
def list_developers():
    """
    List all developers
    """
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from developers;"
    cur.execute(query_string)

    developers = cur.fetchall()

    db.close()


    return render_template('home/developers/developers.html',
                           developers=developers, title="Developers")


@home.route('/home/developers/add', methods=['GET', 'POST'])
@login_required
def add_developer():
    """
    Add a developer to the database
    """
    add_developer = True

    form = DeveloperForm()

    if form.validate_on_submit():
        try:
            pk = random.getrandbits(32)
            #print(pk)
            # add developer to the database
            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "INSERT INTO developers \
                            VALUES(%s, %s, %s, %s, %s, %s, %s);"

            cur.execute(query_string, (pk, 
                                                                       form.name.data, 
                                                                       form.email.data,
                                                                       form.country.data,
                                                                       form.address.data,
                                                                       form.website.data,
                                                                       form.bank_acc_number.data))
            db.commit()
            db.close()

            flash('You have successfully added a new developer.')
            #print("COMPLETED!!!")
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            # in case developer name already exists
            flash('Error: Developer Name already exists.')

            # redirect to developers page
        return redirect(url_for('home.list_developers'))

    #flash("DonE!!!!")
    # load developer template
    return render_template('home/developers/developer.html', action="Add",
                           add_developer=add_developer, form=form,
                           title="Add developer")





@home.route('/home/developers/edit/<int:developer_id>', methods=['GET', 'POST'])
@login_required
def edit_developer(developer_id):
    """
    Edit a developer
    """
    add_developer = False

    form = DeveloperForm()

    if form.validate_on_submit():
        try:
            #print(pk)
            # add developer to the database
            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "UPDATE developers SET \
                            name = %s, email = %s, country = %s, address = %s, \
                            website = %s, bank_acc_number = %s \
                            WHERE developer_id = %s"
            cur.execute(query_string, (form.name.data, 
                                        form.email.data,
                                        form.country.data,
                                        form.address.data,
                                        form.website.data,
                                        form.bank_acc_number.data,
                                        developer_id))
            db.commit()
            db.close()

            flash('You have successfully Edited the developer information.')
            #print("COMPLETED!!!")
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            # in case developer name already exists
            flash('Error: Could Not Update Developer Information')

            # redirect to developers page
        return redirect(url_for('home.list_developers'))

    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from developers WHERE developer_id = {};".format(developer_id)
    cur.execute(query_string)

    developer = cur.fetchone()

    db.close()

    print("ROW:", developer)
    
    form.bank_acc_number.data = developer[6]
    form.address.data = developer[5]
    form.website.data = developer[4]
    form.country.data = developer[3]
    form.email.data = developer[2]
    form.name.data = developer[1]

    return render_template('home/developers/developer.html', action="Edit",
                           add_developer=add_developer, form=form,
                           developer=developer, title="Edit developer")


@home.route('/home/developers/delete/<int:developer_id>', methods=['GET', 'POST'])
@login_required
def delete_developer(developer_id):
    """
    Delete a developer from the database
    """
    try:
        #print(pk)
        # add developer to the database
        db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

        cur = db.cursor()

        query_string = "DELETE FROM developers WHERE developer_id = {}".format(developer_id);

        cur.execute(query_string)
        db.commit()
        db.close()

        flash('You have successfully deleted a developer.')
        #print("COMPLETED!!!")
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        # in case developer name already exists
        flash('Error: Developer Doesnt exists.')
    # redirect to the developers page
    return redirect(url_for('home.list_developers'))


# developer Views
@home.route('/home/applications', methods=['GET', 'POST'])
@login_required
def list_applications():
    """
    List all developers
    """
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from applications;"
    cur.execute(query_string)

    applications = cur.fetchall()

    db.close()


    return render_template('home/applications/applications.html',
                           applications=applications, title="Applications")


@home.route('/home/applications/add/dev', methods=['GET', 'POST'])
@login_required
def add_app_under_dev():
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from developers;"
    cur.execute(query_string)

    developers = cur.fetchall()

    db.close()


    return render_template('/home/applications/developers_compact.html',
                           developers=developers, title="Developers")


@home.route('/applications/add/dev/<int:developer_id>', methods=['GET', 'POST'])
@login_required
def add_application(developer_id):
    """
    Add a developer to the database
    """
    add_app = True

    form = ApplicationForm()

    if form.validate_on_submit():
        try:

            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "INSERT INTO applications \
                            VALUES(%s, %s, %s, %s, %s);"

            cur.execute(query_string, (form.package_name.data, 
                                        developer_id,
                                        form.name.data,
                                        form.app_type.data,
                                        form.price.data))
            db.commit()
            db.close()

            flash('You have successfully added a new Application.')
            print("COMPLETED!!!")
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            # in case developer name already exists
            flash('Error: Application already exists.')

            # redirect to developers page
        return redirect(url_for('home.list_applications'))

    #flash("DonE!!!!")
    # load developer template
    return render_template('home/applications/application.html', action="Add",
                           add_app=add_app, form=form,
                           title="Add Application")

@home.route('/home/applications/delete/<string:package_name>', methods=['GET', 'POST'])
@login_required
def delete_app(package_name):
    """
    Delete a developer from the database
    """
    try:
        #print(pk)
        # add developer to the database
        db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

        cur = db.cursor()

        query_string = "DELETE FROM applications WHERE package_name='{}'".format(package_name);

        cur.execute(query_string)
        db.commit()
        db.close()

        flash('You have successfully deleted an application.')
        #print("COMPLETED!!!")
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        # in case developer name already exists
        flash('Error: Application Doesnt exists.')
    # redirect to the developers page
    return redirect(url_for('home.list_applications'))


@home.route('/home/applications/edit/<int:developer_id>/<string:package_name>,', methods=['GET', 'POST'])
@login_required
def edit_app(developer_id, package_name):
    """
    Edit a developer
    """
    add_app = False

    form = ApplicationForm()
    new_package_name = None
    if form.validate_on_submit():
        try:
            #print(pk)
            # add developer to the database
            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "UPDATE applications SET \
                            package_name = %s, developer_id = %s, name = %s, app_type = %s, \
                            price = %s \
                            WHERE package_name = %s"
            cur.execute(query_string, (form.package_name.data,
                                       developer_id,
                                       form.name.data,
                                       form.app_type.data,
                                       form.price.data,
                                       package_name))
            db.commit()
            db.close()

            new_package_name = form.package_name.data
            flash('You have successfully Edited the App information.')
            print("COMPLETED!!!")
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            # in case developer name already exists
            flash('Error: Could Not Update App Information')

            # redirect to developers page
        return redirect(url_for('home.list_applications'))

    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from applications WHERE package_name='{}';".format(package_name)
    cur.execute(query_string)

    application = cur.fetchone()

    db.close()

    print("ROW:", application)
    
    form.package_name.data = application[0]
    form.name.data = application[2]
    form.app_type.data = application[3]
    form.price.data = application[4]


    return render_template('home/applications/application.html', action="Edit",
                           add_app=add_app, form=form,
                           application=application, title="Edit Application")
