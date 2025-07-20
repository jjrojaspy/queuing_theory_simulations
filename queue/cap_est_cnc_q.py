# Queueing Theory Simulation:
#
# cap: constant arrival probability.
# est: exponential service time.
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
# Simul. has a queue? Yes.
import logging

from random import choice, expovariate, uniform

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

queue = []

total_hours = 12.0
total_minutes = total_hours * 60.0
next_arrive_flag = True
while minute <= total_minutes or len(queue) > 0:
    if uniform(0, 1) <= ARRIVAL_PROBABILITY and minute <= total_minutes:
        arrival_counter += 1

        number_of_costumers_arriving = choice(NUMBER_OF_COSTUMERS_ARRIVING_SAMPLE)
        costumer_counter += number_of_costumers_arriving

        queue.extend(list(range(number_of_costumers_arriving)))
    if len(queue) > 0:
        if service_time <= .0:
            queue.pop(0)

            services_counter += 1
            service_time = expovariate(SERVICE_TIME_RATE)
            cumulative_service_time += service_time

    if service_time > .0:
        service_time -= 1.0

    minute += 1.0

logger.info("******* Results *******")
logger.info("******* Quantities: *******")
logger.info("Number of arrivals: %d " % arrival_counter)
logger.info("Number of arriving customers:  %d" % costumer_counter)
logger.info("Number of served customers: %d" % services_counter)
try:
    logger.info("**************************")
    logger.info("******* Average Values: *******")
    average_arriving_customers = float(costumer_counter) / float(arrival_counter)
    average_service_time = float(cumulative_service_time) / float(services_counter)

    logger.info("Average arriving customers: %f" % average_arriving_customers)
    logger.info("Average service time: %f" % average_service_time)
except ZeroDivisionError:
    logger.info("There was a division by zero...")