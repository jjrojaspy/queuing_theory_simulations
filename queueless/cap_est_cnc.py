# Queueing Theory Simulation:
#
# cap: constant arrival probability
# cst: constant service time.
# cnc: constant number of customers.
#
# Type of Queue: infinite.
# Arrival process: constant probability.
# Queue discipline: FIFO.
# Service process: time ~ exponential(SERVICE_TIME_RATE).
# System capacity:
#   Number of customers allowed: infinite.
#   System availability time: 8 hours.
# Number of servers: 1.
# Simul. has a queue? No.
import logging
import random

ARRIVAL_PROBABILITY = .25
NUMBER_OF_COSTUMERS_ARRIVING_SAMPLE = [1, 2, 3, 4, 5]
SERVICE_TIME_RATE = 2

formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logging.getLogger('').addHandler(console)

logger = logging.getLogger("queue.simulation")
logger.setLevel(logging.INFO)

minute = service_time = .0
cumulative_time_between_arrivals = cumulative_service_time = .0
arrival_counter = costumer_counter = services_counter = 0
queue_length = 0

total_hours = 12.0
total_minutes = total_hours * 60.0
next_arrive_flag = True
while minute <= total_minutes or queue_length > 0:
    if random.uniform(0, 1) <= ARRIVAL_PROBABILITY and minute <= total_minutes:
        arrival_counter += 1
        number_of_costumers_arriving = random.choice(NUMBER_OF_COSTUMERS_ARRIVING_SAMPLE)
        costumer_counter += number_of_costumers_arriving
        queue_length += number_of_costumers_arriving

    if queue_length > 0:
        if service_time <= .0:
            queue_length -= 1
            services_counter += 1
            service_time = random.expovariate(SERVICE_TIME_RATE)
            cumulative_service_time += service_time
    if service_time > .0:
        service_time -= 1.0

    minute += 1.0

logger.info("******* Results *******")
logger.info("******* Quantities: *******")
logger.info("Number of arrivals: %d" % arrival_counter)
logger.info("Number of customers who arrived: %d" % costumer_counter)
logger.info("Number of customers served: %d" % services_counter)
try:
    logger.info("******* Averages: *******")
    average_arriving_customers = float(costumer_counter) / float(arrival_counter)
    average_service_time = float(cumulative_service_time) / float(services_counter)

    logger.info("Average number of customers who arrived: %f" % average_arriving_customers)
    logger.info("Average service time: %f" % average_service_time)
except ZeroDivisionError:
    logger.info("A division by zero has occurred...")
