from flask import request, jsonify
from src.handlers.repositories.performance_metrics_repository import (
    fetch_deliveries_per_driver,
    fetch_average_delivery_time,
    fetch_order_acceptance_rejection_rates,
    fetch_customer_ratings
)

def get_deliveries_per_driver():
    filters = request.args.to_dict()
    data = fetch_deliveries_per_driver(filters)
    # Convert SQLAlchemy Row objects to list of dicts for JSON serialization
    result = []
    for row in data:
        result.append({
            "first_name": row[0],
            "last_name": row[1],
            "deliveries": row[2]
        })
    return jsonify(result), 200

def get_average_delivery_time():
    filters = request.args.to_dict()
    result = fetch_average_delivery_time(filters)
    avg_times = []
    for row in result:
        avg_times.append({
            "first_name": row.first_name,
            "last_name": row.last_name,
            "avg_delivery_time_hours": row.avg_delivery_time_hours
        })
    return jsonify(avg_times)

def get_order_acceptance_rejection():
    filters = request.args.to_dict()
    result = fetch_order_acceptance_rejection_rates(filters)
    return jsonify(result)

def get_customer_ratings():
    filters = request.args.to_dict()
    result = fetch_customer_ratings(filters)
    ratings = []
    for row in result:
        ratings.append({
            "first_name": row.first_name,
            "last_name": row.last_name,
            "avg_rating": row.avg_rating
        })
    return jsonify(ratings)
