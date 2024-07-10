"Classes representing shuttle autopilot strategies"

import fixtures

class Shuttle:
    "Base class for all shuttle autopilots"

    def __init__(self, capacity, supply, dest):
        """
        Initialize autopilot for shuttle with capacity `capacity`
        using `SupplyCache` object `supply` and `DestinationCache`
        object `dest`.  Starts at position 0.
        """
        self.supply = supply  # Used to interact with supply cache at pos 0
        self.dest = dest  #  Used to interacrt with dest. cache at pos 9
        self.capacity = capacity # max material shuttle can hold
        self.stored = 0 # current amount stored by shuttle
        self.pos = 0 # position, an integer from 0 to 9 inclusive

    def available_capacity(self):

        """
        Return how much additional material the shuttle can take
        on right now.
        """
        return self.capacity - self.stored

    def update(self):
        """
        Simulate one minute of time, taking autopilot actions as
        appropriate.  This base class does nothing.  Subclasses
        are supposed to override this method to implement behavior.
        """
        pass

# subclasses
# -----------------------------------------------------------------------------------------------------------------------------
class BackForthShuttle(Shuttle):
    """ Represents a shuttle autopilot strategy that goes back and forth between supply and destination caches."""
    
    def __init__(self, capacity, supply, dest):
        """ 
        Initialize 'capacity', 'supply', and 'dest' using superclass. Starts with at position 0, and state at 'load'.
        """
        super().__init__(capacity, supply, dest)  
        self.state = "load"

    def update(self):
        """ 
        Accounts for one minute of simulated shuttle piloting. This class loads, move forwards, unloads, move backwards, and repeats.
        """
        if self.state == "load": #if state is loading
            if self.pos == 0:  # if shuttle is at  pos 0
                removed = self.supply.remove_material(self.available_capacity()) 
                self.stored += removed
                self.state = "forward" # chaneg state to moving forward
        elif self.state == "forward": # once states chnages to moving forward
            if self.pos < 9: # increment one step forward until pos is less than 9
                self.pos += 1
                if self.pos == 9:
                    self.state = "unload"
            else:
                self.state = "unload" #then change state to unloading
        elif self.state == "unload":
            if self.pos == 9: # if pos is at dest 
                # Unload material to destination cache
                added = self.dest.add_material(self.stored)
                self.stored -= added
                self.state = "backward"
        elif self.state == "backward":
            if self.pos > 0:
                self.pos -= 1
                if self.pos == 0:
                    self.state = "load"
            else :
                self.state = "load"
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
    
class ActOnOverflowShuttle(BackForthShuttle):
    """ 
    Represents a shuttle autopilot strategy waits at the supply until the supply becomes full, then it takes as much sand as possible
    to the destination and comes back.
    """

    def __init__(self, capacity, supply, dest):
        """ 
        Initialize 'capacity', 'supply', and 'dest' using superclass. Starts with at position 0, and state at 'wait'.
        """
        super().__init__(capacity, supply, dest)  
        self.state = "wait"

    def update(self):
        """ 
        Accounts for one minute of simulated shuttle piloting. This class waits, move forwards, unloads, move backwards, and repeats.
        """
        # when state is wait
        if self.state == "wait":
            # if at supply OR coming back to supply
            if self.pos == 0:
                # check is supply is sfull
                if self.supply.is_full():
                    # remove material from supply and store in shuttle
                    removed = self.supply.remove_material(self.available_capacity())
                    self.stored += removed
                    self.state = "forward"
                else:
                    self.state = "wait" #stay waiting until supply is full
        elif self.state == "forward":
            # move to dest if state is forward
            if self.pos < 9:
                self.pos += 1
                if self.pos == 9:
                    self.state = "unload"
            else:
                self.state = "unload"
        elif self.state == "unload":
            # once dest is reached unload material 
            if self.pos == 9:
                added = self.dest.add_material(self.stored)
                self.stored -= added 
                self.state = "backward" # update state to backward
        elif self.state == "backward":
            # move back to supply
            if self.pos > 0:
                self.pos -= 1
                if self.pos == 0:
                    self.state = "wait"
            else:
                self.state = "wait"
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
  
class ActOnUnderflowShuttle(BackForthShuttle):
    """ 
    Represents a shuttle autopilot strategy waits at the supply until the destination cache is empty and 
    the supply contains some sand. It then loads sand, takes it to the destination, and returns.
    """
    
    def __init__(self, capacity, supply, dest):
        """
        Initialize 'capacity', 'supply', and 'dest' using superclass. Starts with at position 0, and state at 'wait'.
        """
        super().__init__(capacity, supply, dest)
        self.state = "wait"
        
    def update(self):
        """ 
        Accounts for one minute of simulated shuttle piloting. This class waits, move forwards, unloads, move backwards, and repeats.
        """
        if self.state == "wait":
            if self.pos == 0:
            # waits until des is empty and supply had some sand
                if self.dest.is_empty() and not self.supply.is_empty():
                    removed = self.supply.remove_material(self.available_capacity())
                    self.stored += removed
                    self.state = "forward"
        # then move to des
        elif self.state == "forward":
            if self.pos < 9:
                self.pos += 1
                if self.pos == 9:
                    self.state = "unload"
            else:
                self.state = "unload"
        # unload material at des
        elif self.state == "unload":
            added = self.dest.add_material(self.stored)
            self.stored -= added
            if added > 0:
                self.state = "backward"
        #move back toward supply
        elif self.state == "backward":
            if self.pos > 0:
                self.pos -= 1
                if self.pos == 0:
                    self.state = "wait"
            else:
                self.state = "wait"