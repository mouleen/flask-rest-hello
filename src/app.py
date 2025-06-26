"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Vehicle, Favorite
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/example2.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code



def get_http_code(body):
    if not body:
        return 400
    else:
        return 200



# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


## Users 

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
# Listar Usuarios
def handle_get_users():
    users=User.query.all()
    if len(users) < 1: 
        return jsonify({"msg":"No se encontraron usuarios"}),404
    
    serialized_users=list(map(lambda x:x.serialize(),users))
    return serialized_users,200
    
@app.route('/user',methods=['POST'])
# Crear Usuario
def handle_create_user():
    body=json.loads(request.data)
    new_user=User(
        username = body['username'],
        email= body['email'],
        password= body['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg":"Usuario Creado"}),200

@app.route('/user/<int:id>', methods=['GET'])
# Obtener Usuario por ID
def handle_get_user(id):
    try:
        user=User.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el usuario"}),500
    #finally: # Corre siempre
    else:
        if user is None: 
            return jsonify({"msg":"No se encontro el usuario"}),404
        serialized_user=user.serialize()
        return serialized_user,200

@app.route('/user/<int:id>',methods=['DELETE'])
# Eliminar Usuario por ID
def handle_delete_user(id):
    try:
        user=User.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el usuario"}),500
    #finally: # Corre siempre
    else:
        if user is None: 
            return jsonify({"msg":"No se encontro el usuario"}),404
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            # Logear algo aca
            return jsonify({"msg":"Excepcion borrando el usuario"}),500
        else:
            return jsonify({"msg":"Usuario eliminado con exito"}),200


## People

@app.route('/people', methods=['GET'])
# Listar personajes
def handle_get_people_all():
    people=People.query.all()
    if len(people) < 1: 
        return jsonify({"msg":"No se encontraron Personajes"}),404
    
    serialized_people=list(map(lambda x:x.serialize(),people))
    return serialized_people,200

@app.route('/people',methods=['POST'])
# Crear personaje
def handle_create_people():
    body=json.loads(request.data)
    new_people=People(
        name = body['name']
    )
    db.session.add(new_people)
    db.session.commit()
    return jsonify({"msg":"Nuevo Personaje Creado"}),200

@app.route('/people/<int:id>', methods=['GET'])
# Obtener personaje por ID
def handle_get_people(id):
    try:
        people=People.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el Personaje"}),500
    #finally: # Corre siempre
    else:
        if people is None: 
            return jsonify({"msg":"No se encontro el Personaje"}),404
        serialized_people=people.serialize()
        return serialized_people,200

@app.route('/people/<int:id>',methods=['DELETE'])
# Eliminar personaje por ID
def handle_delete_people(id):
    try:
        people=People.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el Personaje"}),500
    #finally: # Corre siempre
    else:
        if people is None: 
            return jsonify({"msg":"No se encontro el Personaje"}),404
        try:
            db.session.delete(people)
            db.session.commit()
        except Exception as e:
            # Logear algo aca
            return jsonify({"msg":"Excepcion borrando el Personaje"}),500
        else:
            return jsonify({"msg":"Personaje eliminado con exito"}),200



## Planets

@app.route('/planets', methods=['GET'])
# Listar Planetas
def handle_get_planets():
    planets=Planet.query.all()
    if len(planets) < 1: 
        return jsonify({"msg":"No se encontraron Planetas"}),404
    
    serialized_planets=list(map(lambda x:x.serialize(),planets))
    return serialized_planets,200

@app.route('/planet',methods=['POST'])
# Crear Planeta
def handle_create_planet():
    body=json.loads(request.data)
    new_planet=Planet(
        name = body['name']
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"msg":"Nuevo Planeta Creado"}),200

@app.route('/planet/<int:id>', methods=['GET'])
# Obtener planeta por ID
def handle_get_planet(id):
    try:
        planet=Planet.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el Planeta"}),500
    #finally: # Corre siempre
    else:
        if planet is None: 
            return jsonify({"msg":"No se encontro el Planeta"}),404
        serialized_planet=planet.serialize()
        return serialized_planet,200

@app.route('/planet/<int:id>',methods=['DELETE'])
# Eliminar planeta por ID
def handle_delete_planet(id):
    try:
        planet=Planet.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el Planeta"}),500
    #finally: # Corre siempre
    else:
        if planet is None: 
            return jsonify({"msg":"No se encontro el Planeta"}),404
        try:
            db.session.delete(planet)
            db.session.commit()
        except Exception as e:
            # Logear algo aca
            return jsonify({"msg":"Excepcion borrando el Planeta"}),500
        else:
            return jsonify({"msg":"Planeta eliminado con exito"}),200


## Vehicles 

@app.route('/vehicles', methods=['GET'])
# Listar Vehiculos
def handle_get_vehicles():  
    vehicles=Vehicle.query.all()
    if len(vehicles) < 1: 
        return jsonify({"msg":"No se encontraron Vehiculos"}),404
    
    serialized_vehicles=list(map(lambda x:x.serialize(),vehicles))
    return serialized_vehicles,200

@app.route('/vehicle',methods=['POST'])
# Crear Vehiculos
def handle_create_vehicle():
    body=json.loads(request.data)
    new_vehicle=Vehicle(
        name = body['name']
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({"msg":"Nuevo Vehiculo Creado"}),200

@app.route('/vehicle/<int:id>', methods=['GET'])
# Obtener personaje por ID
def handle_get_vehicle(id):
    try:
        vehicle=Vehicle.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el Vehiculo"}),500
    #finally: # Corre siempre
    else:
        if vehicle is None: 
            return jsonify({"msg":"No se encontro el Vehiculo"}),404
        serialized_vehicle=vehicle.serialize()
        return serialized_vehicle,200

@app.route('/vehicle/<int:id>',methods=['DELETE'])
# Eliminar Vehiculo por ID
def handle_delete_vehicle(id):
    try:
        vehicle=Vehicle.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el Vehiculo"}),500
    #finally: # Corre siempre
    else:
        if vehicle is None: 
            return jsonify({"msg":"No se encontro el Vehiculo"}),404
        try:
            db.session.delete(vehicle)
            db.session.commit()
        except Exception as e:
            # Logear algo aca
            return jsonify({"msg":"Excepcion borrando el Vehiculo"}),500
        else:
            return jsonify({"msg":"Vehiculo eliminado con exito"}),200

## Favorites

@app.route('/favorites', methods=['GET'])
# Listar Favoritos
def handle_get_favorite_all():
    favorites=Favorite.query.all()
    if len(favorites) < 1: 
        return jsonify({"msg":"No se encontraron Favoritos"
                        }),404
    serialized_favorite=list(map(lambda x:x.serialize(),favorites))
    return serialized_favorite,200

@app.route('/favorite',methods=['POST'])
# Crear Favoritos
def handle_create_favorite():
    body=json.loads(request.data)
    if body is None or body['user_id'] is None or body['type'] is None or body['id'] is None: 
        return jsonify({"msg":"No se especificaron datos para la acción"}),400
    
    new_favorite=Favorite(
        user_id = body['user_id']
    )
    match body['type']:
        case "planet":
            new_favorite.planet_id=body['id']
        case "people":
            new_favorite.people_id=body['id']
        case "vehicle":
            new_favorite.vehicle_id=body['id']
        case _:  # Default case (like 'else')
            return jsonify({"msg":"Debe indicar un is para poder crear el Favorito"}),400

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg":"Nuevo Favorito Creado"}),200

@app.route('/favorite/<int:id>', methods=['GET'])
# Obtener Favorito por ID
def handle_get_favorite(id):
    try:
        favorite=Favorite.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el Favorito"}),500
    #finally: # Corre siempre
    else:
        if favorite is None: 
            return jsonify({"msg":"No se encontro el Favorito"}),404
        serialized_favorite=favorite.serialize()
        return serialized_favorite,200

@app.route('/favorite/<int:id>',methods=['DELETE'])
# Eliminar Favorito por ID
def handle_delete_favorite(id):
    try:
        favorite=Favorite.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando el Favorito"}),500
    #finally: # Corre siempre
    else:
        if favorite is None: 
            return jsonify({"msg":"No se encontro el Favorito"}),404
        try:
            db.session.delete(favorite)
            db.session.commit()
        except Exception as e:
            # Logear algo aca
            return jsonify({"msg":"Excepcion borrando el Favorito"}),500
        else:
            return jsonify({"msg":"Favorito eliminado con exito"}),200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
