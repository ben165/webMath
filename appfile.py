#!/usr/bin/python3

# Python stuff
import io

# Flask stuff
from flask import Flask, request, session, render_template

# Math Stuff
import matplotlib
import matplotlib.pyplot as plt

# Very important for thread safety
matplotlib.use('agg')

import numpy
import sympy as sp
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr

# My stuff
import helper as hp

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'DFkCwsJVaWc1YpP+SA5hSYLpRP0='


@app.route("/")
def index():
    return render_template('login.html', session=session, valid=hp.sessionValid(session))


@app.route('/doLogin', methods=['POST'])
def login():
    out = []

    if request.method != 'POST':
        return 'method wrong'

    # Get form data (POST)
    password = request.form['password']
    username = request.form['username']

    # Check data for setting session cookie
    if (hp.checkLogin(password, username)):
        session["username"] = username
        return render_template('status.html', status="Login successful.")
    else:
        return render_template('status.html', status="Login failed.")


@app.route('/doLogout')
def doLogout():
    session.pop('username', None)
    return render_template('status.html', status="Logout successful.")


@app.route("/taylor")
def taylor():
    if not hp.sessionValid(session):
        return render_template('status.html', status="Not logged in.")

    try:
        n = int(request.args.get('order', ''))

        # Check if int and convert it into str
        x00 = str(int(request.args.get('x0', '')))

        # Get formula
        expression = request.args.get('expression', '')

        # Input protection
        if (n > 15 or n < 1):
            n = 5
    except:
        return render_template('taylor.html', picture="", x0="", exp="", exprPretty="", formula="")

    rangeX = 4  # xrange = [-4, 4]

    expr = sp.parse_expr(expression)
    x0 = sp.parse_expr(x00)
    x = sp.symbols('x')

    # Generiere "leeres" Sympy object
    temp = sp.sqrt(0)

    for i in range(0, n + 1):
        e1 = sp.diff(expr, "x", i)
        temp += e1.subs(x, x0) / sp.factorial(i) * (x - x0) ** i

    asciiForm = sp.pretty(temp)

    f0 = sp.lambdify(x, expr, "numpy")
    f1 = sp.lambdify(x, temp, "numpy")

    xValues = numpy.linspace(float(x00) - rangeX, float(x00) + rangeX, 100)
    yValues0 = f0(xValues)
    yValues1 = f1(xValues)

    plt.clf()
    plt.plot(xValues, yValues0, 'b', xValues, yValues1, 'r')
    plt.axis((float(x00) - rangeX, float(x00) + rangeX, -4, 4))
    plt.grid(True)

    # JSON response
    try:
        if request.args.get('json', '') == "1":
            json = {
                "x": list(xValues),
                "y0": list(yValues0),
                "y1": list(yValues1)
            }
            return json
    except:
        pass

    # Normal response (pure backend)
    address = 'plots/' + session['username'] + '.png'
    plt.savefig(address)

    return render_template('taylor.html', picture=address, x0=x0, expr=expr, exprPretty=sp.pretty(expr),
                           formula=asciiForm)


@app.route("/taylorJS")
def taylorJS():
    if not hp.sessionValid(session):
        return render_template('status.html', status="Not logged in.")

    return render_template('jsFrontend.html')


@app.route('/plot3d')
def plot3d():
    if not hp.sessionValid(session):
        return render_template('status.html', status="Not logged in.")
    expression = ""
    try:
        expression = request.args.get('expression', '')
        expr = parse_expr(expression)
        x, y = symbols('x y')
        graph = sp.plotting.plot3d(expr, (x, -5, 5), (y, -5, 5), show=False, size=(10, 10))
        graph.save("plots/" + session['username'] + '.png')
        return render_template('plot3d.html', expression=expression, image_scr="plots/" + session['username'] + ".png")
    except:
        return render_template('plot3d.html', expression=expression, image_scr="")


@app.route('/plots/<picname>')
def plots(picname):
    f = open("plots/" + picname, 'rb')
    content = f.read()
    f.close()

    return content, {'Content-Type': 'image/png'}


@app.route("/jsonTest")
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
