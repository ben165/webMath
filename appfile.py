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
from sympy.printing.mathml import mathml
from sympy.plotting.plot import plot3d

# My stuff
import helper as hp

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'DFkCwsJVaWc1YpP+SA5hSYLpRP0='


@app.route("/")
def index():
    out = []
    out.append("<h2>Welcome</h2>")
    out.append("<p>")

    if not hp.sessionValid(session):
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
    out.append('<li><a href="taylor">Taylor Beispiel Backend</a></li>\n')
    out.append('<li><a href="taylorJS">Taylor Beispiel Frontend + Backend</a></li>\n')
    out.append('<li><a href="plot3d">3D Plot</a></li>\n')
    out.append('</ul>\n')

    return hp.HEAD + "".join(out) + hp.TAIL


@app.route('/doLogin', methods=['POST'])
def login():
    out = []

    if request.method != 'POST':
        return 'method	wrong'

    password = request.form['password']
    username = request.form['username']
    hashed = hp.createHash(password, username)
    print(hashed)

    if (hashed == hp.getPw(username)):
        session["username"] = username
        out.append('<p>Login successful. Welcome back <b>' + username + '</b>.</p>\n')
        out.append('<p>Back to <a href="/">main</a>.</p>\n')
    else:
        out.append('Login failed (Wrong password?). <br /><a href="/">Go back</a>.\n')

    return hp.HEAD + "".join(out) + hp.TAIL


@app.route('/doLogout')
def doLogout():
    session.pop('username', None)
    return hp.HEAD + 'Logout complete. Go <a href="/">back</a>.' + hp.TAIL


@app.route("/taylor")
def taylor():
    if not hp.sessionValid(session):
        return hp.HEAD + 'Not logged in. Go <a href="/">back</a>' + hp.TAIL

    out = []

    out.append('<p><a href="/">Back</a></p>\n')

    out.append('<h2>Taylor example 2</h2>\n')

    out.append('Taylor Approximations\n')

    out.append('<form action="taylor" method="get">\n')
    out.append('<select id="order" name="order">\n')
    for i in range(1, 16):
        out.append('<option value="' + str(i) + '">' + str(i) + '</option>\n')
    out.append('</select></p>\n')

    out.append('<p>Expression: \n')
    out.append('<input type="text" name="expression"></p>')

    out.append('<p>x0 position: \n')
    out.append('<input type="text" name="x0"></p>')

    out.append('<input type="submit" value="Submit">\n')
    out.append('</form>\n\n')

    try:
        n = int(request.args.get('order', ''))
        
        #Check if int
        int(request.args.get('x0', ''))
        
        # But I need a string later
        x00 = request.args.get('x0', '')

        expression = request.args.get('expression', '')

        # DDOS protection
        if n > 15:
            n = 15
    except:
        return hp.HEAD + ''.join(out) + hp.TAIL

    out.append("<hr>\n")
    out.append("<p>Order choosen: " + str(n) + "</p>\n")
    
    #expression = "sin(x)*cos(x)"

    rangeX = 4 # willkuerlich festgelegt

    expr = sp.parse_expr(expression)
    #x00 = "4"
    x0 = sp.parse_expr(x00)

    x = sp.symbols('x')

    # Generiere "leeres" Sympy object (geht das besser?)
    temp = sp.sqrt(0)

    print("n: ", n)
    for i in range(0, n+1):
        e1 = sp.diff(expr, "x", i)
        temp += e1.subs(x, x0) / sp.factorial(i) * (x-x0)**i

    asciiForm = sp.pretty(temp)
    
    print("HHHHHHHHHHHHHHHHH")
    sp.pprint(temp)

    #expr = expr.subs(x, x-x0)

    f0 = sp.lambdify(x, expr, "numpy")
    f1 = sp.lambdify(x, temp, "numpy")

    xValues = numpy.linspace(float(x00)-rangeX, float(x00)+rangeX, 100)
    print("x:  ", xValues)
    yValues0 = f0(xValues)
    print("y0: ", yValues0)
    yValues1 = f1(xValues)
    print("y1: ", yValues1)

    plt.clf()
    plt.plot(xValues, yValues0, 'b', xValues, yValues1, 'r')
    plt.axis((float(x00)-rangeX, float(x00)+rangeX, -4, 4))  # y range durch max Werte der Funktion ersetzen...
    plt.grid(True)
    
    #plt.show()

    plt.savefig("plots/" + session['username'] + '.png')

    out.append('<img src="plot/' + session['username'] + '.png" alt="Sin">\n')

    out.append('<h2>Formel</h2>\n')
    out.append('<pre><br>' + asciiForm + '<br></pre>\n')


    # JSON object return
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


    # Standard return
    return hp.HEAD + ''.join(out) + hp.TAIL




@app.route("/taylorJS")
def taylorJS():
    return render_template('jsFrontend.html')


@app.route('/plot3d')
def plot3d():
    if not hp.sessionValid(session):
        return hp.HEAD + 'Not logged in. Go <a href="/">back</a>' + hp.TAIL

    out = []
    out.append('<p><a href="/">Back</a></p>\n')
    out.append('<h2>3D plot</h2>\n')
    out.append('Enter sympy expression in x and y (example: sin(x)*(x**2+y**2)):\n')

    out.append('<form action="plot3d" method="get">\n')
    out.append('<input type="text" id="expression" name="expression"></p>')
    out.append('<input type="submit" value="Submit">\n')
    out.append('</form>\n\n')

    try:
        expression = request.args.get('expression', '')
        expr = parse_expr(expression)
        s = mathml(expr, printer="presentation")
        out.append('<math>' + s + '</math>')
    except:
        out.append('<p>Invalid sympy expression</p>')
        return hp.HEAD + ''.join(out) + hp.TAIL
    x, y = symbols('x y')
    graph = sp.plotting.plot3d(expr, (x, -5, 5), (y, -5, 5), show=False, size=(10, 10))
    graph.save("plots/" + session['username'] + '.png')
    out.append('<img src="plot/' + session['username'] + '.png">\n')
    return hp.HEAD + ''.join(out) + hp.TAIL


@app.route('/plot/<picname>')
def plots(picname):
    f = open("plots/" + picname, 'rb')
    content = f.read()
    f.close()

    # print(type(content))

    return content, {'Content-Type': 'image/png'}


# return hp.HEAD + "test" + hp.TAIL


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
