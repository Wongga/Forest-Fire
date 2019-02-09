import pylab as plt
import matplotlib as mpl
import scipy as sp
import random as rd
import copy as cp
import time as tm


cdict = {
      'red'  :  ( (0.0, 1.0, 1.0),
                  (0.3, 0.0, 0.0),
                  (0.6, 255./256, 255./256),
                  (1.0, 0.0, 0.0)),

      'green':  ( (0.0, 1.0, 1.0),
                  (0.3, 1.0, 1.0),
                  (0.6, 160./256, 160./256),
                  (1.0, 0.0, 0.0)),
                  
      'blue' :  ( (0.0, 1.0, 1.0),
                  (0.3, 0.0, 0.0),
                  (0.6, 0.0, 0.0),
                  (1.0, 0.0, 0.0))
            }
cm = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)

empty, tree, fire, charred = range(4)

plt.ion()

fig1 = plt.figure(num=1)

fig1.clear()
plt.show()
fig1.canvas.draw()
fig1.canvas.flush_events()


count_states(matrix)
current_counts = count_states(matrix)

def count_states(matrix_):
    
    # Create a list to store the counts of each type of cell:
    counts = [0,0,0,0]
    
    # This line works out the dimensions of the forest:
    w,h = sp.shape(matrix_)
    
    for y in range(h):
        for x in range(w):

            state = matrix_[x,y]
            
            counts[int(state)] = counts[int(state)] + 1
    
    print()
    print("empty: " + str(counts[0]))
    print("tree: " + str(counts[1]))
    print("fire: " + str(counts[2]))
    print("charred: " + str(counts[3]))
    print()
    
    # This last line would allow you to work with the counts in Python after running the simulation...
    # ... but if you're not familiar with Python, you can ignore it (or even remove it).
    return list(counts)

def visualise(figure,matrix,time):
    
    # Set the figure we're working on:
    figure
    
    # Clear whatever was on the plot before:
    plt.cla()
    
    # Draw the forest:
    plt.pcolor(matrix.T, vmin=0, vmax=3, cmap=cm)

    # Set the scale of x and y as equal:
    plt.axis('square')

    # Present the iteration number in the title:
    plt.title('time = ' + str(time))
    
    # Save the figure as a .png file:
    #plt.savefig(name + '_' + str(time) + '.png')

    # Update the plot on the screen:
    figure.canvas.draw()
    figure.canvas.flush_events()

# Choose length of simulation:
maxTime = 100

# Set the size of the region:
width = 50
height = 50

name = 'forestpic'

# Choose the density of the forest:
# ... the probability that each cell will have a tree.]
ptree = 0.7

# The next two parameters control the speed of the simulation.

# Choose an initial delay (in seconds) before the simulation starts:
initial_delay = 2

# And set a minimum time interval (in seconds) between frames:
time_between_frames = 0.2


# This line creates an empty grid to represent the forest:
matrix = sp.zeros([width, height])

# We will actually create a copy of this so that...
# ... the initial state is not lost when we start the simulation:
initial_forest = cp.copy(matrix)


# CREATING THE TREES
# Go through the cells from left to right:
for x in range(width):

    # And from top to bottom:
    for y in range(height):

        # Pick a random number:
        random = rd.random()

        if random < ptree:
            matrix[x,y] = tree

           
# ******************** THE SIMULATION ******************** #

# Make a copy of the forest matrix...
# This will be used to work out the new configuration.
newmatrix = cp.copy(matrix)

# Show the initial state of the forest:
visualise(fig1,matrix,'initial')

# Save an image of the initial state of the forest:
plt.savefig(name + '_initial.png')

# Start the fire at a random location!
matrix[rd.randint(0,width-1), rd.randint(0,height-1)] = fire

# Wait for the specified time delay:
tm.sleep(initial_delay)

# Start the timer
for time in range(maxTime):

    # Draw the picture:
    visualise(fig1,matrix,time)
    
    # Look at each cell in turn starting at the bottom:
    for y in range(height):
        
        # And going from left to right:
        for x in range(width):

            # First check the state of the cell:
            state = matrix[x,y]

            # There are only two ways that the state can change

            # 1) If the cell is on fire, we need to change the state to charred:
            if state == fire:
                state = charred

            # 2) If the cell contains a tree, we need to check the neighbouring cells
            # to see whether any of them are on fire:
            if state == tree:
                
                # Looking left and right:
                for dx in [-1,0,1]:
                    
                    # And up and down:
                    for dy in [-1,0,1]:
                        
                        # Are any of the neighbours on fire?
                        if matrix[(x+dx)%width, (y+dy)%height] == fire:
                            
                            # If so, our tree catches fire:
                            state = fire
            
            # Now we update the cell that we are looking at with the new state:    
            newmatrix[x,y] = state
        
 
    matrix, newmatrix = newmatrix, matrix
    
    # Finally, apply the time delay:
    tm.sleep(time_between_frames)

visualise(fig1,matrix,maxTime)

plt.savefig(name + '_final.png')

