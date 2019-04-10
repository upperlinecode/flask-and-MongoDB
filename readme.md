# Build a Community Board with Flask and MongoDB (with a little help from PyMongo)

1. Intro
2. Initial Setup
	a. [Connect to MongoDB](#connect-to-mongo)
	b. [Push to MongoDB](#push-to-mongo)
	c. [Queries of MongoDB](#queries-of-mongodb)
	d. [Sorting Results](#sorting-results)
	e. [Push to Heroku](#push-to-heroku)
3. Extensions
	a. [Individual Post Pages](#individual-post-pages)
	a. [User Accounts](#user-accounts)
	a. [New User Sign Up](#new-user-sign-up)
	a. [Logging In](#logging-in)
	a. [Logging Out](#logging-out)
	a. [Gated Pages](#gated-pages)
4. Reach Extensions
	a. [Date Formatting](#date-formatting)
	a. [Environment Variables](#environment-variables)
	a. [Password Hashing](#password-hashing)

## Intro

Now that you and your students have built an app using Flask, you might have recognized a need to store and retrieve data. For this, we're going to use a database called MongoDB.

If you're just looking to run the demo code, this is a list of the packages you'll want to make sure you've installed. 

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

To view a finished app, rename `routes-complete.py` to `routes.py` and then execute `flask run` in the Terminal as before.

Read on for the steps and lessons to build that completed Flask + MongoDB app.

## Initial Setup



### Connect to MongoDB

### Push to MongoDB

### Queries of MongoDB

### Sorting Results

### Push to Heroku

- Test this from ide.goorm.io

## Extensions

### Individual Post Pages

### User Accounts

### New User Sign Up

### Logging In

### Logging Out

### Gated Pages

## Reach Extensions

Now that you have a sense of the basics, there are loads of directions you and students may want to take the framework you've built so far. Here, we touch on three possible reach extensions:

- Formatting Dates
- Environment Variables
- Password Hashing

### Date Formatting

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

So to convert the string `04-10-19` into a DateTime Object, we need to recognize that it's in the format of `MM-DD-YY` which would be represented as `%m-%d-%y`. Notice how the dashes as used in the representation just like they're used in the string. `strptime` takes the string and the representation as arguments to output the DateTime Object:

```python
date = 04-10-19
DateObj = datetime.strptime(date, '%m-%d-%y')
```

To represent the DateTime Object in a new way, we can use `strftime` which stands for "string format time". It takes a single argument: the new DateTime format:

```python
dateStr = dateObj.strftime('%a, %b %d, %Y')
print(dateStr)
# Wed, Apr 10, 2019
```

> Note: `%a` is the weekday as locale’s abbreviated name (Sun, Mon, etc.); `%b` is the month as locale’s abbreviated name (Jan, Feb, etc.); `%d` is the day of the month as a zero-padded decimal number (01, 02, etc.); and `%Y` is the year with century as a decimal number (2000, 2001, etc.).

#### Extension

- `datetime` also includes support for parsing and formatting times, timezones, and various localization. Try using `datetime` to display 24-hour time (e.g. 18:00) instead of 12-hour time (e.g. 6:00pm).

#### Resources

- [Python 3.7 datetime Documentation](https://docs.python.org/3.7/library/datetime.html)

### Environment Variables

#### Environment Variables in Goorm

#### Environment Variables in Heroku

### Password Hashing


