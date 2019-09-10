import matplotlib.pyplot as plt
import csv

def plot2d(fl):
    axis_x = []
    axis_y = []
    with open(fl) as csvfile:
        plots = csv.reader(csvfile, delimiter=' ')
        for row in plots:
            axis_y.append(row[0])
            axis_x.append(row[1])
    plt.plot(axis_x, axis_y)
    plt.savefig('./tracker/graph2d.png')

if __name__ == "__main__":
    plot2d('./tracker/points.txt')