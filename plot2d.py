import matplotlib.pyplot as plt
import csv
import numpy as np
import pylab

pylab.rcParams['figure.figsize'] = (8.0, 8.0)

def plot2d(fl1, fl2):
    
    for fl in [fl1, fl2]:
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

        displacement = get_offset(axis_x, axis_y, axis_z)

        print(f'len(time) = {len(time)}  len(x) = {len(axis_x)} :: len(y) = {len(axis_y)} :: len(z) = {len(axis_z)} :: len(offset) = {len(displacement)}')

        plot(time, axis_x, 'Time (s)', 'X (m)', 'magenta', 'Gazebo - X', 'gazebo_x')
        plot(time, axis_y, 'Time (s)', 'Y (m)', 'green', 'Gazebo - Y', 'gazebo_y')
        plot(time, axis_z, 'Time (s)', 'Z (m)', 'blue', 'Gazebo - Z', 'gazebo_z')
        plot(time, displacement, 'Time (s)', 'displacement (m)', 'green', 'Gazebo - Displacement', 'gazebo_displacement')

def plot(axis_x, axis_y, xlabel, ylabel, graph_color, graph_label, fig_name):

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(axis_x, axis_y, color = graph_color, label = graph_label)
    plt.grid(True)
    plt.legend()
    plt.savefig(fig_name, format = 'png')
    #plt.show()
    plt.clf()

    return

def get_offset(x, y, z):

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
    plot2d('cubo.txt')
