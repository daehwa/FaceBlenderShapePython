import numpy as np
import matplotlib.pyplot as plt

def init_visualizer():
    global all_points
    fig = plt.figure("EtherMouth Mesh",figsize = (10,10))
    ax = fig.add_subplot(111, projection='3d')
    all_points, = ax.plot(np.zeros(8800),np.zeros(8800),np.zeros(8800),
                              '.',color='black',markersize=1)
    lip_points, = ax.plot(np.zeros(76),np.zeros(76),np.zeros(76),
                              '.',color='red',markersize=8)
    ax.set(xlim=(-10,10), ylim=(-10,10), zlim=(0,10))
    ax.grid(False)
    ax.view_init(elev=90+25, azim=0, roll=90)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    # Now set color to white (or whatever is "invisible")
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    ax.set_axis_off()

    # equal aspect ratio
    ax.set_box_aspect([ub - lb for lb, ub in (getattr(ax, f'get_{a}lim')() for a in 'xyz')])

    plotter = {
        'all': all_points,
        'lip': lip_points
    }

    return plotter

def visualize_keypoints(plotter, keypoints):
    plotter.set_xdata(keypoints[:,0])
    plotter.set_ydata(keypoints[:,1])
    plotter.set_3d_properties(keypoints[:,2])
    plt.pause(0.01)

