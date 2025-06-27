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

MAX_APP_ENTITIES=100000
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
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion craendo el usuario, verifique los datos enviados"}),500
    else:
        return jsonify({"msg":"Usuario Creado"}),200

@app.route('/user/<int:id>', methods=['GET'])
# Obtener Usuario por ID
def handle_get_user(id):
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de usuario valido"}),400

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

@app.route('/users/favorites', methods=['GET'])
# Obtener Usuario por ID
def handle_get_user_favorites():
    body=json.loads(request.data)
    if body['id'] is None:
        return jsonify({"msg":"Debe especificar el id de usuario"}),400    
    id=body['id']
    if not id.isdigit() or int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de usuario valido"}),400 
    try:
        user=User.query.get(id)
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion buscando los favoritos del usuario"}),500
    #finally: # Corre siempre
    else:
        if user is None: 
            return jsonify({"msg":"No se encontraron favoritos para el usuario"}),404
        serialized_user=user.serialize()
        return serialized_user['favorites'],200


@app.route('/user/<int:id>',methods=['DELETE'])
# Eliminar Usuario por ID
def handle_delete_user(id):
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de usuario valido"}),400
     
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
    people_name=body['name']
    try:
        people_exists=db.session.execute(db.select(People).filter_by(name=people_name)).first()
    except Exception as e:
        return jsonify({"msg":"Excepcion buscado existencias de Personaje"})
    else:
        if people_exists is None:
            try:
                db.session.add(new_people)
                db.session.commit()
            except Exception as e:
                return jsonify({"msg":"Excepcion creando Personaje"})
            else:
                return jsonify({"msg":"Nuevo Personaje Creado"}),200
        else:
            return jsonify({"msg":"Ya existe un Personaje con ese nombre"}),200


@app.route('/people/<int:id>', methods=['GET'])
# Obtener personaje por ID
def handle_get_people(id):
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de personaje valido"}),400
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
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de personaje valido"}),400
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
    planet_name=body['name']
    try:
        planet_exists=db.session.execute(db.select(Planet).filter_by(name=planet_name)).first()
    except Exception as e:
        return jsonify({"msg":"Excepcion buscado existencias del Planeta"})
    else:
        if planet_exists is None:
            try:
                db.session.add(new_planet)
                db.session.commit()
            except Exception as e:
                return jsonify({"msg":"Excepcion creando Planeta"})
            else:
                return jsonify({"msg":"Nuevo Planeta Creado"}),200
        else:
            return jsonify({"msg":"Ya existe un Planeta con ese nombre"}),200




    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"msg":"Nuevo Planeta Creado"}),200

@app.route('/planet/<int:id>', methods=['GET'])
# Obtener planeta por ID
def handle_get_planet(id):
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de planeta valido"}),400
    
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
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de planeta valido"}),400
    
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
    vehicle_name=body['name']
    try:
        vehicle_exists=db.session.execute(db.select(Vehicle).filter_by(name=vehicle_name)).first()
    except Exception as e:
        return jsonify({"msg":"Excepcion buscado existencias de Vehiculo"})
    else:
        if vehicle_exists is None:
            try:
                db.session.add(new_vehicle)
                db.session.commit()
            except Exception as e:
                return jsonify({"msg":"Excepcion creando Vehiculo"})
            else:
                return jsonify({"msg":"Nuevo Vehiculo Creado"}),200
        else:
            return jsonify({"msg":"Ya existe un Vehiculo con ese nombre"}),200

@app.route('/vehicle/<int:id>', methods=['GET'])
# Obtener personaje por ID
def handle_get_vehicle(id):
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de vehiculo valido"}),400
    
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
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de vehiculo valido"}),400
    
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
            return jsonify({"msg":"Debe indicar un id para poder crear el Favorito"}),400

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg":"Nuevo Favorito Creado"}),200

@app.route('/favorite/<int:id>', methods=['GET'])
# Obtener Favorito por ID
def handle_get_favorite(id):
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de favorito valido"}),400
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
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de favorito valido"}),400
    
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


