import random
import statistics
import math
"""
    Function used to test the speed of many simulations.
    Parameters:
        Type : String
            Type of strategy to use
        numTrials : int
            Number of simulations to conduct
        baggage : int
            Amount of baggage each passenger has
        percentFast : float
            Percentage of passengers that move quickly
        randomiseBaggage : Bool
            If True randomise the amount of baggage each passenger has from
            0 to baggage
"""
def simulationTest(Type, numTrials, baggage, percentFast, randomiseBaggage):
    if Type not in ["Random", "Back-to-Front", "Front-to-Back", "Outside-In", "Reverse-Pyramid"]:
        print("Invalid strategy")
        return
    times = []
    for i in range(numTrials):
        times.append(simulation(False, Type, baggage, percentFast, randomiseBaggage))
    print("Average Time taken for strategy " + Type + " was " + str(statistics.mean(times)))
    print("Standard Error in time is " + str(statistics.stdev(times)/math.sqrt(numTrials)))
    return

"""
    Function that assigns the passengers seats so a strategy can be used.
    Parameters:
        Type : String
            Type of strategy to use
        baggage : int
            Amount of baggage each passenger has
        percentFast : float
            Percentage of passengers that move quickly
        randomiseBaggage : Bool
            If True randomise the amount of baggage each passenger has from
            0 to baggage
    Returns:
        Sorted list of passengers
"""
def assignSeats(Type, baggage, percentFast, randomiseBaggage):
    Passengers = []
    if Type == "Random":
        unassignedSeats = [x for x in range(162)]
        for x in range(162):
            randomlyAssignSeat(unassignedSeats, Passengers, 
                               baggage, percentFast, randomiseBaggage)
            
    if Type == "Back-to-Front":
        for x in range(162):
            #Create the group
            if x % (162/3) == 0:
                rowSeats = [161 - y for y in range(x, x + (162//3))]
            #Randomly assign a seat from that group
            randomlyAssignSeat(rowSeats, Passengers, baggage, 
                               percentFast, randomiseBaggage)  
                
    if Type == "Front-to-Back":
        for x in range(162):
            if x % (162/3) == 0:
                rowSeats = [y for y in range(x, x + (162//3))]
            randomlyAssignSeat(rowSeats, Passengers, baggage, 
                               percentFast, randomiseBaggage)  
                
    if Type == "Outside-In":
        outsideSeats = [6*y - 1 for y in range(1, 162//6 + 1)] + [6*y for y in range(162//6)]
        middleSeats = [6*y - 2 for y in range(1, 162//6 + 1)] + [6*y + 1 for y in range(162//6)]
        insideSeats = [6*y - 3 for y in range(1, 162//6 + 1)] + [6*y + 2 for y in range(162//6)]
        seats = [outsideSeats, middleSeats, insideSeats]
        for group in seats:
            for x in range(162//3):
                randomlyAssignSeat(group, Passengers, baggage, 
                                   percentFast, randomiseBaggage)
            
    if Type == "Reverse-Pyramid":
        seats = reversePyramidGroups()
        for group in seats:
            for x in range(162//9):
                randomlyAssignSeat(group, Passengers, baggage, 
                                   percentFast, randomiseBaggage)
        
    return Passengers

"""
    Function that creates the groups needed for the reverse-pyramid method of boarding.
    Returns:
        List of groups from outside back to inside front
"""
def reversePyramidGroups():
    obs = list(set([6*y - 1 for y in range(1, 162//6 + 1) if y ] + [6*y for y in range(162//6)]) 
                            & set([161 - y for y in range(0,54)]))
    oms = list(set([6*y - 1 for y in range(1, 162//6 + 1)] + [6*y for y in range(162//6)])
                              & set([161 - y for y in range(54,108)]))
    ofs = list(set([6*y - 1 for y in range(1, 162//6 + 1)] + [6*y for y in range(162//6)])
                              & set([161 - y for y in range(108,162)]))
    
    mbs = list(set([6*y - 2 for y in range(1, 162//6 + 1)] + [6*y + 1 for y in range(162//6)])
                           & set([161 - y for y in range(0,54)]))
    mms = list(set([6*y - 2 for y in range(1, 162//6 + 1)] + [6*y + 1 for y in range(162//6)])
                             & set([161 - y for y in range(54,108)]))
    mfs = list(set([6*y - 2 for y in range(1, 162//6 + 1)] + [6*y + 1 for y in range(162//6)])
                            & set([161 - y for y in range(108,162)]))
    
    ibs = list(set([6*y - 3 for y in range(1, 162//6 + 1)] + [6*y + 2 for y in range(162//6)])
                           & set([161 - y for y in range(0,54)]))
    ims = list(set([6*y - 3 for y in range(1, 162//6 + 1)] + [6*y + 2 for y in range(162//6)])
                             & set([161 - y for y in range(54,108)]))
    ifs = list(set([6*y - 3 for y in range(1, 162//6 + 1)] + [6*y + 2 for y in range(162//6)])
                            & set([161 - y for y in range(108,162)]))
    return [obs,oms,ofs,mbs,mms,mfs,ibs,ims,ifs]

"""
    Randomly assigns a seats to a passenger from a group of seats.
    Parameters:
        Group : List(int)
            List of seats
        Passengers : List(Passenger)
            List of Passengers
        baggage : int
            Amount of baggage each passenger has
        percentFast : float
            Percentage of passengers that move quickly
        randomiseBaggage : Bool
            If True randomise the amount of baggage each passenger has from
            0 to baggage
            
"""
def randomlyAssignSeat(Group, Passengers, baggage, percentFast, randomiseBaggage):
    seat = random.choice(Group)
    number = random.random()
    if number < percentFast:
        walkingSpeed = 0
    else:
        number = random.random()
        if number < 0.7:
            walkingSpeed = 1
        else:
            walkingSpeed = 2
    if randomiseBaggage:
        baggage = random.randint(0,baggage)
    Group.remove(seat)
    if seat%6 < 3:
        Passengers.append(Passenger([seat//6 + 2, seat%6], baggage, walkingSpeed))
    else:
        Passengers.append(Passenger([seat//6 + 2, seat%6 + 1], baggage, walkingSpeed))
    return

"""
    Print the seats of Passengers.
    Parameters:
        Passengers : List(Passenger)
            List of Passengers
"""
def printPassengerSeats(Passengers):
    for passenger in Passengers:
        print(passenger.seat)
    return

"""
    Call this function to run the simulation.
    Parameters:
        Type : String
            Strategy type to use
        baggage : int
            Amount of baggage each passenger has
        enbleVariableWalkingSpeed : int
            Enable different walking speeds among passengers
        percentFast : float 
            Percentage of passengers that walk quickly
        randomiseBaggage : Bool
            If True randomise the amount of baggage each passenger has from
            0 to baggage
    Returns:
        Time steps taken for boaridng to complete
"""
def simulation(Type, baggage, percentFast, randomiseBaggage):
    #Matrix representing the plane
    #Middle column [3] is the aisle, while [0-2] and [4-6] are the seats
    #1 idencates that a person is there, 0 if not
    plane = [[0 for x in range(7)] for y in range(27)]
    
    #Add on the movement aisles
    plane.append([-1,-1,-1,0,-1,-1,-1])
    plane.append([-1,-1,-1,0,-1,-1,-1])
    plane.insert(0, [-1,-1,-1,0,-1,-1,-1])
    plane.insert(0, [-1,-1,-1,0,-1,-1,-1])
    
    #Create a list of passengers to board the plane
    #Assign them all a seat to go to
    Passengers = assignSeats(Type, baggage, percentFast, randomiseBaggage)
      
    #Create a full plane for ending the simulation
    fullPlane = [[1,1,1,0,1,1,1] for y in range(27)]
    fullPlane.append([-1,-1,-1,0,-1,-1,-1])
    fullPlane.append([-1,-1,-1,0,-1,-1,-1])
    fullPlane.insert(0, [-1,-1,-1,0,-1,-1,-1])
    fullPlane.insert(0, [-1,-1,-1,0,-1,-1,-1])
    
    #Main loop that runs till the plane is full
    OnBoardPassengers = []
    timeSteps = 0
    seatedPassengers = []
    unseatedPassengers = []
    stuckTimer = 0
    while plane != fullPlane:
        if enter(plane, Passengers):
            passenger = Passengers.pop(0)
            passenger.position = [0,3] 
            OnBoardPassengers.append(passenger)
        move(plane, OnBoardPassengers)
        oldplane = plane
        plane = updatePlane(plane, OnBoardPassengers)
        
        timeSteps += 1
        
        #Code that prints the plane layout if the simulation is stuck
        #This seems to be impossible, however I've keep it incase a 1/1000000
        #bug can occur.
        if oldplane == plane:
            stuckTimer -= 1
        else:
            stuckTimer = 0
        if stuckTimer == 100:
            printPlane(plane)
            print("Simulation is Stuck")
            break

        numSeated, numUnseated = numSeatedPassengers(OnBoardPassengers) 
        seatedPassengers.append(numSeated)
        unseatedPassengers.append(numUnseated)
    
    return timeSteps

"""
    Function that randomly generates a list of walking speeds for the 
    passengers.
    Parameters:
            percentFast : float (0,1)
                Percentage of passengers that walk quickly
    Returns:
        List of walking speeds
"""
def generateWalkingSpeeds(percentFast):
    walkingSpeeds = []
    for x in range(162):
        number = random.random()
        if number < percentFast:
            walkingSpeeds.append(0)
        else:
            number = random.random()
            if number < 0.7:
                walkingSpeeds.append(1)
            else:
                walkingSpeeds.append(2)
    return walkingSpeeds
    
"""
    Function for counting the number of passengers that are seated or not.
    Parameters:
        Passengers : List(Passenger)
            List of Passengers
    Returns:
        The number of seated and standing passengers
"""
def numSeatedPassengers(Passengers):
    numSeated = 0
    numUnseated = 0
    for passenger in Passengers:
        if passenger.reachedDest():
            numSeated += 1
        else:
            numUnseated += 1
    
    return numSeated, numUnseated

"""
    Function that prints the plane layout when called, along with row numbers.
    Parameters:
        plane : List(List(int))
            Layout of the plane
"""
def printPlane(plane):
    print("--------------------------------")
    for x in range(len(plane)):
        print(plane[x], x)
    print("--------------------------------")
    return
    
"""
    Function that updates the position of every passenger on the plane.
    If called after every move command as the current position of all 
    passenger can change after that command.
    Parameters:
        plane : List(List(int))
            Layout of the plane
        Passengers : List(Passenger)
            List of all Passengers on the plane
    Return:
        The new plane layout
"""
def updatePlane(plane, Passengers):
    #Reset plane
    plane = [[0 for x in range(7)] for y in range(27)]
    plane.append([-1,-1,-1,0,-1,-1,-1])
    plane.append([-1,-1,-1,0,-1,-1,-1])
    plane.insert(0, [-1,-1,-1,0,-1,-1,-1])
    plane.insert(0, [-1,-1,-1,0,-1,-1,-1])
    
    for passenger in Passengers:
        plane[passenger.getCurrRow()][passenger.getCurrColumn()] = 1
    return plane


"""
    Function that moves all passengers on the plane with respect to some rules.
    Parameters:
        plane : List(List(int))
            Layout of the plane
        Passengers : List(Passenger)
            List of all Passengers on the plane
"""
def move(plane, Passengers):
    for passenger in Passengers:
        #Wating passengers don't move
        if passenger.waiting == True:
            #Once moving passengers are in the aisle move normally
            if passenger.getWaitingOn(1).getCurrRow() == passenger.getWaitingOn(1).getRow() + 1:
                passenger.waiting = False
        
        #Move passengers need to move into the aisle and up one
        elif passenger.move == True:
            #Move out of seat
            if not (passenger.getMovingFor().getCurrRow() == passenger.getMovingFor().getRow()):
                if passenger.getCurrColumn() < 3:
                    passenger.moveRight(plane)
                elif passenger.getCurrColumn() > 3:
                    passenger.moveLeft(plane)
                elif passenger.getCurrRow() <= passenger.getRow() + 1:
                    passenger.moveUp(plane)
            else:
                #Move back into seat
                if passenger.getCurrRow() > passenger.getRow():
                    passenger.moveDown(plane)
                elif passenger.getCurrColumn() < passenger.getColumn():
                    passenger.moveRight(plane)
                elif passenger.getCurrColumn() > passenger.getColumn():
                    passenger.moveLeft(plane)
                else:
                    passenger.move = False
        elif passenger.reachedDest():
           continue
        else:
            #Normal move pattern
            if passenger.getCurrRow() < passenger.getRow():
                #Only move up if waiting or there are no moving passengers
                if passenger.getCurrRow() == (passenger.getRow() - 1) or \
                        not (checkPassengerMove(Passengers, [passenger.getCurrRow() + 1, 5])
                        or checkPassengerMove(Passengers, [passenger.getCurrRow() + 1, 1])
                        or checkPassengerMove(Passengers, [passenger.getCurrRow() + 1, 2])
                        or checkPassengerMove(Passengers, [passenger.getCurrRow() + 1, 4])
                        or checkPassengerMove(Passengers, [passenger.getCurrRow() + 2, 3])
                        or checkPassengerMove(Passengers, [passenger.getCurrRow() + 3, 3])):
                    passenger.moveUp(plane)
            else:
                if passenger.getCurrColumn() < passenger.getColumn():
                    passenger.moveRight(plane)
                if passenger.getCurrColumn() > passenger.getColumn():
                    passenger.moveLeft(plane)
            
            if passenger.getCurrRow() == (passenger.getRow() - 1):
                #Flags passengers that have to wait for other passengers to move
                if passenger.getColumn() == 0:
                    if passengerCheck(Passengers, [passenger.getRow(), 1], False):
                        flagPassengers([passenger.getRow(), 1], passenger, Passengers)
                    if passengerCheck(Passengers, [passenger.getRow(), 2], False):
                        flagPassengers([passenger.getRow(), 2], passenger,  Passengers)
                    if passengerSeatCheck(Passengers, [passenger.getRow(), 3], [passenger.getRow(), 1]):
                        flagPassengers([passenger.getRow(), 3], passenger,  Passengers)
                    if passengerSeatCheck(Passengers, [passenger.getRow(), 3], [passenger.getRow(), 2]):
                        flagPassengers([passenger.getRow(), 3], passenger,  Passengers)
                elif passenger.getColumn() == 1:
                    if passengerCheck(Passengers, [passenger.getRow(), 2], True):
                        flagPassengers([passenger.getRow(), 2], passenger,  Passengers)
                    if passengerSeatCheck(Passengers, [passenger.getRow(), 3], [passenger.getRow(), 2]):
                        flagPassengers([passenger.getRow(), 3], passenger,  Passengers)
                elif passenger.getColumn() == 6:
                    if passengerCheck(Passengers, [passenger.getRow(), 5], False):
                        flagPassengers([passenger.getRow(), 5], passenger,  Passengers)
                    if passengerCheck(Passengers, [passenger.getRow(), 4], False):
                        flagPassengers([passenger.getRow(), 4], passenger,  Passengers)
                    if passengerSeatCheck(Passengers, [passenger.getRow(), 3], [passenger.getRow(), 5]):
                        flagPassengers([passenger.getRow(), 3], passenger,  Passengers)
                    if passengerSeatCheck(Passengers, [passenger.getRow(), 3], [passenger.getRow(), 4]):
                        flagPassengers([passenger.getRow(), 3], passenger,  Passengers)
                elif passenger.getColumn() == 5:
                    if passengerCheck(Passengers, [passenger.getRow(), 4], True):
                        flagPassengers([passenger.getRow(), 4], passenger,  Passengers)
                    if passengerSeatCheck(Passengers, [passenger.getRow(), 3], [passenger.getRow(), 4]):
                        flagPassengers([passenger.getRow(), 3], passenger,  Passengers)
            
    return

"""
    Function that checks if the passenger at a given position is seating in
    a given position
    Parameters:
        Passengers : List(Passenger)
            List of on board passengers
        position : [int, int]
            Position to check
        seat : [int, int]
            Seat to check
    Return:
        True if passenger is in position and their seat is the same.
"""
def passengerSeatCheck(Passengers, position, seat):
    for passenger in Passengers:
        if passenger.position == position:
            if passenger.seat == seat:
                return True
    return False


"""
    Function that checks if a passenger is at a given position.
    Additionally, will check if the position is the seat of the passenger if
    needed.
    Parameters:
        Passengers : List(Passenger)
            List of on board passengers
        position : [int, int]
            Position to check
        checkSeat : Bool
            Check if the passenger is currently seated
    Return:
        True if passenger is in position, False otherwise
"""
def passengerCheck(Passengers, position, checkSeat):
    for passenger in Passengers:
        if passenger.position == position:
            if checkSeat:
                return passenger.seat == position
            else:
                return True
    return False


"""
    Function that checks if the passenger in a position is moving out of the
    way for another passenger.
    Parameters:
        Passengers : List(Passenger)
            List of on board passengers
        position : [int, int]
            Position to check
    Return:
        True if passenger in position is set to move, False otherwise
"""
def checkPassengerMove(Passengers, position):
    for passenger in Passengers:
        if passenger.position == position and passenger.move:
            return True
    return False

"""
    Function that flags the passenger in a given position as set to move
    for the given person passenger.
    Parameters:
        position : [int, int]
            Position to flag
        person : Passenger
            Passenger who is waiting
        Passengers : List(Passenger)
            List of on board passengers
"""
def flagPassengers(position, person, Passengers):
    person.waiting = True
    for passenger in Passengers:
        if passenger.position == position:
            passenger.move = True
            person.setWaitingOn(passenger)
            passenger.setMovingFor(person)
            return 
    return

"""
    Function that checks if a passenger can currently enter the plane.
    Parameters:
        plane : List(List(int))
            Layout of the plane
        Passengers : List(Passenger)
            List of all Passengers on the plane
    Return:
        True if the next passenger can enter the plane, False otherwise.
"""
def enter(plane, Passengers):
    if Passengers == []:
        return False
    if plane[0][3] == 0:
        plane[0][3] = 1
        return True
    return False

class Passenger:
    """
    This class represents a passenger for the plane.
    Attributes:
        seat : [int, int]
            The seat the passenger wishes to reach
        position : [int, int]
            The current position of the passenger
        waiting : Bool
            True if the passenger is waiting for someone to move out of the way
        waitingOn : [Passenger, Passenger]
            The passengers that a waiting passenger is waiting on
        move : Bool
            True if the passenger is moving for a waiting passenger
        movingFor : Passenger
            The passenger that a moving passenger is moving for
        baggage : int
            Amount of baggage each passenger has
        walkingSpeed : int
            The number of time steps taken to move one position
        walkingCooldown : int
            The number time steps until the passenger can walk again
    """
    
    def __init__(self, seat, baggage, walkingSpeed):
        self.seat = seat
        #Passengers not on the plane are at position [-1,-1]
        self.position = [-1,-1]
        self.waiting = False
        self.waitingOn = [0, 0]
        self.move = False
        self.movingFor = 0
        self.baggage = baggage
        self.walkingSpeed = walkingSpeed
        self.walkCooldown = 0
        
    def getRow(self):
        return self.seat[0]
    
    def getCurrRow(self):
        return self.position[0]
        
    def getColumn(self):
        return self.seat[1]
        
    def getCurrColumn(self):
        return self.position[1]
        
    def moveDown(self, plane):
        #Only move if the position to move to is free
        if plane[self.position[0] - 1][self.position[1]] == 0:
            if self.walkCooldown == 0:
                self.position[0] -= 1
                self.walkCooldown = self.walkingSpeed
            else:
                self.walkCooldown -= 1    

    def moveUp(self, plane):
        if plane[self.position[0] + 1][self.position[1]] == 0:
            if self.walkCooldown == 0:
                self.position[0] += 1
                self.walkCooldown = self.walkingSpeed
            else:
                self.walkCooldown -= 1   
        
    def moveLeft(self, plane):
        if self.baggage == 0:
            if plane[self.position[0]][self.position[1] - 1] == 0:
                if self.walkCooldown == 0:
                    self.position[1] -= 1
                    self.walkCooldown = self.walkingSpeed
                else:
                    self.walkCooldown -= 1   
        else:
            self.baggage -= 1
        
    def moveRight(self, plane):
        if self.baggage == 0:
            if plane[self.position[0]][self.position[1] + 1] == 0:
                if self.walkCooldown == 0:
                    self.position[1] += 1
                    self.walkCooldown = self.walkingSpeed
                else:
                    self.walkCooldown -= 1   
        else:
            self.baggage -= 1
        
    def setWaitingOn(self, Passenger):
        #If passenger if waiting on two people, then second one is the one in
        #the middle seat and first is the one in the aisle seat
        if self.waitingOn[1] != 0:
            self.waitingOn[0] = Passenger
        else:
            self.waitingOn[1] = Passenger
    
    def setMovingFor(self, Passenger):
        self.movingFor = Passenger
        
    def getWaitingOn(self, number):
        return self.waitingOn[number]
    
    def getMovingFor(self):
        return self.movingFor
    
    def reachedDest(self):
        return self.position == self.seat