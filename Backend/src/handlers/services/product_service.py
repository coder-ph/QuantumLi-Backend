from src.handlers.repositories.product_repository import ProductRepository
from src.utils.logger import logger

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def get_product(self, product_id):
        
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            logger.warning(f"[ProductService] Product {product_id} not found in repository.")
            return None
        logger.info(f"[ProductService] Product {product_id} retrieved successfully.")
        return product

    def create_product(self, product_data):
       
        try:
            product = self.product_repository.create_product(product_data)
            logger.info(f"[ProductService] Product {product['product_id']} created successfully.")
            return product
        except Exception as e:
            logger.error(f"[ProductService] Error creating product: {str(e)}")
            return None
    def get_all_products(self):
        try:
            products = self.product_repository.get_all_products()
            logger.info(f"[ProductService] Retrieved {len(products)} products successfully.")
            return products
        except Exception as e:
            logger.error(f"[ProductService] Error retrieving all products: {str(e)}")
            raise e


    def update_product(self, product_id, update_data):
        
        product = self.product_repository.update_product(product_id, update_data)
        if not product:
            logger.warning(f"[ProductService] Product {product_id} not found for update.")
            return None
        logger.info(f"[ProductService] Product {product_id} updated successfully.")
        return product

    def delete_product(self, product_id):
       
        product = self.product_repository.delete_product(product_id)
        if not product:
            logger.warning(f"[ProductService] Product {product_id} not found for deletion.")
            return None
        logger.info(f"[ProductService] Product {product_id} deleted successfully.")
        return product
