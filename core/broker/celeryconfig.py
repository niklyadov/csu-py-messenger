from os import getenv

from dotenv import load_dotenv

load_dotenv()

broker_url = getenv("AMQP_URI")
task_ignore_result = True
task_store_errors_even_if_ignored = True
worker_concurrency = int(getenv("WORKER_CONCURRENCY", "4"))

task_routes = {
    "queue.*": "queue",
}
