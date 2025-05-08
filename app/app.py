import os
import random
import string
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import redis
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_password = os.getenv("REDIS_PASSWORD")

mongo_uri = os.getenv("MONGO_URI")

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)

mongo_client = MongoClient(mongo_uri)
db = mongo_client.visitor_db
visitors_collection = db.visitors

def generate_random_id(length: int = 4) -> str:
    """Generate a random alphanumeric ID."""
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))

@app.route('/')
def hello_world():

    client_ip = request.remote_addr   
    user_agent = request.headers.get('User-Agent', '')

    total_visits = redis_client.incr('total_visits')

    visitor = visitors_collection.find_one({'ip': client_ip})
    if visitor:
        visitor_id = visitor['id']
        visitors_collection.update_one(
            {'ip': client_ip},
            {'$inc': {'visits': 1}}
        )
        ip_visits = visitors_collection.find_one({'ip': client_ip})['visits']
    else:
        visitor_id = generate_random_id()
        visitors_collection.insert_one({
            'id': visitor_id,
            'ip': client_ip,
            'visits': 1
        })
        ip_visits = 1

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello World App</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
            table {{ border-collapse: collapse; width: 100%; max-width: 800px; margin: 0 auto; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>Hello World!</h1>
        <table>
            <tr><th>Name</th><th>Yousef Alkaranwi</th></tr>
            <tr><td>id</td><td>{visitor_id}</td></tr>
            <tr><td>IP</td><td>{client_ip}</td></tr>
            <tr><td>user-agent</td><td>{user_agent}</td></tr>
            <tr><td>visits (this IP)</td><td>{ip_visits}</td></tr>
            <tr><td>total visits</td><td>{total_visits}</td></tr>
        </table>
	<h1>Yousef Will become a good DevOps Engineer in Beyon Limits Inshallah</h1>
 	<h1>Yousef Will become a good DevOps Engineer in Beyon Limits Inshallah</h1>
    </body>
    </html>
    """

@app.route('/health')
def health_check():
    try:
        redis_client.ping()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Redis connection failed: {e}"}), 500

    try:
        mongo_client.admin.command('ping')
    except Exception as e:
        return jsonify({"status": "error", "message": f"MongoDB connection failed: {e}"}), 500

    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 5050))
    app.run(host=host, port=port)
