from datetime import datetime
from sqlalchemy import func
from src.startup.database import db
from src.Models import Order, Driver_Ratings, Driver

from src.Models.orderResponse import OrderResponse
from src.Models.shipment import Shipment

def fetch_deliveries_per_driver(filters):
    start_date = filters.get('start_date', "2025-05-05")
    end_date = filters.get('end_date', None)
    min_deliveries = int(filters.get('min_deliveries', 0))
    max_deliveries = int(filters.get('max_deliveries', 100))

    # Convert empty string dates to None
    if start_date == '':
        start_date = None
    if end_date == '':
        end_date = None

    query = db.session.query(Driver.first_name, Driver.last_name,Order.order_date).join(OrderResponse, OrderResponse.driver_id == Driver.driver_id).join(Order, Order.order_id == OrderResponse.order_id)
    print(query.all(), "queryyyyyyyyyyyyyyyyyyyyyyyyyyy")

    query = db.session.query(Driver.first_name, Driver.last_name, func.count(Order.order_id).label('deliveries')) \
        .join(OrderResponse, OrderResponse.driver_id == Driver.driver_id) \
        .join(Order, Order.order_id == OrderResponse.order_id)
    # print(query.all(), "queryyyyyyyyyyyyyyyyyyyyyyyyyyy")

    if start_date:
        query = query.filter(Order.order_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Order.order_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id) \
        .having(func.count(Order.order_id) >= min_deliveries) \
        .having(func.count(Order.order_id) <= max_deliveries)



    result = query.all()
    return result


from sqlalchemy import extract

def fetch_average_delivery_time(filters):
    start_date = filters.get('start_date', None)
    end_date = filters.get('end_date', None)
    min_time = float(filters.get('min_time', 0))
    max_time = float(filters.get('max_time', 120))

    query = db.session.query(
        Driver.first_name,
        Driver.last_name,
        (func.avg(
            extract('epoch', Shipment.actual_arrival) - extract('epoch', Shipment.actual_departure)
        ) / 3600).label('avg_delivery_time_hours')
    ).join(OrderResponse, OrderResponse.driver_id == Driver.driver_id) \
     .join(Order, Order.order_id == OrderResponse.order_id) \
     .join(Shipment, Shipment.order_id == Order.order_id)

    if start_date:
        query = query.filter(Order.order_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Order.order_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id)
    # Temporarily comment out having clauses to debug empty results
    # .having(func.avg(
    #     extract('epoch', Shipment.actual_arrival) - extract('epoch', Shipment.actual_departure)
    # ) >= min_time * 60) \
    # .having(func.avg(
    #     extract('epoch', Shipment.actual_arrival) - extract('epoch', Shipment.actual_departure)
    # ) <= max_time * 60)

    count = query.count()
    from src.utils.logger import logger
    logger.info(f"fetch_average_delivery_time: Found {count} records matching filters.")

    result = query.all()
    return result


def fetch_order_acceptance_rejection_rates(filters):
    start_date = filters.get('start_date', None)
    end_date = filters.get('end_date', None)

    query = db.session.query(
        Driver.first_name,
        Driver.last_name,
        func.sum(func.cast(OrderResponse.status == 'accepted', db.Integer)).label('accepted'),
        func.sum(func.cast(OrderResponse.status == 'rejected', db.Integer)).label('rejected')
    ).join(OrderResponse, OrderResponse.driver_id == Driver.driver_id) \
     .join(Order, Order.order_id == OrderResponse.order_id)

    if start_date:
        query = query.filter(Order.order_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Order.order_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id)

    result = query.all()
    rates = []
    for row in result:
        total_orders = row.accepted + row.rejected
        acceptance_rate = row.accepted / total_orders if total_orders else 0
        rejection_rate = row.rejected / total_orders if total_orders else 0
        rates.append({
            "driver_name": f"{row.first_name} {row.last_name}",
            "acceptance_rate": acceptance_rate,
            "rejection_rate": rejection_rate
        })

    return rates


from src.utils.logger import logger
from datetime import datetime
from sqlalchemy import func
from src.startup.database import db
from src.Models.drivers import Driver
from src.Models.driverRating import Driver_Ratings

def fetch_customer_ratings(filters):
    start_date = filters.get('start_date', None)
    end_date = filters.get('end_date', None)
    min_rating = float(filters.get('min_rating', 0))
    max_rating = float(filters.get('max_rating', 5))

    query = db.session.query(Driver.first_name, Driver.last_name, func.avg(Driver_Ratings.rating).label('avg_rating')) \
        .join(Driver_Ratings, Driver_Ratings.driver_id == Driver.driver_id)

    if start_date:
        query = query.filter(Driver_Ratings.rating_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Driver_Ratings.rating_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id) \
        .having(func.avg(Driver_Ratings.rating) >= min_rating) \
        .having(func.avg(Driver_Ratings.rating) <= max_rating)

    count = query.count()
    logger.info(f"fetch_customer_ratings: Found {count} ratings matching filters.")

    result = query.all()
    return result