@app.route('/favorite/<string:param_entity_type>/<int:param_entity_id>', methods=['POST'])
# Crea Favorito de un Usuario 
def handle_set_user_favorite(param_entity_type,param_entity_id):
    body=json.loads(request.data)
    if param_entity_type is None:
        return jsonify({"msg":"Debe especificar el tipo para el favorito"}),400    
    if param_entity_id is None:
        return jsonify({"msg":"Debe especificar el id para el favorito"}),400    
    id=param_entity_id
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id valido"}),400 
    
    if not body['user_id'].isdigit() or body['user_id'] is None or int(body['user_id']) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de usuario valido"}),400 

    uid=body['user_id']
    new_favorite=Favorite(
        user_id = uid,
    )
    match param_entity_type:
        case "planet":
            new_favorite.planet_id=param_entity_id
        case "people":
            new_favorite.people_id=param_entity_id
        case _:  # Default case (like 'else')
            return jsonify({"msg":"Debe indicar un id para poder crear el Favorito"}),400


    if param_entity_type == "planet" or param_entity_type == "people":
            try:
                match param_entity_type:
                    case "planet":
                        user_favorite = db.session.execute(db.select(Favorite).filter_by(user_id=uid,planet_id=param_entity_id)).first()
                    case "people":
                        user_favorite = db.session.execute(db.select(Favorite).filter_by(user_id=uid,people_id=param_entity_id)).first()
                    case _:  # Default case (like 'else')
                        return jsonify({"msg":f"Debe indicar un id para poder borrar el Favorito: {param_entity_type}"}),400        
            except Exception as e:
                # Logear algo aca
                return jsonify({"msg":f"Excepcion creando el Favorito, verifique los datos enviados {e}"}),500
            else:
                if user_favorite is None:
                    try:
                        db.session.add(new_favorite)
                        db.session.commit()
                        return jsonify({"msg":"Nuevo Favorito de Planeta Creado"}),200
                    except Exception as e:
                        # Logear algo aca
                        return jsonify({"msg":f"Excepcion creando el Favorito, verifique los datos enviados {e}"}),500
                else:
                        return jsonify({"msg":f"El Favorito que intenta crear ya existe"}),400


@app.route('/favorite/<string:param_entity_type>/<int:param_entity_id>', methods=['DELETE'])
# Borra Favorito de un Usuario 
def handle_delete_user_favorite(param_entity_type,param_entity_id):
    body=json.loads(request.data)
    if param_entity_type is None:
        return jsonify({"msg":"Debe especificar el tipo para el favorito"}),400    
    if param_entity_id is None:
        return jsonify({"msg":"Debe especificar el id para el favorito"}),400    
    id=param_entity_id
    if int(id) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id valido"}),400 
    
    if not body['user_id'].isdigit() or body['user_id'] is None or int(body['user_id']) > MAX_APP_ENTITIES:
        return jsonify({"msg":"Debe especificar el id de usuario valido"}),400 
    
    uid=body['user_id']
    try:
        match param_entity_type:
            case "planet":
                user_favorite = db.session.execute(db.select(Favorite).filter_by(user_id=uid,planet_id=param_entity_id)).scalar_one()
            case "people":
                user_favorite = db.session.execute(db.select(Favorite).filter_by(user_id=uid,people_id=param_entity_id)).scalar_one()
            case _:  # Default case (like 'else')
                return jsonify({"msg":f"Debe indicar un id para poder borrar el Favorito: {param_entity_type}"}),400        
    except Exception as e:
        # Logear algo aca
        return jsonify({"msg":"Excepcion eliminando el Favorito para el usuario especificado, verifique los datos y vuelva a intentarlo"}),500
    else:
        if not user_favorite is None:
            db.session.delete(user_favorite)
            db.session.commit()
            return jsonify({"msg":"Favorito eliminado con exito"}),200
        else:
            return jsonify({"msg":"No se pudo persistir el Favorito para el usuario especificado"}),500
    



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
