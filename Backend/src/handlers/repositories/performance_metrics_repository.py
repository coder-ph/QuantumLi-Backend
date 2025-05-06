from datetime import datetime
from sqlalchemy import func
from src.startup.database import db
from src.Models import Order, Driver_Ratings, Driver

def fetch_deliveries_per_driver(filters):
    start_date = filters.get('start_date', None)
    end_date = filters.get('end_date', None)
    min_deliveries = filters.get('min_deliveries', 0)
    max_deliveries = filters.get('max_deliveries', 100)

    query = db.session.query(Driver.name, func.count(Order.order_id).label('deliveries')) \
        .join(Order, Order.driver_id == Driver.driver_id)

    if start_date:
        query = query.filter(Order.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Order.date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id) \
        .having(func.count(Order.order_id) >= min_deliveries) \
        .having(func.count(Order.order_id) <= max_deliveries)

    result = query.all()
    return result

def fetch_average_delivery_time(filters):
    start_date = filters.get('start_date', None)
    end_date = filters.get('end_date', None)
    min_time = filters.get('min_time', 0)
    max_time = filters.get('max_time', 120)

    query = db.session.query(Driver.name, func.avg(Order.delivery_time).label('avg_delivery_time')) \
        .join(Order, Order.driver_id == Driver.driver_id)

    if start_date:
        query = query.filter(Order.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Order.date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id) \
        .having(func.avg(Order.delivery_time) >= min_time) \
        .having(func.avg(Order.delivery_time) <= max_time)

    result = query.all()
    return result

def fetch_order_acceptance_rejection_rates(filters):
    start_date = filters.get('start_date', None)
    end_date = filters.get('end_date', None)

    query = db.session.query(
        Driver.name,
        func.sum(func.cast(Order.status == 'accepted', db.Integer)).label('accepted'),
        func.sum(func.cast(Order.status == 'rejected', db.Integer)).label('rejected')
    ).join(Order, Order.driver_id == Driver.driver_id)

    if start_date:
        query = query.filter(Order.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Order.date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id)

    result = query.all()
    rates = []
    for row in result:
        total_orders = row.accepted + row.rejected
        acceptance_rate = row.accepted / total_orders if total_orders else 0
        rejection_rate = row.rejected / total_orders if total_orders else 0
        rates.append({
            "driver_name": row.name,
            "acceptance_rate": acceptance_rate,
            "rejection_rate": rejection_rate
        })

    return rates

def fetch_customer_ratings(filters):
    start_date = filters.get('start_date', None)
    end_date = filters.get('end_date', None)
    min_rating = filters.get('min_rating', 0)
    max_rating = filters.get('max_rating', 5)

    query = db.session.query(Driver.name, func.avg(Rating.rating).label('avg_rating')) \
        .join(Rating, Rating.driver_id == Driver.driver_id)

    if start_date:
        query = query.filter(Rating.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Rating.date <= datetime.strptime(end_date, '%Y-%m-%d'))

    query = query.group_by(Driver.driver_id) \
        .having(func.avg(Rating.rating) >= min_rating) \
        .having(func.avg(Rating.rating) <= max_rating)

    result = query.all()
    return result
