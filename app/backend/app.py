from flask import Flask, jsonify, request
import time
import random
import os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# ------------------------
# App Metadata (Blue/Green demo)
# ------------------------

APP_VERSION = os.getenv("APP_VERSION", "v1-blue")

# ------------------------
# Prometheus Metrics
# ------------------------

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"]
)

APP_INFO = Counter(
    "app_info",
    "Application info",
    ["app_name", "version"]
)

APP_INFO.labels(
    app_name="auto-scaling-ecommerce-backend",
    version=APP_VERSION
).inc()

# ------------------------
# Fake in-memory DB
# ------------------------

PRODUCTS = [
    {
        "id": "p1",
        "name": "Wireless Headphones",
        "description": "Noise cancelling over-ear headphones",
        "price": 2999,
        "category": "Electronics",
        "image": "https://picsum.photos/300/200?1"
    },
    {
        "id": "p2",
        "name": "Smart Watch",
        "description": "Fitness tracking smart watch",
        "price": 4999,
        "category": "Wearables",
        "image": "https://picsum.photos/300/200?2"
    },
    {
        "id": "p3",
        "name": "Gaming Mouse",
        "description": "High precision RGB gaming mouse",
        "price": 1599,
        "category": "Gaming",
        "image": "https://picsum.photos/300/200?3"
    },
    {
        "id": "p4",
        "name": "Mechanical Keyboard",
        "description": "Blue switch mechanical keyboard",
        "price": 3499,
        "category": "Accessories",
        "image": "https://picsum.photos/300/200?4"
    }
]

# ------------------------
# Routes
# ------------------------

@app.route("/", methods=["GET"])
def home():
    REQUEST_COUNT.labels("GET", "/", 200).inc()
    return jsonify({
        "message": "Backend is running 🚀",
        "version": APP_VERSION
    }), 200


@app.route("/health", methods=["GET"])
def health():
    REQUEST_COUNT.labels("GET", "/health", 200).inc()
    return jsonify({
        "status": "UP",
        "version": APP_VERSION
    }), 200


@app.route("/version", methods=["GET"])
def version():
    REQUEST_COUNT.labels("GET", "/version", 200).inc()
    return jsonify({
        "app": "auto-scaling-ecommerce-backend",
        "version": APP_VERSION
    }), 200


@app.route("/api/products", methods=["GET"])
@REQUEST_LATENCY.labels("/api/products").time()
def get_products():
    burn_cpu()
    REQUEST_COUNT.labels("GET", "/api/products", 200).inc()
    return jsonify(PRODUCTS), 200


@app.route("/api/cart", methods=["POST"])
@REQUEST_LATENCY.labels("/api/cart").time()
def add_to_cart():
    data = request.get_json()
    burn_cpu()
    REQUEST_COUNT.labels("POST", "/api/cart", 201).inc()
    return jsonify({
        "message": "Product added to cart",
        "product_id": data.get("product_id"),
        "version": APP_VERSION
    }), 201


# ------------------------
# Prometheus endpoint
# ------------------------

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }

# ------------------------
# CPU burn (HPA demo)
# ------------------------

def burn_cpu():
    x = 0
    for _ in range(1_000_000):
        x += random.random()
    time.sleep(0.1)

# ------------------------
# Main
# ------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    