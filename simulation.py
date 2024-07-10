"Basic simulation to test shuttle autopilot"

import monorail.shuttle as shuttle
import fixtures
import monorail.tui as tui

# Make the supply cache, capacity 900
sc = fixtures.SupplyCache(500)

# Make the destination cache, capacity 500
dc = fixtures.DestinationCache(200)

# Make the shuttle autopilot for a shuttle with
# capacity 200 
S = shuttle.Shuttle(0, sc, dc)

# subclass:
S = shuttle.BackForthShuttle(300, sc, dc)
#S = shuttle.ActOnOverflowShuttle(200, sc, dc)
#S = shuttle.ActOnUnderflowShuttle(200, sc, dc)

# Fill the supply with sand (starts empty by default)
sc.stored = sc.capacity

# Clear terminal (scroll up 60 lines)
print("\n" * 60)

t = 0  # Tracks simulation time

# Main simulation loop runs forever
# (control-C or option-. to quit)
while True:
    print("State at time t={}:".format(t))
    tui.show(sc, dc, S)  # Display current situation
    print("\n" * 3)
    input("Press Enter to advance simulation")
    print("\n" * 60)
    S.update()
    t += 1
