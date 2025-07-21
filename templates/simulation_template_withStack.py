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
from simulation import Stack

# ----- Logging Setup -----
formatter = Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console = StreamHandler()
console.setLevel(INFO)
console.setFormatter(formatter)
getLogger('').addHandler(console)

logger = getLogger("queue.simulation")
logger.setLevel(INFO)

# ----- Simulation Parameters -----
CUSTOMER_ARRIVING_PROBABILITY = .95

NUMBER_OF_CUSTOMERS_ARRIVING = [2, 1]

SERVICE_CAPACITY = 200
SERVICE_HOURS = 8.0
SERVICE_TIME_RATE = 1

# ----- Simulation State -----
minute = service_time = 0.0
cumulative_service_time = 0.0

arrival_counter = \
    customer_counter = \
    lost_counter = \
    lost_counter_by_full_queue = \
    lost_counter_by_service_closed = \
    services_counter = 0

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
            for _ in range(customers_arriving):
                queue.add("customer")

            arrival_counter += 1
            customer_counter += customers_arriving
        else:
            lost_counter += customers_arriving
            lost_counter_by_full_queue += customers_arriving
    else:
        lost_counter += customers_arriving
        lost_counter_by_service_closed += customers_arriving

    if not queue.is_empty():
        if is_server_idle():
            queue.pop()
            services_counter += 1

            service_time = generate_service_time()
            cumulative_service_time += service_time

    if is_server_busy():
        service_time -= 1

    minute += 1.0

    if not is_server_open() and queue.is_empty():
        break

# ----- Results -----
logger.info("******* Results *******")
logger.info("******* Quantities: *******")
logger.info("Number of arrivals: %d" % arrival_counter)
logger.info("Number of customers who arrived: %d" % customer_counter)
logger.info("Number of customers served: %d" % services_counter)
logger.info("Number of total customers lost: %d" % lost_counter)
logger.info("Number of total customers lost because the queue was full: %d" % lost_counter_by_full_queue)
logger.info("Number of total customers lost because the service was closed: %d" % lost_counter_by_service_closed)
try:
    logger.info("******* Averages: *******")
    average_arriving_customers = float(customer_counter) / float(arrival_counter)
    average_served_customers = float(services_counter) / float(arrival_counter)
    average_lost_customers = float(lost_counter) / float(arrival_counter)
    average_lost_customers_by_full_queue = float(lost_counter_by_full_queue) / float(lost_counter)
    average_lost_customers_by_service_closed = float(lost_counter_by_service_closed) / float(lost_counter)
    average_service_time = float(cumulative_service_time) / float(services_counter)

    logger.info("Percentage of customers who arrived: %f" % average_arriving_customers)
    logger.info("Percentage of served customers: %f" % average_served_customers)
    logger.info("Percentage of lost customers: %f" % average_lost_customers)
    logger.info("Percentage of lost customers because of a full queue: %f" % average_lost_customers_by_full_queue)
    logger.info("Percentage of lost customers because service closed: %f" % average_lost_customers_by_service_closed)
    logger.info("Average service time: %f" % average_service_time)
except ZeroDivisionError:
    logger.info("A division by zero has occurred...")
