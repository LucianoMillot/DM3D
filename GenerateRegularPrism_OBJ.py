import numpy as np
import matplotlib.pyplot as plt

# Regular polygon parameters
p = np.array([0, 0, 5])  # X Y Z Translation
r = 2.5  # Radius
h = 1  # Height
n = 5  # Number of sides
alpha, beta, gamma = 0, 0, 0  # Rotation on the three axes, in degrees

# Rotation matrix and translation
def euler2rot(alpha, beta, gamma):
    """
    Convert Euler angles to rotation matrix.
    """
    alpha_rad = np.radians(alpha)
    beta_rad = np.radians(beta)
    gamma_rad = np.radians(gamma)

    rot_x = np.array([[1, 0, 0],
                      [0, np.cos(alpha_rad), -np.sin(alpha_rad)],
                      [0, np.sin(alpha_rad), np.cos(alpha_rad)]])
    rot_y = np.array([[np.cos(beta_rad), 0, np.sin(beta_rad)],
                      [0, 1, 0],
                      [-np.sin(beta_rad), 0, np.cos(beta_rad)]])
    rot_z = np.array([[np.cos(gamma_rad), -np.sin(gamma_rad), 0],
                      [np.sin(gamma_rad), np.cos(gamma_rad), 0],
                      [0, 0, 1]])

    return np.dot(rot_z, np.dot(rot_y, rot_x))

rot = euler2rot(alpha, beta, gamma)
trans = p

# Create the empty tables
edges = []
vertices = []

# Initializing some variables
closed = False  # Indicates whether we have finished generating our polygon
i = 0  # Current iteration
ang_step = 360 / n  # Angle for each portion of the polygon

# Generating the first pair of vertices (Vi, Vi+1)
vertices.append([r * np.cos(np.radians(ang_step * i)),
                 r * np.sin(np.radians(ang_step * i)),
                 0])
vertices.append([r * np.cos(np.radians(ang_step * i)),
                 r * np.sin(np.radians(ang_step * i)),
                 h])
i += 1

while not closed:
    # Generate the vertical edge connecting the last iteration vertices
    edges.append([len(vertices)-2, len(vertices)-1])
    # Generate the new pair of vertices at a given position
    vertices.append([r * np.cos(np.radians(ang_step * i)),
                     r * np.sin(np.radians(ang_step * i)),
                     0])
    vertices.append([r * np.cos(np.radians(ang_step * i)),
                     r * np.sin(np.radians(ang_step * i)),
                     h])
    # Create the edges connecting the last vertices horizontally with their predecessors
    edges.append([len(vertices)-4, len(vertices)-2])
    edges.append([len(vertices)-3, len(vertices)-1])

    i += 1
    # If we end up where we started...
    if ang_step * i >= 360:
        # Just finish by connecting the last iteration vertices
        edges.append([len(vertices)-2, len(vertices)-1])
        edges.append([len(vertices)-1, 1])  # Connect last vertex to the second vertex
        edges.append([len(vertices)-2, 0])  # Connect second-to-last vertex to the first vertex
        closed = True

# Apply the rot and trans matrices to the vertices
vertices = np.array(vertices)
for i in range(len(vertices)):
    vertices[i, :3] = np.dot(rot, vertices[i, :3]) + trans

# Print the vertices and edges tables
print("Vertices: ", vertices)
print("Edges: ", edges)

# Represent the model
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for edge in edges:
    ax.plot3D([vertices[edge[0], 0], vertices[edge[1], 0]],
              [vertices[edge[0], 1], vertices[edge[1], 1]],
              [vertices[edge[0], 2], vertices[edge[1], 2]], 'b')
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([0, 10])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
