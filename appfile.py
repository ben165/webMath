#!/usr/bin/python3

# Python stuff
import io

# Flask stuff
from flask import Flask, request, session

# Math Stuff
import matplotlib.pyplot as plt
import numpy as np

# My stuff
import helper as hp


app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'DFkCwsJVaWc1YpP+SA5hSYLpRP0='


def sessionValid():
	try:
		if session['username'] and ('username' in session):
			return True
		return False
	except:
		False


@app.route("/")
def index():


	out = []
	out.append("<h2>Welcome</h2>")
	out.append("<p>")

	if not sessionValid():
		out.append('<h3>Login</h3>\n')
		out.append('<form action="doLogin" method="post">\n')
		out.append('<p>Username:<br />\n')
  		
		out.append('<select id="username" name="username">\n')
		out.append('<option value="jakob">jakob</option>\n')
		out.append('<option value="benjamin">benjamin</option>\n')
		out.append('</select></p>\n')
		
		out.append('<p>Password:<br />\n')
		out.append('<input type="password" name="password"></p>\n')
		out.append('<input type="submit" value="Submit">\n')
		out.append('</form>')
		out.append("</p>")
		return hp.HEAD + "".join(out) + hp.TAIL

	out.append("Logged in as " + session["username"])
	out.append(' (<a href="doLogout">Logout</a>)\n')
	out.append('</p>\n')

	out.append('<h2>Options</h2>\n')
	out.append('<ul>\n')
	out.append('<li><a href="taylor">Taylor Beispiel</a></li>\n')
	out.append('<li>3D Plot Beispiel (not implemented yet)</li>\n')
	out.append('</ul>\n')

	return hp.HEAD + "".join(out) + hp.TAIL



@app.route('/doLogin', methods=['POST'])
def	login():
	out = []

	if request.method != 'POST':
		return	'method	wrong'

	password = request.form['password']
	username = request.form['username']
	hashed = hp.createHash(password, username)
	print(hashed)

	if ( hashed == hp.getPw(username)):
		session["username"] = username
		out.append('<p>Login successful. Welcome back <b>' +username+ '</b>.</p>\n')
		out.append('<p>Back to <a href="/">main</a>.</p>\n')
	else:
		out.append('Login failed (Wrong password?). <br /><a href="/">Go back</a>.\n')

	return hp.HEAD + "".join(out) + hp.TAIL


@app.route('/doLogout')
def doLogout():
	session["username"] = None
	return hp.HEAD + 'Logout complete. Go <a href="/">back</a>.' + hp.TAIL



@app.route("/taylor")
def plot():

	if not sessionValid():
		return hp.HEAD + 'Not logged in. Go <a href="/">back</a>' + hp.TAIL

	out = []

	out.append('<p><a href="/">Back</a></p>\n')

	out.append('<h2>Taylor example</h2>\n')

	out.append('Taylor Approximations of <b>sin(x)</b> as position x=0\n')

	out.append('<form action="taylor" method="get">\n')  	
	out.append('<select id="order" name="order">\n')
	for i in range(1,11):	
		out.append('<option value="'+str(i)+'">'+str(i)+'</option>\n')
	out.append('</select></p>\n')
	
	out.append('<input type="submit" value="Submit">\n')
	out.append('</form>\n\n')


	try:
		orderNr = int(request.args.get('order', ''))
	except:
		return hp.HEAD + ''.join(out) + hp.TAIL

	out.append("<hr>\n")
	out.append("Order choosen: " + str(orderNr))

	# Plot range
	xmin = -4*np.pi
	xmax = 4*np.pi

	plt.figure( figsize=(8,6) ) #figsize=(19.20,10.80)
	x = np.linspace(-4*np.pi, 4*np.pi, 200)
	yTaylor = np.zeros(len(x))
	ySin = np.sin(x)

	# Approximation
	sign = -1
	for i in range(0, orderNr+1):
		if (i % 2 == 0):
			continue
		else:
			sign *= -1
			yTaylor += sign * x**i/np.math.factorial(i)

	plt.plot(x, ySin, 'b', x, yTaylor, 'r')
	plt.axis((xmin, xmax, -4, 4))
	plt.grid(True)

	#plt.show()
	plt.savefig("plots/" + session['username'] + '.png')

	out.append('<img src="plot/'+session['username']+'.png" alt="Sin Taylor">\n')

	return hp.HEAD + ''.join(out) + hp.TAIL



@app.route('/plot/<picname>')
def plots(picname):
	f = open("plots/" + picname, 'rb')
	content = f.read()
	f.close()

	#print(type(content))

	return content, {'Content-Type': 'image/png'}
	#return hp.HEAD + "test" + hp.TAIL


@app.route("/test")
def test():
	x = """
	{
		"a": 1,
		"b": 2
	}
	"""
	return x, {'Content-Type': 'application/json'}




if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8080, debug=True)

