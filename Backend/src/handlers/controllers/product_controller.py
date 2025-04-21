from flask import request, jsonify
from flask_jwt_extended import jwt_required
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

@limiter.limit("10 per minute")
def get_product(product_id):
    try:
        product = product_service.get_product(product_id)
        if product:
            logger.info(f"[ProductController] Product {product_id} retrieved successfully.")
            return product_schema.jsonify(product)
        logger.warning(f"[ProductController] Product {product_id} not found.")
        return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        logger.error(f"[ProductController] Error retrieving product {product_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500



@limiter.limit("5 per minute")
def get_all_products():
    try:
        products = product_service.get_all_products()
        logger.info(f"[ProductController] Retrieved {len(products)} products.")
        return jsonify(products_schema.dump(products)), 200
    except Exception as e:
        logger.error(f"[ProductController] Error fetching products: {str(e)}")
        return jsonify({"message": "Failed to fetch products"}), 500


@jwt_required()
@roles_required('admin')
@limiter.limit("5 per minute")
def create_product():
    data = request.get_json()
    try:
        product = product_service.create_product(data)
        if product:
            logger.info(f"[ProductController] Product created: {product.get('id')}")
            return product_schema.jsonify(product), 201
        logger.warning("[ProductController] Product creation failed.")
        return jsonify({"message": "Failed to create product"}), 400
    except Exception as e:
        logger.error(f"[ProductController] Error creating product: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@roles_required('admin')
@limiter.limit("5 per minute")
def update_product(product_id):
    data = request.get_json()
    try:
        product = product_service.update_product(product_id, data)
        if product:
            logger.info(f"[ProductController] Product {product_id} updated successfully.")
            return product_schema.jsonify(product)
        logger.warning(f"[ProductController] Failed to update product {product_id}.")
        return jsonify({"message": "Failed to update product"}), 400
    except Exception as e:
        logger.error(f"[ProductController] Error updating product {product_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@jwt_required()
@roles_required('admin')
@limiter.limit("5 per minute")
def delete_product(product_id):
    try:
        product = product_service.delete_product(product_id)
        if product:
            logger.info(f"[ProductController] Product {product_id} deleted.")
            return product_schema.jsonify(product)
        logger.warning(f"[ProductController] Failed to delete product {product_id}.")
        return jsonify({"message": "Failed to delete product"}), 400
    except Exception as e:
        logger.error(f"[ProductController] Error deleting product {product_id}: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500
