# Queueing Theory Simulation:
#
# cap: constant arrival probability.
# est: exponential service time.
# cnc: constant number of customers.
#
# Type of Queue: finite.
#   Capacity: 200 - This value can be modified for testing purposes.
# Arrival process: constant probability.
# Queue discipline: LIFO.
# Service process: time ~ exponential(SERVICE_TIME_RATE).
# System capacity:
#   Number of customers allowed: finite.
#   System availability time: 8 hours.
# Number of servers: 1.
# Simul. has a queue? Yes.
from logging import INFO, Formatter, StreamHandler, getLogger
from random import expovariate, uniform, choice
from statistics import mean

from simulation import Stack

# ----- Constants -----
BLANK_MESSAGE = "                       "

# ----- Logging Setup -----
formatter = Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console = StreamHandler()
console.setLevel(INFO)
console.setFormatter(formatter)
getLogger('').addHandler(console)

logger = getLogger("queue.simulation")
logger.setLevel(INFO)

# ----- Simulation Parameters -----
CUSTOMER_ARRIVING_PROBABILITY = .99

NUMBER_OF_CUSTOMERS_ARRIVING = [2, 1]

SERVICE_CAPACITY = 235
SERVICE_HOURS = 8.0
SERVICE_TIME_RATE = 50

# ----- Simulation State -----
minute = service_time = 0.0

arrival_counter = 0

customers: list[int] = []
service_times: list[float] = []

lost_customers: list[int] = []
lost_customers_by_full_queue: list[int] = []
lost_customers_by_service_closed: list[int] = []

queue = Stack(SERVICE_CAPACITY, str)


# ----- Helper Functions -----
def generate_arrivals():
    if uniform(0, 1) <= CUSTOMER_ARRIVING_PROBABILITY:
        return choice(NUMBER_OF_CUSTOMERS_ARRIVING)

    return 0


def generate_service_time():
    return expovariate(SERVICE_TIME_RATE)


def is_server_busy():
    return service_time > .0


def is_server_idle():
    return service_time <= .0


def is_server_open():
    return minute <= SERVICE_HOURS * 60.0


while True:
    customers_arriving = generate_arrivals()
    if is_server_open():
        if 0 < customers_arriving <= queue.capacity() - queue.count():
            arrival_counter += 1
            customers.append(customers_arriving)
            for _ in range(customers_arriving):
                queue.add("customer")
        elif customers_arriving > queue.capacity() - queue.count():
            lost_customers.append(customers_arriving)
            lost_customers_by_full_queue.append(customers_arriving)
    else:
        lost_customers.append(customers_arriving)
        lost_customers_by_service_closed.append(customers_arriving)

    if not queue.is_empty():
        if is_server_idle():
            queue.pop()

            service_time = generate_service_time()
            service_times.append(service_time)
    if is_server_busy():
        service_time -= 1

    minute += 1.0

    if not is_server_open() and queue.is_empty():
        break

# ----- Results -----
logger.info("******* Results *******")
logger.info(BLANK_MESSAGE)
logger.info("******* Quantities: *******")
logger.info("Number of arrival events: %d" % arrival_counter)
logger.info("Number of customers who arrived: %d" % sum(customers))
logger.info("Number of customers served: %d" % len(service_times))

if len(lost_customers) > 0:
    logger.info("Number of total customers lost: %d" % sum(lost_customers))
if len(lost_customers_by_full_queue) > 0:
    logger.info("Number of total customers lost because the queue was full: %d" % sum(lost_customers_by_full_queue))
if len(lost_customers_by_service_closed) > 0:
    logger.info(
        "Number of total customers lost because the service was closed: %d" % sum(lost_customers_by_service_closed))

logger.info(BLANK_MESSAGE)
logger.info("******* Averages: *******")
logger.info("Average number of customers who arrived: %f" % mean(customers))

if len(lost_customers) > 0:
    logger.info("Average number of lost customers: %f" % mean(lost_customers))
if len(lost_customers_by_full_queue) > 0:
    logger.info("Average number of lost customers because of a full queue: %f" % mean(lost_customers_by_full_queue))
if len(lost_customers_by_service_closed) > 0:
    logger.info("Average number of lost customers because service closed: %f" % mean(lost_customers_by_service_closed))

logger.info("Average service time: %f" % mean(service_times))
