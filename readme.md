# Build a Community Board with Flask and MongoDB (with a little help from PyMongo)

1. Intro
2. Initial Setup
    1. [Connect to MongoDB](#connect-to-mongodb)
    2. [Push Data to MongoDB](#push-data-to-mongodb)
    3. [Queries of MongoDB](#queries-of-mongodb)
    4. [Sorting and Limiting Query Results](#sorting-and-limiting-query-results)
    5. [Push to Heroku](#push-to-heroku)
3. Extensions
    1. [Individual Post Pages](#individual-post-pages)
    2. [User Accounts](#user-accounts)
    3. [New User Sign Up](#new-user-sign-up)
    4. [Logging In](#logging-in)
    5. [Logging Out](#logging-out)
    6. [Gated Pages](#gated-pages)
4. Reach Extensions
    1. [Date Formatting](#date-formatting)
    2. [Environment Variables](#environment-variables)
    3. [Password Hashing](#password-hashing)

## Intro

Now that you and your students have built an app using Flask, you might have recognized a need to store and retrieve data. For this, we're going to use a database called MongoDB.

### Show Me a Demo First

If you've come just looking to run the demo code, this is a list of the packages you'll want to make sure you've installed. If you're using your own development environment, these should work as written.

> In [ide.cs50.io](https://ide.cs50.io), you may need to add a `--user` flag at the end of each: `pip install <package> --user`. 

```python
pip install flask
pip install flask-pymongo # for mongodb connection
pip install dnspython # for mongodb connection
pip install bcrypt # for password handling
pip install bson # for page/post
pip install datetime # for prettifying dates
pip install python-dotenv # for .env variables
```

Or all in one:

```python
pip install flask flask-pymongo dnspython bcrypt bson datetime python-dotenv
```

And you'll need to export these variables in the Terminal:

```bash
export FLASK_APP=main.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
export FLASK_DEBUG=1
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
```

To view the finished app:

- First create a `.env` file with these credentials:
```bash
MONGO_USERNAME="admin"
MONGO_PASSWORD="6zCs4vJtrzwkLBqL"
```
- Then rename the `routes.py` starter template to anything else, and rename `routes-complete.py` to `routes.py`.
- Lastly, execute `flask run` in the Terminal as before.

> Test out how to submit an event, sign up, log in, view an event page, and log out.
> Examine (the newly named) `routes.py` to see how each action is implemented.

### How'd You Make That?

Read on for the steps and lessons to build that completed Flask + MongoDB app.

## Initial Setup

> Although you may be tempted to dive into a mini-lesson about "What is a database?" because it's tempting to want to share every bit of background knowledge with students, our experience has taught us that students need to see **that** the app can work before they become interested in the nuances of **why** it works exactly as it does. So don't feel like you ought to spend much time on this concept your first time through.
> 
> We've also picked out a few other times in these lessons where you may be tempted to dive deep into a topic, but it may be better to reserve that enthusiasm.

To get started using MongoDB as a database, you'll want to sign up for an Atlas (free) account at [mongodb.com](https://www.mongodb.com/). The sign up process is a bit lengthy, but it involves:

- Signing up with a (valid) email address
  > If you're demoing this sign-up for students and you have a gmail account you've already used to sign up, consider using `yourname+mongo@gmail.com` (or some variant) to sign up as a new user.
- Submitting your name and creating a password
- When asked to create your first cluster, you can either follow the prompts, or close the dialog box.
- If you close the dialog, you'll be presented with options for the "Cloud Provider" and "Region".
  > We suggest using AWS as the "Cloud Provider" and the region geographically closest to you.
- Choose the "M0" cluster tier to keep things free.
- No "Backup" is needed.
- And you can give the cluster a name or use the default "Cluster0"
- Finally, tap the green "Create Cluster" button.
  > It will take 7-10 minutes to create the cluster, so it's best to create the MongoDB account before taking a break.

While the cluster is being created in the cloud, you can begin the installation of the modules necessary to use MongoDB with Flask:

- a Python toolkit to connect to MongoDB built especially for Flask (`flask-pymongo`), and
- a DNS toolkit for Python (`dnspython`).

In the Terminal:

```bash
pip install flask-pymongo
pip install dnspython
```

Once the cluster is created on MongoDB, we need to do three things to complete the database setup before we can connect to it from our app:

- [Create a database](#create-a-database)
- [Create a database user](#create-a-database-user)
- [Whitelist IP addresses](#whitelist-ip-addresses)

#### Create a database

To create a database in the MongoDB interface, click on the name of the cluster, e.g. `Cluster0` and then on the "Collections" heading (or just on the "Collections" button below the cluster name).

![Initial View in MongoDB Interface](screenshots/mongodb-1-initial.png "Initial View in MongoDB Interface")

> You'll notice a MongoDB "checklist" pop up as you get set up. It's worth calling out the user experience of building a new cluster/database/collection on MongoDB. Do students think it's good? bad? intuitive? confusing?

In the "Collections" tab, you'll be prompted with a big green button to "Create Database" - tap that button.

![Collections View in MongoDB Interface](screenshots/mongodb-3-collections.png "Collections View in MongoDB Interface")

You'll then be prompted to give the database a name (it can be anything, e.g. `test`) and to create the first collection by giving it a name (it can also be anything, e.g. `events`). Later, we'll see that when adding data to a database, if you are sending data to a collection that doesn't (yet) exist, MongoDB will create that collection for you. So there's no need to stress about getting this perfect from the beginning.

![Create Database in MongoDB Interface](screenshots/mongodb-5-create-database.png "Create Database in MongoDB Interface")

> You don't need to check "Capped Collection".

We now have our first database! But before we can connect to it, we need to set up our first database user.

#### Create a database user

To create a database user, return to the Clusters overview by clicking on "Clusters" in the left sidebar. Once there, select the "Security" tab.

![Security View in MongoDB Interface](screenshots/mongodb-6-create-database-user.png "Security View in MongoDB Interface")

Notice the green button in the top-right corner that says "+ Add New User" - go ahead and tap that.

Choose a username, e.g. `admin` and (secure) password, e.g. `Ypzb8UvmWKXJsubU`, and make a note of the password you've selected.

![Add New User in MongoDB Interface](screenshots/mongodb-7-add-new-user.png "Add New User in MongoDB Interface")

> We suggest tapping "Autogenerate Secure Password" to create a compliant password. Then tap "Show" and copy-and-paste the password somewhere safe.

When creating a user, you can set various privileges for that user. For this app, we're just going to keep the default "Read and write to any database" permissions.

Tap "Add User" to complete the creation of your first database user!

#### Whitelist IP addresses

> Resist the temptation to go too deep into "What is an IP Address?" your first time through.

Now we need to let MongoDB know the IP addresses from which it is safe to access our database and to which it is safe to send data from the database.

Still on the "Security" tab, you'll now see the user you just created. Tap the "IP Whitelist" sub-tab to view a list of the safe IP addresses.

![Whitelist IP Address in MongoDB Interface](screenshots/mongodb-9-ip-whitelist.png "Whitelist IP Address in MongoDB Interface")

Again, tap the green button in the top-right labeled "+ Add IP Address".

We're presented with an option to just add the current IP address, to allow access from anywhere, or to list a particular IP address. Since most students will want their app to be accessed by anyone anywhere (and since they should not be storing particularly sensitive data), it's ok to tap the "Allow Access from Anywhere" button. Add a comment, e.g. "Global access", then tap "Confirm".

![Whitelist IP Address in MongoDB Interface](screenshots/mongodb-10-add-whitelist.png "Whitelist IP Address in MongoDB Interface")

> It may take a moment for the "Allow Access from Anywhere" setting to be implemented.

### Connect to MongoDB

To facilitate connecting to MongoDB, we'll be using the module we installed called Flask-PyMongo. Flask-PyMongo is a set of Python tools for interacting with MongoDB that have been wrapped to integrate well with Flask.

We've already installed the module, but we needed to import it to our app:

```python
from flask_pymongo import PyMongo
```

To connect to our MongoDB, we need to specify two configuration parameters: 'MONGO_DBNAME' and 'MONGO_URI'. This is done by assigning values to two new `app.config` properties:

```python
# name of database
app.config['MONGO_DBNAME'] = 'database-name' 

# URI of database
app.config['MONGO_URI'] = 'mongo-uri'
```

We should replace `database-name` with the name of the database we created in the MongoDB interface, e.g. `test`.

To get our `mongo-uri`, we need to head back to the MongoDB interface. Click to the "Overview" tab, and tap the "Connect" button below the name of the cluster.

![Overview in MongoDB Interface](screenshots/mongodb-11-overview.png "Overview in MongoDB Interface")

Here we'll choose the middle option, "Connect Your Application".

![Connect to Cluster in MongoDB Interface](screenshots/mongodb-12-connect-to-db.png "Connect to Cluster in MongoDB Interface")

Because we're using Python 3.7, we want to select the "Python" driver and the version of "3.6 or later". That will populate the Connection String Only box with a URI that is (mostly) the `mongo-uri`.

![Connect to Cluster in MongoDB Interface](screenshots/mongodb-13-connect-to-db.png "Connect to Cluster in MongoDB Interface")

If you examine the URI closely, you'll notice that our user's username has been included in the URI, but the password is represented as `<password>`. Before we can connect to our database, we'll need to replace `<password>` with our password that we stored somewhere secure.

Setting the configuration parameters should now look like:

```python
# name of database
app.config['MONGO_DBNAME'] = 'test' 

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:Ypzb8UvmWKXJsubU@cluster0-kxrbn.mongodb.net/test?retryWrites=true'
```

> It's worth noting that the default URI in the "Connect Your Application" dialog box is for node.js (3.0 or later), and it is exactly the same as the driver for Python (3.6 or later). If a student misses switching the driver, it won't actually matter.

> It's also worth noting that the second module we installed, `dnspython`, is necessary to account for the `+srv` in the 'MONGO_URI'.

The final part of setting up the connection between our app and our MongoDB is to create a new variable called `mongo` that will use PyMongo to connect our app to the database using the aforementioned configuration variables:

```python
mongo = PyMongo(app)
```

That may seem like a lot of work to get things set up, but a bit of setup will make our lives a lot easier down the line when we're reading data from and writing data to MongoDB.

### Push Data to MongoDB

#### Write Data Directly to MongoDB

To find out whether our app is correctly configured to connect to our MongoDB, we can add a new route to our app that will just write data to our database:

```python
@app.route('/add')

def add():
    user = mongo.db.users
    user.insert({'name':'Your Name'})
    return 'Added User!'
```

In the `add()` function, we first indicate which collection we want to write data to. In this case, we've selected the `users` collection. What's that? We don't yet have a `users` collection? MongoDB is smart enough to recognize that if we're writing data to a collection that doesn't yet exist, it will first create that new collection then add the data to it.

We next use the `.insert()` method to add a simple JSON object to the database. Here we're only specifying one property, `'name'`, with the value `'Your Name'`. Try replacing `'Your Name'` with your name or other names.

Lastly, the function will return the text "Added User!" on the page.

With Flask running, once you've added this new route and successfully gotten a page that says "Added User!", head back to your MongoDB interface, navigate to your "Collections" (using the "Collections" button on the "Overview"), and notice that you have a new collection called `users`. Clicking on that collection should show a new entry with the name you submitted!

#### Using a Form to Collect Data

Using the backend to write data to a database is not very user-friendly. Instead, we'd ideally use a form to collect the user's data and then store that data to the database. Let's do this by adding a new route and a new HTML template:

```python
@app.route('/events/new', methods=['GET', 'POST'])

def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    else:
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        user_name = request.form['user_name']

        events = mongo.db.events
        events.insert({'event': event_name, 'date': event_date, 'user': user_name})
        return redirect('/')
```

And the corresponding HTML snippet:

```html
<form method="post" action="/events/new">
    <label for="event_name">Event Name:</label>
    <input type="text" name="event_name" value="">
    <label for="event_date">Date:</label>
    <input type="date" name="event_date" value="">
    <label for="name">Name:</label>
    <input type="name" name="user_name" value="">
    <input type="submit" value="Submit">
</form>
```

By now you should be familiar with the different between `GET` and `POST` requests. This route shows the user the `new_event.html` template if the page is accessed via a `GET` request. If, however, the route is accessed via a `POST` request, it will collect the data from the form and store it to the database.

By now you should also be familiar with the `request` function in Flask. Here it is used to store each of the user-submitted values to a variable. Next the MongoDB collection which is the target for the data is specified, `events`, and new data is added to the collection as a JSON object via the `.insert()` method we saw before. Lastly, the user is redirected to the homepage.

### Queries of MongoDB

> Resist the temptation to go too deep into "What is a query?" your first time through.

We've now seen how to write data to MongoDB, but we also want to read (and display) data from MongoDB. To do this, we will need to query, or request particular data from, MongoDB.

PyMongo and Flask-PyMongo have a number of useful built-in query methods:

- `.find({})` - will find multiple entries that match the criteria in the `{}`. Returns all documents that match the criteria.
- `.find_one({})` - will find a single entry that matches the criteria in the `{}`. Returns a single document.
- `.find_one_and_delete({})` - will find and delete one document that matches the criteria in the `{}`.
- `.find_one_and_replace({}, {})` - will find one document that matches the criteria in the first `{}` and replace it with the second `{}`.

> Read about additional query methods in the [PyMongo API Documentation](http://api.mongodb.com/python/current/api/pymongo/collection.html)

To see querying in action, we'll start with the most general search of all. Using the `.find({})` method with empty `{}` (or with no `{}` at all) will return all items in the database.

```python
@app.route('/events')

def events():
    collection = mongo.db.events
    events = collection.find({})

    return render_template('events.html', events = events)
```

Again, we first define the collection in our MongoDB we want to query. We then run the `.find({})` query on that collection and store the results in the `events` variable which is sent to the template in the `render_template()` function.

And an HTML snippet for that route:

```html
<div>
    <ul>
        {% for event in events %}
            <li>{{ event.event }} - {{ event.date }}</li>
        {% endfor %}
    </ul>
</div>
```

> We use the handlebar-percent syntax to execute a `for` loop over all of the entries in the `events` array. This will result in creating all of the `<li>`'s within the `<ul>`, one for each entry in `events`.

But what if instead of all documents, you only wanted to find the ones that match some criteria? The method you should use will depend on whether or not the result of the query is unique.

If the query may return multiple documents, you can use the `.find({})` method with search criteria to match against, e.g.:

```python
events = collection.find({'event' : 'Submit Homework'})
```

This would find *all* events for which the `event` property is `'Submit Homework` and return an iterable object.

But what if you know there's only one such entry, for example when searching a list of users for only one particular user (since users must be unique). Instead of using the `.find({})` query method, we can use the `.find_one({})` query method:

```python
user = users.find_one({'name' : 'My Name'})
```

The `.find_one({})` query method is particularly useful when searching a collection in which documents are assigned unique id's.

### Sorting and Limiting Query Results

In addition to finding documents that match a particular query, you may also want to sort the results and/or limit the search to the first n-many results. PyMongo has two methods to help us do just that.

#### Sorting Query Results

The `.sort()` method is used to rearrange the documents that are returned according to some criteria. For example, to sort the events from oldest to newest, we might sort by a `date` parameter and provide an indicator that we want the results in *ascending* order (`1`):

```python
events = collection.find({}).sort('date', 1) 
```

If we wanted the results in descending order from newest to oldest, we just switch the `1` to `-1`:

```python
events = collection.find({}).sort('date', -1) 
```

It is also possible to sort data by multiple fields, e.g.:

```python
events = collection.find({}).sort([('date', pymongo.ASCENDING), ('price', pymongo.DESCENDING)]) 
```

This query would find all events, then sort the results first by date (oldest to newest), then by price (highest to lowest).

- Consider how a user would find it most useful to see the data and design a corresponding query. 

#### Limiting Query Results

The `.limit()` method is useful for larger datasets where you may only want to show a few results. This query would only show the first 10 documents in a collection:

```python
events = collection.find({}).limit(10) 
```

#### Complex Queries

`.sort()` and `.limit()` can be chained together with `.find({})` to produce complex queries. This query would sort all entries in a collection by the `date` field (newest to oldest) and then include only the first 5:

```python
events = collection.find({}).sort('date', -1).limit(5) 
```

> According to the [documentation](https://docs.mongodb.com/manual/reference/method/db.collection.find/#combine-cursor-methods), `.sort()` is always run before `.limit()` irrespective of the order in which they are chained.
> ```python
> # These are equivalent
> events = collection.find({}).sort('date', -1).limit(5)
> events = collection.find({}).limit(5).sort('date', -1)
> ```

> Also check out the [MongoDB Python Documentation for Iterating Over Query Results](http://api.mongodb.com/python/current/api/pymongo/cursor.html)

### Push to Heroku

- Test this from ide.goorm.io

## Extensions

### Individual Post Pages

Now that we have individual posts stored in our MongoDB database with unique identifiers, `_id`'s, we can consider how to show a unique page for each. Adding a new route for each new post would be massively inefficient, so instead, we'll make use of variables in the route name and definition.

Before we write a new route, we'll want to make sure we've installed the `bson` module. The `bson` module will help us convert `ObjectId`s into usable strings we can more-easily work with in our database.

```bash
pip install bson
```

We'll need to add an import statement in our app, as well:

```python
from bson.objectid import ObjectId
```

Next we'll write a new route that includes the `<eventID>` variable as part of the route name itself. We'll then pass that same `eventID` variable to the `event()` function.

In the `event()` function:

- We first define the collection in the MongoDB we plan to use.
- Then we'll filter the collection to retrieve only the event that has an `_id` that matches the `eventID` variable.
- This event is then passed to the `event.html` template to be rendered for the user.

```python
@app.route('/events/<eventID>')

def event(eventID):
    collection = mongo.db.events
    event = collection.find_one({'_id' : ObjectId(eventID)})

    return render_template('event.html', event = event)
```

And an HTML snippet to show the filtered data:

```html
<div>
    <h1>{{ event.event }} ({{ event.date }})</h1>
    <h3>Posted by {{ event.user }}</h3>
</div>
```

### User Accounts & Sessions

> Resist the temptation to go too deep into "What is a session? What is a cookie?" your first time through.

A common feature of many apps is that they allow the creation of user accounts. To do this, a few things need to happen:

- [New User Sign Up](#new-user-sign-up)
- [Logging In](#logging-in)
- [Logging Out](#logging-out)
- [Gated Pages](#gated-pages)

Before we address each of these actions, it's worth nothing *how* the app will know whether a user is logged in. To keep track of whether a user is logged in, we'll use the `session` variable that is part of any browser. The `session` variable is stored in the browser memory, and we can access it using a function built into Flask: `session`.

To bring in the `session` function from Flask, we'll update the import statement in our app. 

```python
from flask import render_template, request, redirect, session, url_for
```

> Note, we're also adding the `url_for` function which will be used to simplify how a user is passed from one page to another.

To be able to use the `session` functionality, we need to store a secret key that will be used to sign each session. The `secret_key` will be a property of the app itself:

```python
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
```

Now that a session can be created, we can assign a value to a property of the `session` variable in order to store that value:

```python
session['username'] = "My Name"
```

To access that variable, we can call the `session` variable and the property name:

```python
print(session['username'])
# My Name
```

We can also write logic statements to capture whether the `session` variable contains a particular property:

```python
if 'username' in session:
	# some code here
```

### New User Sign Up

In order for a new user to sign up, a few things need to happen:

1. We need to show the user the `signup.html` template (via a `GET` request).
2. Once they've filled out the form on that template, we need to check the database to see if we can find that user (via a `POST` request and `.find_one()`.
3. If we can find that user, then they already exist, so a new user cannot sign up with the same name.
4. If we cannot find that user, then that user does not yet exist, so we can create it.
5. To create the new user in the database, we can `.insert()` the `username` and `password` we get from the form.
6. We then start a new session with the `username` from the form.
7. Lastly, we redirect the user to the homepage.

```python
@app.route('/signup', methods=['POST', 'GET'])

def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists! Try logging in.'

    return render_template('signup.html')
```

And here's an HTML snippet that corresponds to the route above:

```html
<form action="/signup" method="POST">
    <label for="name">Name</label>
    <input type="text" name="username">
    <label for="password">Password</label>
    <input type="password" name="password">
    <input type="submit" value="Sign Up">
</form>
```

> Since we don't (yet) have a way for a user to log out, you can clear the session cookie using your browser's Developer Tools.

- Consider where you might want to show the user they are logged in.
- Consider what else a user would expect to see when signing up.
- Also consider what a user should do if they already have an account? (see below) 

### Logging In

Now that a user has signed up, they'll need a way to sign back in in the future. To account for this, we may want a new `login` route.

This route should consult the MongoDB and find the user who is trying to log in. It will then compare the password submitted by the user to the password stored in the database. If the passwords are the same, a new session will be started for the user and the user will be routed to the index page. Otherwise, they will receive a message indicating an invalid username/password combination.

```python
@app.route('/login', methods=['POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'
```

And here's an HTML snippet that corresponds to the route above. Notice how it includes a link to the `signup` route in case a user doesn't yet have an account.

```html
<h2>Log in</h2>
<div>
    <form action="/login" method="POST">
        <label for="name">Name</label>
        <input type="text" name="username">
        <label for="password">Password</label>
        <input type="password" name="password">
        <input type="submit" value="Log In">
    </form>
    <p>No account? <a href="/signup">Sign up.</a></p>
</div>
```

- Consider where you might want to include a form to "Log In"
- Consider how you would only show the login form to a user who isn't logged in (e.g. doesn't yet have a session started).

### Logging Out

Once a user is logged in, they may also want to log out. Logging out is as simple as clearing the stored session data and redirecting to another page.

```python
@app.route('/logout')

def logout():
    session.clear()
    return redirect('/')
```

- Consider where in your HTML templates you may want to include a link to "Log Out".

### Gated Pages

Sometimes you may have pages that you don't want everyone to be able to see, e.g profile/account information or a list of the events/items a user has submitted. Maybe you only want to show information when a user is logged in and it is that same user's information you want to show.

Using what we already know, think about how to write a new route that shows a template populated by data from the database filtered by the name stored in `session['username']`. An example solution is shown below.

We can add a new route:

```python
@app.route('/events/myevents')

def myevents():
    collection = mongo.db.events
    username = session['username']
    events = collection.find({'user' : username})

    return render_template('my_events.html', events = events)
```

And also a new snippet for an HTML template:

```html
<div>
    <ul>
        {% for event in events %}
            <li><a href="/events/{{event._id}}">{{ event.event }} - {{ event.date }}</a>(Posted by {{ event.user }})</li>
        {% endfor %}
    </ul>
</div>
```

- Consider where in your HTML template(s) you might want to include a link to "My Events"
- Think about how you might only show the "My Events" link to a user who is logged in.

## Reach Extensions

Now that you have a sense of the basics, there are loads of directions you and students may want to take the framework you've built so far. Here, we touch on three possible reach extensions:

- [Date Formatting](#date-formatting)
- [Environment Variables](#environment-variables)
- [Password Hashing](#password-hashing)

### Date Formatting

> Resist the temptation to go too deep into "What is a date? What is a time?" your first time through.

Formatting dates in python is done using the `datetime` module. `datetime` is already built into Python 3, but you may want to ensure it's installed using:

```bash
pip install datetime
```

Then import the `datetime` functions into your app:

```python
from datetime import datetime
```

There are two functions you may find useful for reformatting dates: `strptime` and `strftime`.

#### `strptime`

`strptime` is short for "string parse time" and takes a string as an argument and returns a DateTime Object. It does this according to a format that you define by using variables that represent different parts of a date/time: e.g. `%d` is the day of the month as a zero-padded decimal number, and `%Y` is the year with century as a decimal number. The [documentation](https://docs.python.org/3.7/library/datetime.html#strftime-and-strptime-behavior) has the full list of options.

So to convert the string `04-10-19` into a DateTime Object, we need to recognize that it's in the format of `MM-DD-YY` which would be represented as `%m-%d-%y`. Notice how the dashes as used in the representation just like they're used in the string. `strptime` takes the string and the representation as arguments to output a DateTime Object:

```python
date = "04-10-19"
dateObj = datetime.strptime(date, '%m-%d-%y')
```

#### `strftime`

To represent the DateTime Object in a new way, we can use `strftime` which stands for "string format time". It takes a single argument: the new DateTime format:

```python
dateStr = dateObj.strftime('%a, %b %d, %Y')
print(dateStr)
# Wed, Apr 10, 2019
```

> `%a` is the weekday as locale’s abbreviated name (Sun, Mon, etc.); `%b` is the month as locale’s abbreviated name (Jan, Feb, etc.); `%d` is the day of the month as a zero-padded decimal number (01, 02, etc.); and `%Y` is the year with century as a decimal number (2000, 2001, etc.).

#### Extensions

- `datetime` also includes support for parsing and formatting times, timezones, and various localization/languages.
- Try using `datetime` to display 24-hour time (e.g. 18:00) instead of 12-hour time (e.g. 6:00pm).

#### Resources

- [Python 3.7 datetime Documentation](https://docs.python.org/3.7/library/datetime.html)

### Environment Variables

> Resist the temptation to go too deep into "What is an environment variable?" your first time through.

Environment variables are used to protect sensitive usernames and passwords. By hiding credentials, it is much more difficult for anyone to gain unauthorized access to sensitive data.

Credentials are listed in a file called `.env`, and that file is then named in a repository's `.gitignore` file. By including `.env` in the `.gitignore`, the `.env` file will not be uploaded and shared to github. Instead, we will be able to use the credentials when we develop in our local environment, and when we push to the cloud we'll need to make sure to securely store the credentials in the platform itself.

To use environment variables, we first need to install the `python-dotenv` module (and the `os` module) using the Terminal:

```bash
pip install os # if you haven't already
pip install python-dotenv
```

And we need to include the `load_dotenv` function in our app:

```python
import os # if you haven't already
from dotenv import load_dotenv
```

Next, we create a new file called `.env` and list the credentials we want to store there:

```
MONGO_USERNAME="admin"
MONGO_PASSWORD="password"
```

Back in our app, the `load_dotenv` function loads the variables from the `.env` file so we can use variable names in place of the credentials themselves.

```python
# first load environment variables in .env
load_dotenv()

# then store environment variables with new names
USER = os.getenv("MONGO_USERNAME")
PASS = os.getenv("MONGO_PASSWORD")
```

Now whenever we want to use the credentials, we can just use the name of the variable instead of the credential itself.

Recall the code we use to connect to our MongoDB:

```python
app.config['MONGO_URI'] = 'mongodb+srv://admin:password@server-kxrbn.mongodb.net/test?retryWrites=true'
```

Using environment variables, it is now secured:

```python
app.config['MONGO_URI'] = 'mongodb+srv://'+USER+':'+PASS+'@server-kxrbn.mongodb.net/test?retryWrites=true'
```

So if someone were to see our code (on github or using other tools), they wouldn't be able to see our username and password.

#### Environment Variables in Goorm

When you are building in Goorm, ...

#### Environment Variables in Heroku

When you deploy your app to heroku, you are not deploying the `.env` file. Instead, heroku has it's own secure storage location for listing environment variables.

For your deployed app to function on heroku, you'll need to access...

#### Extensions

#### Resources

- [python-dotenv on GitHub](https://github.com/theskumar/python-dotenv)

### Password Hashing

> Resist the temptation to go too deep into "What is a hash? What's the best way to store passwords?" your first time through.

So far, we've asked users to come up with a username and a password, however we're storing that password in plaintext in our database. Storing passwords in plaintext is **highly insecure** because if someone who isn't authorized gains access to the database, they would have access to all users' passwords.

To store passwords more securely, we can hash the password, and store that value instead. Then when a user tries to log into the app, we'll compare the hash of the password they provide to the hash of the password that is stored in the database. If they two match, we grant access; if they don't, then we deny access.

> The benefit of using a hash is that it cannot (practically) be unhashed. Unlike encryption/decryption, the hash is a one-way function, so even if someone gets a hash, they cannot work backwards to figure out the original password input.

To hash passwords, we'll use the `bcrypt` module:

```bash
pip install bcrypt
```

And we need to import `bcrypt` into our app:

```python
import bcrypt
```

We can now modify the `signup` route to generate and store the hash of the password provided by the user:

```python
@app.route('/signup', methods=['POST', 'GET'])

def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : str(hashpass, 'utf-8')})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists! Try logging in.'

    return render_template('signup.html')
```

And we can modify the `login` route to check that the hash of the password provided matches the stored password hash for a given user:

```python
@app.route('/login', methods=['POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw((request.form['password']).encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'
```

Sign up with a new user to see how `bcrypt.hashpw()` generates and stores a hashed password instead of the plaintext password.

#### Extensions

- Explore other hashing algorithms, e.g. SHA-256
- Explore how "salts" are used to complicate stored password hashes

#### Resources

- [The bcrypt Project](https://pypi.org/project/bcrypt/)

