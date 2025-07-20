# Queueing Theory Simulation:
#
# cat: constant arrival time.
# cst: constant service time.
# cnc: constant number of customers.
#
# Type of Queue: infinite.
# Arrival process: constant time.
# Queue discipline: FIFO.
# Service process: constant time.
# System capacity:
#   Number of customers allowed: infinite.
#   System availability time: 8 hours.
# Number of servers: 1.
# Simul. has a queue? Yes.
import logging

from random import choice

TIMES_BETWEEN_ARRIVALS_SAMPLE = [2, 3, 5, 7, 11]
NUMBER_OF_COSTUMERS_ARRIVING_SAMPLE = [1,2,3]
SERVICE_TIMES_SAMPLE = [4, 6, 8, 9, 10, 12]

formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logging.getLogger('').addHandler(console)

logger = logging.getLogger("queue.simulation")
logger.setLevel(logging.INFO)

minute = next_arrival_time = service_time = 0

cumulative_time_between_arrivals = cumulative_service_time = 0

times_counter = arrival_counter = costumer_counter = services_counter = 0

queue = []

total_hours = 8
total_minutes = total_hours * 60
next_arrive_flag = True
while minute <= total_minutes or len(queue) > 0:
    if minute <= total_minutes and next_arrive_flag:
        times_counter += 1

        time_between_arrivals = choice(TIMES_BETWEEN_ARRIVALS_SAMPLE)

        next_arrival_time = minute + time_between_arrivals
        cumulative_time_between_arrivals += time_between_arrivals

        next_arrive_flag = False

    if minute == next_arrival_time:
        arrival_counter += 1

        number_of_costumers_arriving = choice(NUMBER_OF_COSTUMERS_ARRIVING_SAMPLE)

        costumer_counter += number_of_costumers_arriving

        queue.extend(list(range(number_of_costumers_arriving)))

        next_arrive_flag = True

    if len(queue) > 0:
        if service_time <= 0:
            queue.pop(0)

            services_counter += 1
            service_time = choice(SERVICE_TIMES_SAMPLE)
            cumulative_service_time += service_time

    if service_time > 0:
        service_time -= 1

    minute += 1

logger.info("******* Results *******")
logger.info("******* Quantities *******")
logger.info("Number of arrival times generated: %d" % times_counter)
logger.info("Number of arrivals generated: %d " % arrival_counter)
logger.info("Number of customers arriving:  %d" % costumer_counter)
logger.info("Number of served customers: %d" % services_counter)
try:
    logger.info("******* Averages: *******")
    average_time_between_arrivals = float(cumulative_time_between_arrivals) / float(times_counter)
    average_arriving_customers = float(costumer_counter) / float(arrival_counter)
    average_service_time = float(cumulative_service_time) / float(services_counter)

    logger.info("Time between arrivals average: %f" % average_time_between_arrivals)
    logger.info("Number of customers average: %f" % average_arriving_customers)
    logger.info("Service time average: %f" % average_service_time)
except ZeroDivisionError:
    logger.info("There was a division by zero...")
