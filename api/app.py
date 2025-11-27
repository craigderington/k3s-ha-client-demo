from flask import Flask, jsonify
import os
import redis
import socket

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
COUNTER_KEY = os.getenv("COUNTER_KEY", "demo-counter")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
hostname = socket.gethostname()


@app.route("/api/value", methods=["GET"])
def get_value():
    value = r.get(COUNTER_KEY)
    if value is None:
        value = 0
        r.set(COUNTER_KEY, value)
    return jsonify({"value": int(value), "pod": hostname})


@app.route("/api/increment", methods=["POST"])
def increment():
    value = r.incr(COUNTER_KEY)
    return jsonify({"value": int(value), "pod": hostname})


@app.route("/healthz")
def healthz():
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

