from flask import Flask, request, render_template
import jinja2
from app import app

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/inventory')
def inventory():
	return render_template('inventory.html')

@app.route('/software')
def software():
	return render_template('software.html')

@app.route('/psirt')
def psirt():
	return render_template('psirt.html')

