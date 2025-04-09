from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.handlers.services.product_service import ProductService
from src.schemas.product_schema import ProductSchema
from src.utils.logger import logger
from src.utils.decorators import roles_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

product_service = ProductService()
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@jwt_required()
@limiter.limit("5 per minute")
def get_product(product_id):
    product = product_service.get_product(product_id)
    if product:
        return product_schema.jsonify(product)
    return jsonify({"message": "Product not found"}), 404

@jwt_required()
@roles_required('admin')
@limiter.limit("5 per minute")
def create_product():
    data = request.get_json()
    try:
        product = product_service.create_product(data)
        if product:
            return product_schema.jsonify(product), 201
        return jsonify({"message": "Failed to create product"}), 400
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@roles_required('admin')
@limiter.limit("5 per minute")
def update_product(product_id):
    data = request.get_json()
    try:
        product = product_service.update_product(product_id, data)
        if product:
            return product_schema.jsonify(product)
        return jsonify({"message": "Failed to update product"}), 400
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@roles_required('admin')
@limiter.limit("5 per minute")
def delete_product(product_id):
    try:
        product = product_service.delete_product(product_id)
        if product:
            return product_schema.jsonify(product)
        return jsonify({"message": "Failed to delete product"}), 400
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500
