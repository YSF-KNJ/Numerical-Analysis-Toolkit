from flask import Flask, render_template, request, send_file
from sympy import *
import xlsxwriter


app = Flask(__name__)


# root 
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

# point fixe
@app.route('/point_fixe', methods=['GET', 'POST'])
def point_fixe():
    x = symbols('x')
    if request.method == 'POST':
        nombre_iteration = int(request.form['nombre_iteration'])
        x0 = float(request.form['x0'])
        gx = str(request.form['gx'])
        filename = str(gx)+"-"+str(x0)+"-"+str(nombre_iteration)+"-point-fixe"+".xlsx"
        file = open(filename,"w+",encoding = 'utf-8') 
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        format1 = workbook.add_format({'bold': True, 'font_color': 'red','align': 'center'})
        format2 = workbook.add_format({'align': 'center'})
        worksheet.write("A1","N",format1)
        worksheet.write("B1","X",format1)
        worksheet.write("C1","F(X)",format1)
        g = sympify(gx)
        xn = x0
        c = 1
        for i in range(nombre_iteration):
            c+=1
            t = float(g.subs(x, xn))
            worksheet.write(f"A{c}",i+1,format2)
            worksheet.write(f"B{c}",xn,format2)
            worksheet.write(f"C{c}",t,format2)
            if (t == xn):break
            else: xn = t
        worksheet.write(f"C{c}",t,format1)
        workbook.close()
        file.close()
        return render_template('result.html', filename = filename , result = t, heading = "Résultat par méthode de point fixe", aside = "X")
    return render_template('point_fixe.html')

# newton
@app.route('/newton', methods=['GET', 'POST'])
def newton():
    x = symbols('x')
    def derivee(f):
        df = Derivative(f, x)
        return df.doit()
    if request.method == 'POST':
        nombre_iteration = int(request.form['nombre_iteration'])
        x0 = float(request.form['x0'])
        fx = str(request.form['fx'])
        filename = str(fx)+"-"+str(x0)+"-"+str(nombre_iteration)+"-newton"+".xlsx"
        file = open(filename,"w+",encoding = 'utf-8') 
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        format1 = workbook.add_format({'bold': True, 'font_color': 'red','align': 'center'})
        format2 = workbook.add_format({'align': 'center'})
        worksheet.write("A1","N",format1)
        worksheet.write("B1","X",format1)
        worksheet.write("C1","F(X)",format1)
        f = sympify(fx)
        df = derivee(f)
        xn = x0
        c = 1
        for i in range(nombre_iteration):
            dfxn = float(df.subs(x, xn))
            if (dfxn != 0 ):
                c+=1
                fxn = float(f.subs(x, xn))
                t = xn - (fxn/dfxn)
                worksheet.write(f"A{c}",i+1,format2)
                worksheet.write(f"B{c}",xn,format2)
                worksheet.write(f"C{c}",t,format2)
                if (t == xn):break
                else: xn = t
        worksheet.write(f"C{c}",t,format1)
        workbook.close()
        file.close()
        return render_template('result.html', filename = filename , result = t, aside = "X", heading = "Résultat par méthode de newton")
    return render_template('newton.html')

# polynome_lagrange
@app.route('/polynome_lagrange', methods=['GET', 'POST'])
def polynome_lagrange():
    x = symbols('x')
    if request.method == 'POST':
        x_values_input = request.form['x_values_input']
        fx_values_input = request.form['fx_values_input']
        x_values_input_sp = x_values_input.split(',')
        fx_values_input_sp = fx_values_input.split(',')
        x_values,fx_values = [],[]
        for i in x_values_input_sp:
            x_values.append(int(i))
        for j in fx_values_input_sp:
            fx_values.append(int(j))

        n = int(len(x_values))
        filename = "polynome_lagrange"+".txt"
        file = open(filename,"w+",encoding = 'utf-8')
        file.write(f"n = {n}\n\n")
        for i in range(n):
            file.write(f"f({x_values[i]}) = {fx_values[i]}\n")
        file.write("\n")
        def alpha(n,j,x_values):
            bast,makam = 1,1
            for i in range(n):
                if(i == j):continue
                bast *= x - x_values[i]
                makam *= x_values[j] - x_values[i]
                lf = simplify(bast/makam)
                rtw = str(lf).replace('**','^')
            file.write(f"L(x{j}) = {rtw}\n")
            return bast/makam
        for k in range(n):
            if (k==0):p = alpha(n,k,x_values)*fx_values[k]
            else:p += alpha(n,k,x_values)*fx_values[k]
        p = simplify(p)
        kp = str(p)
        ptw = kp.replace('**','^')
        file.write(f"\nP{n}(x) = {ptw}\n")
        file.close()
        return render_template('result.html', filename = filename , result = f"{ptw}\n", heading = "La Polynôme de Lagrange ", aside = f"P{n}(x)")
    return render_template('polynome_lagrange.html')

# trapeze
@app.route('/trapeze', methods=['GET', 'POST'])
def trapeze():
    x = symbols('x')
    if request.method == 'POST':
        a = float(request.form['a'])
        b = float(request.form['b'])
        n = int(request.form['n'])
        f = request.form['function']
        filename = f+'_'+str(a)+'-'+str(b)+'_'+str(n)+'.txt'
        f = sympify(f)
        h = (b - a) / n
        somme = 0
        for i in range(1, n):
            somme += f.subs(x,a + i * h)
        resultat = h / 2 * (f.subs(x,a) + 2 * somme + f.subs(x,b))
        with open(filename,'w+') as file:
            file.write(str(resultat))
            
        return render_template('result.html', filename = filename, result = resultat,heading = "Résultat approximative par la méthode des trapèzes", aside = "Résultat")
    return render_template('trapeze.html')

# rectangle
@app.route('/rectangle', methods=['GET', 'POST'])
def rectangle():
    x = symbols('x')
    if request.method == 'POST':
        a = float(request.form['a'])
        b = float(request.form['b'])
        n = int(request.form['n'])
        f = request.form['f']
        filename = f+'_'+str(a)+'-'+str(b)+'_'+str(n)+'.txt'
        f = sympify(f)
        h = (b - a) / n
        somme = 0
        for i in range(1, n):
            somme += f.subs(x,a + i * h)
        resultat = h * somme
        with open(filename,'w+') as file:
            file.write(str(resultat))
            
        return render_template('result.html', filename = filename, result = resultat,heading = "Résultat approximative par la méthode des rectangles",aside = "Résultat")
    return render_template('rectangle.html')



@app.route('/download')
def download():
    filename = request.args.get('filename')
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

