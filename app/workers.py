import threading
import queue
import time
import random

task_queue = queue.Queue()
workers = []
worker_count = 3  # initial servers


def worker(worker_id):
    while True:
        task = task_queue.get()
        if task is None:
            break

        print(f"Worker {worker_id} processing task {task}")
        time.sleep(random.uniform(0.5, 2))  # simulate work
        task_queue.task_done()


def start_workers(n):
    global workers, worker_count
    worker_count = n
    workers = []

    for i in range(n):
        t = threading.Thread(target=worker, args=(i,))
        t.daemon = True
        t.start()
        workers.append(t)


def scale_workers(new_count):
    global worker_count

    if new_count > worker_count:
        # scale up
        for i in range(worker_count, new_count):
            t = threading.Thread(target=worker, args=(i,))
            t.daemon = True
            t.start()
            workers.append(t)

    elif new_count < worker_count:
        # scale down
        for _ in range(worker_count - new_count):
            task_queue.put(None)  # signal to stop a worker

    worker_count = new_count


def add_task(task):
    task_queue.put(task)