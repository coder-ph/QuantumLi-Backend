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
    """
    Fetch a product by ID.
    Requires authentication via JWT and rate limiting.
    """
    try:
        # Attempt to retrieve product from service layer
        product = product_service.get_product(product_id)
        
        if not product:
            logger.warning(f"[get_product] Product with ID {product_id} not found.")
            return jsonify({"message": f"Product with ID {product_id} not found."}), 404
        
        # Successfully found product, return response
        return jsonify(product_schema.dump(product)), 200

    except Exception as e:
        logger.error(f"[get_product] Error retrieving product with ID {product_id}: {str(e)}")
        return jsonify({"message": "An error occurred while retrieving the product."}), 500

@limiter.limit("5 per minute")
@jwt_required()
@roles_required("admin")  # Example role-based access
def get_all_products():
    """
    Get all products.
    """
    try:
        products = product_service.get_all_products()
        if not products:
            logger.warning("[get_all_products] No products found.")
            return jsonify({"message": "No products found."}), 404
        
        # Return list of products
        return jsonify(products_schema.dump(products)), 200

    except Exception as e:
        logger.error(f"[get_all_products] Error retrieving products: {str(e)}")
        return jsonify({"message": "An error occurred while retrieving products."}), 500
