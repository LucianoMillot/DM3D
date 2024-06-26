#This is the main class, that generates and .obj file for a power strip
#with the given parameters

#European and American power strip models are available
#For each plug, a model is available

#The power strip is generated by placing the plugs in the correct positions

import numpy as np
import matplotlib.pyplot as plt

#Here are the indices needed for connecting the plugs to the power strip
european_plug_vert_idx = [528, 527, 532, 530, 526, 525, 531, 529]
american_plug_vert_idx = [48, 50, 45, 46, 47, 49, 43, 44]

#Read the OBJ file
def read_obj(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('f '):
                face = line.strip().split()[1:]
                face_indices = []
                for vertex in face:
                    vertex_indices = vertex.split('/')
                    face_indices.append(int(vertex_indices[0]))
                faces.append(face_indices)
    return np.array(vertices), np.array(faces)

#Offset the vertices in space
def offset_vertices(vertices, offset):
    return vertices + offset

#When the power strip is generated, the indices of the faces need to be offset
#by the number of vertices in the power strip
def offset_indices_faces(faces, offset):
    faces_copy = faces.copy() #Make a copy of the faces, so the original is not modified
    for i in range(len(faces_copy)):
        for j in range(len(faces_copy[i])):
            faces_copy[i][j] += offset
    return faces_copy

# Plot the vertices
def plot_vertex(vertices):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the vertices
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2])

    # Set the aspect ratio of the plot
    max_range = np.array([vertices[:, 0].max()-vertices[:, 0].min(), vertices[:, 1].max()-vertices[:, 1].min(), vertices[:, 2].max()-vertices[:, 2].min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(vertices[:, 0].max()+vertices[:, 0].min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(vertices[:, 1].max()+vertices[:, 1].min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(vertices[:, 2].max()+vertices[:, 2].min())
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

# Plot vertex + faces
def plot_vertex_faces(vertices, faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the vertices
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2])

    # Faces are given as indices of the vertices to be connected
    for face in faces:
        face_vertices = vertices[face-1]
        face_vertices = np.concatenate((face_vertices, [face_vertices[0]]), axis=0)
        ax.plot(face_vertices[:, 0], face_vertices[:, 1], face_vertices[:, 2])

    # Set the aspect ratio of the plot
    max_range = np.array([vertices[:, 0].max()-vertices[:, 0].min(), vertices[:, 1].max()-vertices[:, 1].min(), vertices[:, 2].max()-vertices[:, 2].min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(vertices[:, 0].max()+vertices[:, 0].min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(vertices[:, 1].max()+vertices[:, 1].min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(vertices[:, 2].max()+vertices[:, 2].min())
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
#Add h-gap and v-gap
def generate_power_strip(num_plugs, plug_type, distance_between_plugs=5, lateral_gap=5, vertical_gap=5, visuliaze=False, path=''):

    if distance_between_plugs < 5 or distance_between_plugs > 60:
        raise ValueError('Invalid distance between plugs')
    
    if lateral_gap < 5 or lateral_gap > 25:
        raise ValueError('Invalid lateral gap')
    
    if vertical_gap < 5 or vertical_gap > 25:
        raise ValueError('Invalid vertical gap')
    
    # The actual distance we need for calculating the offset
    # is the distance between the plugs + the height of the plug
    # This constant is the height of the plug
    distance_between_plugs += 39.5

    # Read the OBJ file
    if plug_type == 'European':
        plug_vertices, plug_faces = read_obj('Plug models/European modified.obj')
        plug_vert_idx = european_plug_vert_idx
        plug_offset = -2.5
    elif plug_type == 'American':
        plug_vertices, plug_faces = read_obj('Plug models/American modified.obj')
        plug_vert_idx = american_plug_vert_idx
        plug_offset = 0
    else:
        raise ValueError('Invalid plug type')
    
    final_vertices = []
    final_faces = []
    prev_offset = np.array([lateral_gap, plug_offset, 45+vertical_gap])
    key_vertices_idx = None
    key_vertices_idx_next = None
    key_vertices_idx_next_bottom = None

    top_vertices_idx = [] #1-indexed due to OBJ file format
    bottom_vertices_idx = [] #1-indexed due to OBJ file format

    for _ in range(num_plugs):
        # Offset vertices
        plug_vertices = offset_vertices(plug_vertices, prev_offset)

        # Define key vertices and indices
        key_vertices = [[0, 0, 0], [lateral_gap, 0, 0], [lateral_gap+45, 0, 0], [2*lateral_gap+45, 0, 0]]
        key_vertices += [[0, 5, 0], [lateral_gap, 5, 0], [lateral_gap+45, 5, 0], [2*lateral_gap+45, 5, 0]]
        if _ == 0:
            final_vertices.extend(key_vertices)

        # Add additional vertices for each plug, top side
        final_vertices.extend([[0, 0, 45 + vertical_gap + distance_between_plugs * _], [2*lateral_gap+45, 0, 45 + vertical_gap + distance_between_plugs * _]])

        # Update key vertices indices, top side
        if _ == 0:
            key_vertices_idx = [1, 2, 3, 4]
            key_vertices_idx.extend([len(final_vertices) - 1, len(final_vertices)])
            top_vertices_idx.extend(key_vertices_idx)
        else:
            key_vertices_idx = key_vertices_idx_next
            key_vertices_idx.extend([len(final_vertices) - 1, len(final_vertices)])
            top_vertices_idx.extend(key_vertices_idx[4:6])   

        # Start preparing for the next iteration
        key_vertices_idx_next = [len(final_vertices)-1, 0, 0, len(final_vertices)]

        # Add additional vertices for each plug, bottom side
        final_vertices.extend([[0, 5, 45 + vertical_gap + distance_between_plugs * _], [2*lateral_gap+45, 5, 45 + vertical_gap + distance_between_plugs * _]])

        # Update key vertices indices, bottom side
        if _ == 0:
            key_vertices_idx.extend([5, 6, 7, 8])
            key_vertices_idx.extend([len(final_vertices) - 1, len(final_vertices)])
            bottom_vertices_idx.extend(key_vertices_idx[6:])
        else:
            key_vertices_idx.extend(key_vertices_idx_next_bottom)
            key_vertices_idx.extend([len(final_vertices) - 1, len(final_vertices)])
            bottom_vertices_idx.extend(key_vertices_idx[10:12])

        # Continue preparing for the next iteration
        key_vertices_idx_next_bottom = [len(final_vertices)-1, 0, 0, len(final_vertices)]

        # Offset and add vertices and faces
        vertex_offset = len(final_vertices)
        final_vertices.extend(plug_vertices)
        final_faces.extend(offset_indices_faces(plug_faces, vertex_offset))

        # Define new faces, top side
        new_faces = [
            [key_vertices_idx[0], plug_vert_idx[0] + vertex_offset, key_vertices_idx[4]],
            [key_vertices_idx[0], key_vertices_idx[1], plug_vert_idx[0] + vertex_offset],
            [plug_vert_idx[0] + vertex_offset, plug_vert_idx[1] + vertex_offset, key_vertices_idx[4]],
            [key_vertices_idx[1], plug_vert_idx[2] + vertex_offset, plug_vert_idx[0] + vertex_offset],
            [key_vertices_idx[2], plug_vert_idx[2] + vertex_offset, key_vertices_idx[1]],
            [key_vertices_idx[3], plug_vert_idx[2] + vertex_offset, key_vertices_idx[2]],
            [key_vertices_idx[3], key_vertices_idx[5], plug_vert_idx[2] + vertex_offset],
            [key_vertices_idx[5], plug_vert_idx[3] + vertex_offset, plug_vert_idx[2] + vertex_offset]
        ]
        final_faces.extend(new_faces)

        # Define new faces, bottom side
        new_faces = [
            [key_vertices_idx[6], key_vertices_idx[10], plug_vert_idx[4] + vertex_offset],
            [key_vertices_idx[6], plug_vert_idx[4] + vertex_offset, key_vertices_idx[7]],
            [key_vertices_idx[10], plug_vert_idx[5] + vertex_offset, plug_vert_idx[4] + vertex_offset],
            [key_vertices_idx[7], plug_vert_idx[4] + vertex_offset, plug_vert_idx[6] + vertex_offset],
            [key_vertices_idx[7], plug_vert_idx[6] + vertex_offset, key_vertices_idx[8]],
            [key_vertices_idx[8], plug_vert_idx[6] + vertex_offset, key_vertices_idx[9]],
            [key_vertices_idx[9], plug_vert_idx[6] + vertex_offset, key_vertices_idx[11]],
            [plug_vert_idx[6] + vertex_offset, plug_vert_idx[7] + vertex_offset, key_vertices_idx[11]]
        ]
        final_faces.extend(new_faces)

        # Update previous offset for next iteration
        prev_offset = np.array([0, 0, distance_between_plugs])
        key_vertices_idx_next[1] = plug_vert_idx[1] + vertex_offset
        key_vertices_idx_next[2] = plug_vert_idx[3] + vertex_offset
        key_vertices_idx_next_bottom[1] = plug_vert_idx[5] + vertex_offset
        key_vertices_idx_next_bottom[2] = plug_vert_idx[7] + vertex_offset

    # Close the power strip
    #Key for top side
    key_vertices_idx = [len(final_vertices)-2 - len(plug_vertices) - 1] + \
                       [plug_vert_idx[1] + vertex_offset, plug_vert_idx[3] + vertex_offset] + \
                       [len(final_vertices)-2 - len(plug_vertices)]
    final_vertices.extend([[0, 0, distance_between_plugs * num_plugs + 2 * vertical_gap - 15], [2*lateral_gap+45, 0, distance_between_plugs * num_plugs + 2 * vertical_gap - 15]])
    key_vertices_idx.extend([len(final_vertices) - 1, len(final_vertices)])

    top_vertices_idx.extend([key_vertices_idx[0], key_vertices_idx[3], key_vertices_idx[4], key_vertices_idx[5]])
    #Key for bottom side
    key_vertices_idx += [len(final_vertices)-2 - len(plug_vertices) - 1] + \
                              [plug_vert_idx[5] + vertex_offset, plug_vert_idx[7] + vertex_offset] + \
                              [len(final_vertices)-2 - len(plug_vertices)]
    final_vertices.extend([[0, 5, distance_between_plugs * num_plugs + 2 * vertical_gap - 15], [2*lateral_gap+45, 5, distance_between_plugs * num_plugs + 2 * vertical_gap - 15]])
    key_vertices_idx.extend([len(final_vertices) - 1, len(final_vertices)])

    bottom_vertices_idx.extend([key_vertices_idx[6], key_vertices_idx[9], key_vertices_idx[10], key_vertices_idx[11]])

    # Top side
    new_faces = [
        [key_vertices_idx[0], key_vertices_idx[1], key_vertices_idx[4]],
        [key_vertices_idx[1], key_vertices_idx[2], key_vertices_idx[4]],
        [key_vertices_idx[2], key_vertices_idx[5], key_vertices_idx[4]],
        [key_vertices_idx[2], key_vertices_idx[3], key_vertices_idx[5]]
    ]
    final_faces.extend(new_faces)

    # Bottom side
    new_faces = [
        [key_vertices_idx[6], key_vertices_idx[10], key_vertices_idx[7]],
        [key_vertices_idx[7], key_vertices_idx[10], key_vertices_idx[8]],
        [key_vertices_idx[8], key_vertices_idx[10], key_vertices_idx[11]],
        [key_vertices_idx[8], key_vertices_idx[11], key_vertices_idx[9]]
    ]
    final_faces.extend(new_faces)

    # Lateral faces

    # Flatten and order the lists
    top_vertices_idx = list(set(top_vertices_idx))
    bottom_vertices_idx = list(set(bottom_vertices_idx))
    top_vertices_idx.sort()
    bottom_vertices_idx.sort()

    # Z-
    new_faces = [[top_vertices_idx[0], bottom_vertices_idx[0], top_vertices_idx[1]],
                 [top_vertices_idx[1], bottom_vertices_idx[0], bottom_vertices_idx[1]],
                 [top_vertices_idx[1], bottom_vertices_idx[1], top_vertices_idx[2]],
                 [top_vertices_idx[2], bottom_vertices_idx[1], bottom_vertices_idx[2]],
                 [top_vertices_idx[2], bottom_vertices_idx[2], top_vertices_idx[3]],
                 [top_vertices_idx[3], bottom_vertices_idx[2], bottom_vertices_idx[3]]
                 ]
    final_faces.extend(new_faces)

    # Z+
    new_faces = [[top_vertices_idx[len(top_vertices_idx)-2], top_vertices_idx[len(top_vertices_idx)-1], bottom_vertices_idx[len(bottom_vertices_idx)-1]],
                 [bottom_vertices_idx[len(bottom_vertices_idx)-2], top_vertices_idx[len(top_vertices_idx)-2], bottom_vertices_idx[len(bottom_vertices_idx)-1]]
                ]
    final_faces.extend(new_faces)

    #Remove initial vertices not taking part anymore
    #This way the data is cleaner for the algorithm
    top_vertices_idx.remove(2)
    top_vertices_idx.remove(3)
    bottom_vertices_idx.remove(6)
    bottom_vertices_idx.remove(7)
    
    # X-
    for i in range(0, len(top_vertices_idx)-2, 2):
        new_faces = [[top_vertices_idx[i], top_vertices_idx[i+2], bottom_vertices_idx[i]],
                     [bottom_vertices_idx[i+2], bottom_vertices_idx[i], top_vertices_idx[i+2]]
                    ]
        final_faces.extend(new_faces)

    # X+
    for i in range(1, len(top_vertices_idx)-1, 2):
        new_faces = [[top_vertices_idx[i], bottom_vertices_idx[i], top_vertices_idx[i+2]],
                     [bottom_vertices_idx[i], bottom_vertices_idx[i+2], top_vertices_idx[i+2]]
                    ]
        final_faces.extend(new_faces)
    
    # Convert final_vertices and final_faces to NumPy arrays
    final_vertices = np.array(final_vertices)
    final_faces = np.array(final_faces)

    # Plot the vertices and faces
    if visuliaze:
        plot_vertex_faces(final_vertices,final_faces)

    # Write the OBJ file
    with open(path + 'output_top.obj', 'w') as file:
        for vertex in final_vertices:
            file.write('v ' + ' '.join(map(str, vertex)) + '\n')
        for face in final_faces:
            file.write('f ' + ' '.join(map(str, face)) + '\n')

def generate_bottom_enclousure(num_plugs, lateral_gap, vertical_gap, distance_between_plugs, path):
    
    #Open the power strip file
    with open('Plug models/Bottom_enclosure.obj', 'r') as file:
        power_strip = file.readlines()

        #Substitute the length and witdh of the power strip
        #If line begins with v, it is a vertex
        #Any vertex with value 20 is the length of the power strip
        #Also take into account the inner gap
        for i in range(len(power_strip)):
            if power_strip[i].startswith('v '):
                power_strip[i] = power_strip[i].replace('20.', str(2*vertical_gap + num_plugs*(distance_between_plugs+45) - distance_between_plugs) + '.')
                power_strip[i] = power_strip[i].replace('17.', str(2*vertical_gap + num_plugs*(distance_between_plugs+45) - distance_between_plugs - 3) + '.')
                power_strip[i] = power_strip[i].replace('-10.', str(-(2*lateral_gap+45)) + '.')
                power_strip[i] = power_strip[i].replace('-7.', str(-(2*lateral_gap+42)) + '.')


        with open(path + 'output_bottom.obj', 'w') as file:
            for line in power_strip:
                file.write(line)

if __name__ == '__main__':
    generate_power_strip(num_plugs=2, plug_type='American',lateral_gap=15, vertical_gap=25, distance_between_plugs=25)
    generate_bottom_enclousure(num_plugs=2, lateral_gap=15, vertical_gap=25, distance_between_plugs=25)
