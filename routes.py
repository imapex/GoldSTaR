from flask import Flask, request, render_template
import jinja2
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		apic_username = request.form['apic_username']
		apic_password = request.form['apic_password']
		pi_username = request.form['pi_username']
		pi_password = request.form['pi_password']

		if apic_username:
			from app import getTicket, getDevicesFromAPICEM
			theTicket=getTicket(apic_username,apic_password)
			getDevicesFromAPICEM(theTicket)
		elif pi_username:
			from app import getDevicesFromPrime
			getDevicesFromPrime(pi_username,pi_password)

		from app import runningVersions
		return render_template('inventory.html', inventory = runningVersions)
	else:
		return "<h2> Invalid Request </h2>"

@app.route('/inventory')
def inventory():
	from app import runningVersions
	return render_template('inventory.html', inventory = runningVersions)

@app.route('/software')
def software():
	return render_template('software.html')

@app.route('/psirt')
def psirt():
	return render_template('psirt.html')

