from redis import Redis
from rq import Worker
from config import REDIS_CONNECTION_STRING, TASK_QUEUE, MONGO_DB_URI
import argparse
from mongoengine import connect

connect(host=MONGO_DB_URI)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--action", help="Define what you want to do.", choices=["work"], required=True
    )
    args = parser.parse_args()

    if args.action == "work":
        connection = Redis.from_url(REDIS_CONNECTION_STRING)
        worker = Worker([TASK_QUEUE], connection=connection)
        worker.work()
