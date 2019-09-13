import matplotlib.pyplot as plt
import csv
import numpy as np
import pylab

# window size
pylab.rcParams['figure.figsize'] = (8.0, 8.0)

# open a archive with points(t, x(t), y(t), z(t))
def plot2d(fl1, fl2):
    
    # parameters of each graph
    parameters = [('magenta', 'Gazebo - X(t)', 'gazebo_x'), ('green', 'Gazebo - Y(t)', 'gazebo_y'), ('blue', 'Gazebo - Z(t)', 'gazebo_z'), ('yellow', 'Gazebo - Displacement(t)', 'gazebo_displacement'),  \
                  ('cyan', 'Real - X(t)', 'real_x')  , ('red', 'Real - Y(t)', 'real_y') , ('coral', 'Real - Z(t)', 'real_z'), ('chocolate', 'Real - Displacement(t)', 'real_displacement')]

    index = 0

    for fl in [fl1, fl2]:
        print(index)
        axis_x = []
        axis_y = []
        axis_z = []
        time   = []

        with open(fl) as csvfile:
            plots = csv.reader(csvfile, delimiter=' ')

            for row in plots:
                time.append(float(row[0]))
                axis_x.append(float(row[1]))
                axis_y.append(float(row[2]))
                axis_z.append(float(row[3]))

        # get displacement from trajectory
        displacement = get_offset(axis_x, axis_y, axis_z)

        #print(f'len(time) = {len(time)}  len(x) = {len(axis_x)} :: len(y) = {len(axis_y)} :: len(z) = {len(axis_z)} :: len(offset) = {len(displacement)}')

        plot(time, axis_x, 'Time (s)', 'X (mm)', parameters[index])
        plot(time, axis_y, 'Time (s)', 'Y (mm)', parameters[index + 1])
        plot(time, axis_z, 'Time (s)', 'Z (mm)', parameters[index + 2])
        plot(time, displacement, 'Time (s)', 'Displacement (mm)', parameters[index + 3])

        index += 4

# ploting a graph 2D 
def plot(axis_x, axis_y, xlabel, ylabel, parameters):

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(axis_x, axis_y, color = parameters[0], label = parameters[1])
    plt.grid(True)
    plt.legend()
    plt.savefig(parameters[2], format = 'png')
    plt.show()
    plt.clf()

    return

# get the displacement of a cube from own trajectory
def get_offset(x, y, z):

    # displacement x time
    displacement = []
    displacement.append(0)

    for i in range(1, len(x)):
        offset  = pow(x[i] - x[i-1], 2)
        offset += pow(y[i] - y[i-1], 2)
        offset += pow(z[i] - z[i-1], 2)

        offset  = np.sqrt(offset)

        displacement.append(offset)

    return displacement

if __name__ == "__main__":
    plot2d('cubo.txt', 'cubinho.txt')
