# Import necessary libraries
import numpy as np                      # For numerical operations and arrays
import matplotlib.pyplot as plt         # For plotting
import matplotlib.animation as animation  # For creating animations


g = 9.81            # Acceleration due to gravity (m/s^2)
mass = 0.1          # Mass of the projectile (kg)
k = 0.05            # Air resistance coefficient (kg/m)
v0 = 20             # Initial velocity magnitude (m/s)
theta = 45          # Launch angle (degrees)

theta_rad = np.radians(theta)  # Convert angle to radians
vx0 = v0 * np.cos(theta_rad)   # Initial horizontal velocity
vy0 = v0 * np.sin(theta_rad)   # Initial vertical velocity

dt = 0.01          # Time step (seconds)
t_max = 5          # Maximum simulation time
n = int(t_max / dt)  # Number of time steps

x = np.zeros(n)    # Horizontal position array
y = np.zeros(n)    # Vertical position array
vx = np.zeros(n)   # Horizontal velocity array
vy = np.zeros(n)   # Vertical velocity array

x[0] = 0           # Initial x position
y[0] = 0           # Initial y position
vx[0] = vx0        # Initial x velocity
vy[0] = vy0        # Initial y velocity


# NUMERICAL INTEGRATION (Euler Method)


for i in range(1, n):
    v = np.sqrt(vx[i-1]**2 + vy[i-1]**2)  # Speed magnitude at previous step

    # Acceleration components including air resistance
    ax = -k * v * vx[i-1] / mass
    ay = -g - (k * v * vy[i-1]) / mass

    # Velocity update
    vx[i] = vx[i-1] + ax * dt
    vy[i] = vy[i-1] + ay * dt

    # Position update
    x[i] = x[i-1] + vx[i-1] * dt
    y[i] = y[i-1] + vy[i-1] * dt

    # Stop the loop when the projectile hits the ground (y < 0)
    if y[i] < 0:
        x = x[:i+1]
        y = y[:i+1]
        break


fig, ax = plt.subplots()                     # Create figure and axis
ax.set_xlim(0, max(x) * 1.1)                 # Set x-axis limits a bit beyond max x
ax.set_ylim(0, max(y) * 1.1)                 # Set y-axis limits a bit beyond max y
line, = ax.plot([], [], 'y--', lw=2)          # Line object for trajectory path
point, = ax.plot([], [], 'ro')               # Red dot to show moving projectile

# Add labels and title
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Projectile Motion with Air Resistance')
plt.grid()


def init():
    line.set_data([], [])      # Clear the line
    point.set_data([], [])     # Clear the dot
    return line, point

def update(frame):
    line.set_data(x[:frame], y[:frame])      # Update trajectory line
    point.set_data(x[frame-1], y[frame-1])   # Move red dot to current position
    return line, point


ani = animation.FuncAnimation(
    fig,               # Figure to animate
    update,            # Function to call for each frame
    frames=len(x),     # Total number of frames
    init_func=init,    # Initialization function
    blit=True,         # Redraw only the changed parts
    interval=dt*1000,  # Interval between frames in ms
    repeat=True      # Do not loop
)

# Set background and foreground colors
fig.patch.set_facecolor('black')       # Figure background
ax.set_facecolor('black')              # Axes background

# Change spine, tick, label, and title colors to white
ax.tick_params(colors='white')                     # Tick labels
ax.xaxis.label.set_color('white')                  # X-axis label
ax.yaxis.label.set_color('white')                  # Y-axis label
ax.title.set_color('white')                        # Title

# Change spine colors (borders of plot area)
for spine in ax.spines.values():
    spine.set_color('white')

# Optionally: white grid lines
ax.grid(True, color='gray')  # You can also use 'white' or lighter gray

plt.show()
