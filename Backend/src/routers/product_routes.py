from flask import Blueprint
from src.handlers.controllers.product_controller import (get_product,get_all_products,
    create_product,
    update_product,
    delete_product)
    


product_bp = Blueprint('product_bp', __name__)

product_bp.add_url_rule('/products/<uuid:product_id>', 'get_product', get_product, methods=['GET'])
product_bp.add_url_rule('/products', 'get_all_products', get_all_products, methods=['GET'])
product_bp.add_url_rule('/products', 'create_product', create_product, methods=['POST'])
product_bp.add_url_rule('/products/<uuid:product_id>', 'update_product', update_product, methods=['PUT'])
product_bp.add_url_rule('/products/<uuid:product_id>', 'delete_product', delete_product, methods=['DELETE'])
