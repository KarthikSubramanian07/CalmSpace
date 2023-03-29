from flask import Flask, flash, request, redirect, render_template, url_for 
import csv
import RPi.GPIO as GPIO
import pywemo
import sys
from datetime import datetime
import time
import csv
import logging


app = Flask(__name__)
app.secret_key = b'***]/'
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('this will show in the log')

@app.route('/')
def index():
    csv_reader=None
    mailval='h***@gmail.com'
    
    with open('/home/pi/calmspace/email.txt', "r") as file:
        for line in file.readlines():
            mailval = line.rstrip()
            app.logger.debug('on load, mail:',mailval)
    
    with open('/home/pi/calmspace/config.csv', encoding="utf8") as f:
        csv_reader = csv.reader(f)
        return render_template('index.html', data=csv_reader, mail=mailval)

@app.route('/clear')
def clear():
    app.logger.debug('on clear')
    f = open('/home/pi/calmspace/config.csv', 'w+')
    f.close()
    return render_template('index.html')

@app.route('/discover')
def discover():
    app.logger.debug('on discover')
    mydevices = pywemo.discover_devices()
    app.logger.debug(mydevices)
    f = open('/home/pi/calmspace/config.csv', 'w')
    writer = csv.writer(f)
    app.logger.debug('writer created')
    for device in mydevices:
        row = [device,0]
        writer.writerow(row)
        app.logger.debug('written row:',row)
    f.close()
    app.logger.debug('file closed')
    return redirect(url_for('index'))

@app.route('/save/', methods=('GET', 'POST'))
def save():
    rows=[]
    app.logger.debug('on save1')
    chkdevices=request.form.getlist('chkdevice')
    app.logger.debug('chkdevices:',chkdevices)
    with open('/home/pi/calmspace/config.csv', encoding="utf8") as f:
        csv_reader = csv.reader(f)
    #f = open('/home/pi/calmspace/config.csv', 'w+')
        for row in csv_reader:
            if(row[0] in chkdevices):
                app.logger.info("wow, I exist")
                row[1]=1
            else:
                row[1]=0
            rows.append(row)
    
    app.logger.info('hello here1')
    app.logger.info("rows")
    app.logger.info(rows)
    app.logger.debug('hello here2')

    f = open('/home/pi/calmspace/config.csv', 'w+')
    writer = csv.writer(f)
    app.logger.debug('writer created')
    for row in rows:
        writer.writerow(row)
        app.logger.debug('written row:',row)
    f.close()

    
    email = request.form['email']
    with open("/home/pi/calmspace/email.txt", "w+") as fo:
        fo.write(email)
        app.logger.debug('email file created, writing:',email)
    
    
    #f.close()
    return redirect(url_for('index'))
    #return render_template('index.html', data=csv_reader)

@app.route('/vmd_timestamp')
def vmd_timestamp():
    app.logger.debug('on discover')
    mydevices = pywemo.discover_devices()
    app.logger.debug(mydevices)
    f = open('/home/pi/calmspace/config.csv', 'w')
    writer = csv.writer(f)
    app.logger.debug('writer created')
    for device in mydevices:
        row = [device]
        writer.writerow(row)
        app.logger.debug('written row:',row)
    f.close()
    app.logger.debug('file closed')
    with open('/home/pi/calmspace/config.csv', encoding="utf8") as f:
        csv_reader = csv.reader(f)
        return render_template('index.html', data=csv_reader)
     
#These functions will run when POST method is used.
@app.route('/', methods = ["POST"] )
def plot_png():
    #gathering file from form
    uploaded_file = request.files['txt_file']
    
    #making sure its not empty
    if uploaded_file.filename != '':
        #reading the file
        text = uploaded_file.filename
        app.logger.debug('this is a DEBUG message')
        # open the file in the write mode
        f = open('/home/pi/calmspace/config.csv', 'w')

        # create the csv writer
        writer = csv.writer(f)
        app.logger.debug('writer created')

        # write a row to the csv file
        row1 = ["My Light","10.0.0.2"]
        writer.writerow(row1)
        app.logger.debug('written row:',row1)

        # close the file
        f.close()
        app.logger.debug('file closed')

        return render_template('success.html',
                        PageTitle = "Success page")

     
    
    else:
        return render_template('index.html',
                        PageTitle = "Landing page")
      #This just reloads the page if no file is selected and the user tries to POST. 


if __name__ == '__main__':
    app.run(debug = True)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)    