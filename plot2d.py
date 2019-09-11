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

        plot(time, axis_y, 'Time (s)', 'Z (m)', 'magenta', 'Gazebo', 'gazebo')

def plot(axis_x, axis_y, xlabel, ylabel, graph_color, graph_label, name):

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(axis_x, axis_y, color = graph_color, label = graph_label)
    plt.grid(True)
    plt.legend()
    plt.savefig(name, format = 'png')
    plt.show()
    plt.clf()


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
