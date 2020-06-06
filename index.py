from flask import Flask, render_template
from string import Template
app = Flask(__name__)

import database

@app.route("/")
def main():
    db = database.Database()
    # db.addCar("A4","Audi","Elektryczny")
    offers,columns = db.getOffers_index()
    f = open("./templates/index.html", "r")
    index = Template(f.read())

    f = open("./templates/container.html", "r")
    container = f.read()
    f.close()

    container_id = open("./static/containter_id.css", "r")
    con_id = container_id.read()
    container_id.close()

    containers = ""
    container_id_css = ""
    print(offers)
    # print(offers[1][0])
    for i in range(len(offers)):
        cont_id = Template(con_id)
        cont_id = cont_id.substitute(CSS_id=offers[i][0],CSS_image=offers[i][2])
        container_id_css+= cont_id + "\n\n"
        # print(container_id_css)
        cont = Template(container)
        # print(str(cont_id))
        cont = cont.substitute(CSS_id = offers[i][0],Car_name=offers[i][1])
        containers += cont + "\n"
    print(container_id_css)
    index = index.substitute(container = containers, car_id_css=str(container_id_css))
    return index

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run()
    