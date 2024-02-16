from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from models import ItemModel
from schemas import ItemSchema,ItemUpdateSchema

blp = Blueprint("items",__name__, description="Operations on items")


@blp.route("/items/<int:item_id>")
class Item(MethodView):
    # @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    # @jwt_required()
    def delete(self, item_id):
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401,message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)

        db.session.delete(item)

        db.session.commit()
        return {"message":"Item deleted."},204

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        # item_data
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id,**item_data)

        db.session.add(item)
        db.session.commit()

        return item



@blp.route("/items")
class ItemList(MethodView):
    # هر دفعه از داخل این اسکیما رد میشه
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    # @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        # it will not be checked for
        # uniqueness here
        item = ItemModel(**item_data)

        try:
            # you can do role back in session
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An Error occured while inserting the item.")

        return item
