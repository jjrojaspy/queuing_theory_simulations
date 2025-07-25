import logging
import random

# ----- Simulation Parameters -----
ARRIVAL_PROBABILITY = 0.25
CUSTOMERS_ARRIVAL_SAMPLE = [1, 2, 3, 4, 5]
SERVICE_TIME_RATE = .25
TOTAL_HOURS = 12.0

# ----- Logging Setup -----
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger("queue.simulation")
logger.setLevel(logging.INFO)


# ----- Helper Functions -----
def generate_service_time(rate):
    return random.expovariate(rate)


def generate_arrivals(probability, sample):
    if random.uniform(0, 1) <= probability:
        return random.choice(sample)
    return 0


def enqueue_customers(queue, num_customers):
    for _ in range(num_customers):
        queue.append("Customer")


def dequeue_customer(queue):
    return queue.pop(0) if queue else None


def check_customers():
    return len(customer_queue) > 0


# ----- Simulation State -----
arrivals = 0
arrival_counter = customer_counter = services_counter = 0
cumulative_service_time = 0.0
minute = service_time = 0.0
total_minutes = TOTAL_HOURS * 60.0

customer_queue = []
# ----- Simulation Loop -----
while minute <= total_minutes or customer_queue:
    arrivals = generate_arrivals(ARRIVAL_PROBABILITY, CUSTOMERS_ARRIVAL_SAMPLE)
    if arrivals > 0 and minute <= total_minutes:
        arrival_counter += 1
        customer_counter += arrivals
        enqueue_customers(customer_queue, arrivals)

    if check_customers():
        if service_time <= 0.0:
            dequeue_customer(customer_queue)
            services_counter += 1
            service_time = generate_service_time(SERVICE_TIME_RATE)
            cumulative_service_time += service_time
    if service_time > 0.0:
        service_time -= 1.0

    minute += 1.0

# ----- Results -----
logger.info("******* Results *******")
logger.info("******* Quantities: *******")
logger.info("Number of arrivals: %d" % arrival_counter)
logger.info("Number of customers who arrived: %d" % customer_counter)
logger.info("Number of customers served: %d" % services_counter)
try:
    logger.info("******* Averages: *******")
    average_arriving_customers = float(customer_counter) / float(arrival_counter)
    average_service_time = float(cumulative_service_time) / float(services_counter)

    logger.info("Average number of customers who arrived: %f" % average_arriving_customers)
    logger.info("Average service time: %f" % average_service_time)
except ZeroDivisionError:
    logger.info("A division by zero has occurred...")
