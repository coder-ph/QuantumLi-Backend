from src.Models.product import Product
from src.startup.database import db
from sqlalchemy.exc import SQLAlchemyError
from src.utils.logger import logger
import redis
import json


class ProductRepository:
    def __init__(self):
        try:
            self.redis_client = redis.StrictRedis(
                host='localhost',
                port=6379,
                db=0,
                decode_responses=True
            )
            self.redis_client.ping()
        except redis.exceptions.ConnectionError as e:
            logger.warning("[Redis] Connection failed. Caching will be disabled.")
            self.redis_client = None

    def get_product_by_id(self, product_id):
      
        cache_key = f"product:{product_id}"
        try:
            if self.redis_client:
                cached_product = self.redis_client.get(cache_key)
                if cached_product:
                    logger.info(f"[ProductRepository] Cache hit for product {product_id}")
                    return json.loads(cached_product)

            product = Product.query.get(product_id)
            if product:
                if self.redis_client:
                    self.redis_client.setex(cache_key, 3600, json.dumps(product.to_dict()))
                logger.info(f"[ProductRepository] Retrieved product {product_id} from DB")
                return product.to_dict()
            else:
                logger.warning(f"[ProductRepository] Product {product_id} not found.")
                return None
        except Exception as e:
            logger.error(f"[ProductRepository] Error fetching product {product_id}: {str(e)}")
            return None

    def create_product(self, product_data):
        
        try:
            product = Product(**product_data)
            db.session.add(product)
            db.session.commit()
            logger.info(f"[ProductRepository] Product created: {product.id}")
            return product.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"[ProductRepository] DB error during creation: {str(e)}")
            raise e

    def update_product(self, product_id, update_data):
       
        try:
            product = Product.query.get(product_id)
            if not product:
                logger.warning(f"[ProductRepository] Product {product_id} not found for update.")
                return None

            for key, value in update_data.items():
                setattr(product, key, value)

            db.session.commit()

            if self.redis_client:
                self.redis_client.delete(f"product:{product_id}")

            logger.info(f"[ProductRepository] Product {product_id} updated.")
            return product.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"[ProductRepository] DB error during update: {str(e)}")
            raise e

    def delete_product(self, product_id):
        
        try:
            product = Product.query.get(product_id)
            if not product:
                logger.warning(f"[ProductRepository] Product {product_id} not found for deletion.")
                return None

            db.session.delete(product)
            db.session.commit()

            if self.redis_client:
                self.redis_client.delete(f"product:{product_id}")

            logger.info(f"[ProductRepository] Product {product_id} deleted.")
            return product.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"[ProductRepository] DB error during deletion: {str(e)}")
            raise e
        
    def get_all_products(self):
        cache_key = "products:all"
        try:
            if self.redis_client:
                cached_products = self.redis_client.get(cache_key)
                if cached_products:
                    logger.info("[ProductRepository] Cache hit for all products")
                    return json.loads(cached_products)

            products = Product.query.all()
            product_list = [product.to_dict() for product in products]

            if self.redis_client:
                self.redis_client.setex(cache_key, 3600, json.dumps(product_list))

            logger.info("[ProductRepository] Retrieved all products from DB")
            return product_list
        except Exception as e:
            logger.error(f"[ProductRepository] Error fetching all products: {str(e)}")
            return []

