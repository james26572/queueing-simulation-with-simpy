
import random

import simpy


RANDOM_SEED = 42
WAIT_TIMES = []



class CleanFood(object):
    """A cleanfood object has a limited number of servers (``NUM_MACHINES``) to
    serve customers in parallel.

    Customers have to request one of the clerks. When they got one, they
    can start the serving processes and wait for it to finish (which
    takes a certain amount of minutes).

    """
    def __init__(self, env,server_model):
        self.env = env
        self.driveThrough = None
        self.service_times = None
        self.service_probabilities = None
        if server_model == "A" or "C":

        
            self.service_times = [2, 3, 4, 5, 6, 7, 8, 9]
            self.service_probabilities = [.24, .2, .15, .14, .12, .08, .05, .02]
            if server_model == "A":
                self.driveThrough = simpy.Resource(env, 1)
            else:
                self.driveThrough = simpy.Resource(env, 2)
        elif server_model == "B":
            self.service_times = [1,2,3,4,5]
            self.service_probs = [.2,.35,.3,.1,.05]
            self.driveThrough = simpy.Resource(env, 1)

        else:
            print("Invalid sever model")


    def serve(self, car):
        """The serving processes. It takes a ``car`` processes and tries to serve it."""
        service_time = random.choices(self.service_times, self.service_probabilities)[0]
        yield self.env.timeout(service_time)
        print("Finished serving {car}".format(car = car))
        


def car(env, name, cw):
    """The customer process (each customer has a ``name``) arrives at the drive through
    (``cw``) and requests a clerk.

    It then starts the serving process, waits for it to finish and
    leaves to never come back ...

    """
    print('%s arrives at the drive through at %.2f.' % (name, env.now))
    arrival_time = env.now
    begin_service_time = None
    with cw.driveThrough.request() as request:
        yield request

        print('%s enters the service hatch at %.2f.' % (name, env.now))
        begin_service_time = env.now

        WAIT_TIMES.append(begin_service_time-arrival_time)
        yield env.process(cw.serve(name))
        
        

        print('%s leaves the drive through at %.2f.' % (name, env.now))




def setup(env,design):
    """Create a serving model with a given number of clerks
    and generate customers with exponential interarrival times."""
    driveThrough = CleanFood(env, design)

    # Generate cars with exponential interarrival times
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/6))
        i += 1
        env.process(car(env, 'Car %d' % i, driveThrough))






def main(design):
    env = simpy.Environment()
    env.process(setup(env,design))
    env.run(until=300)
    average_wait_time = sum(WAIT_TIMES)/len(WAIT_TIMES)
    max_wait_tme = max(WAIT_TIMES)
    zero_wait_time = WAIT_TIMES.count(float(0))
    print("The average waiting time for a cusomer for design {design} is {average_wait_time} minutes".format(design = design,average_wait_time=average_wait_time))
    print("The max waiting time for a customer for design {design} is {max_wait_time} minutes".format(design = design,max_wait_time = max_wait_tme))
    print("{zero_wait_time}% of customers are served instantly with design {design}".format(zero_wait_time = zero_wait_time,design=design))




main("A")
WAIT_TIMES = []


main("B")
WAIT_TIMES = []

main("C")

