#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# class Plant:
#     def __init__(self,id,name,image,price):
#         self.id = id
#         self.name = name
#         self.image = image
#         self.price = price

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "image": self.image,
#             "price": self.price
#         }    

class Plants(Resource):
    def get(self):
       response_dict_list = [plant.to_dict() for plant in Plant.query.all()]
       response  = make_response(jsonify(response_dict_list),200)
       return response
    
    def post(self):
        new_plant = Plant(
            name= request.json['name'],
            image = request.json['image'],
            price = request.json['price']                   
        )
        db.session.add(new_plant)
        db.session.commit()
        response_dict = new_plant.to_dict()
        return make_response(jsonify(response_dict), 201)
    
api.add_resource(Plants, '/plants')    

class PlantByID(Resource):
    def get(self,id):

        plant = Plant.query.filter_by(id = id).first()
        response = make_response(jsonify(plant.to_dict()),200)
        return response
        
api.add_resource(PlantByID, '/plants/<int:id>')  



     
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
