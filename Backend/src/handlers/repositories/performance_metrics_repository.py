from datetime import datetime
from sqlalchemy import func
from src.startup.database import db
from src.Models import Order, Driver_Ratings, Driver

from src.Models.orderResponse import OrderResponse
from src.Models.shipment import Shipment

def fetch_deliveries_per_driver(filters):
    start_date = filters.get('start_date', "2025-05-05")
    end_date = filters.get('end_date', None)
    min_deliveries = filters.get('min_deliveries', 0)
    max_deliveries = filters.get('max_deliveries', 100)

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
    print(query.filter(Order.order_date >= datetime.strptime(start_date, '%Y-%m-%d')).first(),"querrryyyyy")
    return result

from sqlalchemy import extract

def fetch_average_delivery_time(filters):
    start_date = filters.get('start_date', None)
    end_date = filters.get('end_date', None)
    min_time = filters.get('min_time', 0)
    max_time = filters.get('max_time', 120)

    query = db.session.query(
        Driver.first_name,
        Driver.last_name,
        func.avg(
            extract('epoch', Shipment.actual_arrival) - extract('epoch', Shipment.actual_departure)
        ).label('avg_delivery_time_seconds')
    ).join(OrderResponse, OrderResponse.driver_id == Driver.driver_id) \
     .join(Order, Order.order_id == OrderResponse.order_id) \
     .join(Shipment, Shipment.order_id == Order.order_id)

    if start_date:
        query = query.filter(Order.order_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Order.order_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id) \
        .having(func.avg(
            extract('epoch', Shipment.actual_arrival) - extract('epoch', Shipment.actual_departure)
        ) >= min_time * 60) \
        .having(func.avg(
            extract('epoch', Shipment.actual_arrival) - extract('epoch', Shipment.actual_departure)
        ) <= max_time * 60)

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

def fetch_customer_ratings(filters):
    start_date = filters.get('start_date', None)
    end_date = filters.get('end_date', None)
    min_rating = filters.get('min_rating', 0)
    max_rating = filters.get('max_rating', 5)

    query = db.session.query(Driver.first_name, Driver.last_name, func.avg(Driver_Ratings.rating).label('avg_rating')) \
        .join(Driver_Ratings, Driver_Ratings.driver_id == Driver.driver_id)

    if start_date:
        query = query.filter(Driver_Ratings.rating_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Driver_Ratings.rating_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id) \
        .having(func.avg(Driver_Ratings.rating) >= min_rating) \
        .having(func.avg(Driver_Ratings.rating) <= max_rating)

    result = query.all()
    return result
