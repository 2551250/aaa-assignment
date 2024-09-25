import numpy as np

# Role assigment function
def role_assignment(teammate_positions, formation_positions): 
    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    #-----------------------------------------------------------#
    n = len(formation_positions)
    cost_matrix = create_cost_matrix(n, teammate_positions, formation_positions)
    cost_matrix = subtract_row_minimum(cost_matrix)
    cost_matrix = subtract_column_minimum(cost_matrix)
    cost_matrix = optimize(cost_matrix)
    point_preferences = optimal_assignment(cost_matrix, formation_positions)
    return point_preferences


# Creates initial cost_matrix
def create_cost_matrix(n, teammate_positions, formation_positions):
    cost_matrix = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            cost_matrix[i][j] = euclidean_distance(teammate_positions[i], formation_positions[j])
    return cost_matrix


# Repeatedly covers zeros and and adjusts matrix until optimal solution found
def optimize(cost_matrix):
    n = len(cost_matrix)
    num_lines = 0
    num_lines, row_cover, col_cover = cover_zeros(cost_matrix)
    while(num_lines < n):
        cost_matrix = adjust_matrix(cost_matrix, row_cover, col_cover)
        num_lines, row_cover, col_cover = cover_zeros(cost_matrix)
    return cost_matrix


# Subtracts the minimum from each row
def subtract_row_minimum(cost_matrix):
    n = len(cost_matrix)
    for i in range(0, n):
        min = np.min(cost_matrix[i, :])
        cost_matrix[i, :] = cost_matrix[i, :] - min * np.ones((n))
    return cost_matrix


# Subtracts the minimum from each column
def subtract_column_minimum(cost_matrix):
    n = len(cost_matrix)
    for j in range(0, n):
        min = np.min(cost_matrix[:, j])
        cost_matrix[:, j] = cost_matrix[:, j] - min * np.ones((1, n))
    return cost_matrix


# Covers the zeros with the least number of lines
def cover_zeros(cost_matrix):
    # Greedy algorithm does not work in all cases
    n = len(cost_matrix)
    copy = np.copy(cost_matrix)
    row_cover = np.zeros(n)
    col_cover = np.zeros(n)

    # For each row, mark (with -1) an arbitray zero such that assignments do not overlap 
    for i in range(n):
        for j in range(n):
            if copy[i][j] == 0 and col_cover[j] == 0 and row_cover[i] == 0:
                copy[i][j] = -1
                col_cover[j] = 1
                row_cover[i] = 1
                break

    # Clear covered rows and columns
    for i in range(n):
        row_cover[i] = 0
        col_cover[i] = 0

    # Cover all columns containing a marked zero (-1)
    for i in range(n):
        for j in range(n):
            if copy[i][j] == -1:
                col_cover[j] = 1

    while(True):
        found = True
        row = -1
        col = -1
        i = 0
        # Find new non-covered zero and mark it with -2
        while (i < n and row == -1):
            for j in range(n):
                if copy[i][j] == 0 and row_cover[i] == 0 and col_cover[j] == 0:
                    found = False
                    copy[i][j] = -2
                    row = i
                    col = j
                    break
            i+= 1
        
        # All zeros covered so we have reached the optimal solution
        if found:
            break

        skip = False
        # If current zero (marked with -2) is on same row as marked zero (-1), cover the row and uncover column
        for j in range(n):
            if copy[row][j] == -1:
                row_cover[row] = 1
                col_cover[j] = 0
                skip = True

        # Do not perform if row and column swapped
        # We find a new way to mark the current (-2) zero
        path = [[row, col]]
        if not skip:
            while(True):
                flag = False
                # Find a zero marked with -1 in the current column 
                for i in range(n):
                    if copy[i, col] == -1:
                        row = i
                        flag = True
                
                if not flag:
                    break

                path.append([row, col])
                # Find a zero marked with -2 in the current row
                for i in range(n):
                    if copy[row, i] == -2:
                        col = i
                
                # Add all zeros encountered to the path
                path.append([row, col])

            # For each zero in the path, replace -2 with -1 and -1 with 0
            # i.e. try this new solution
            for point in path:
                if copy[point[0], point[1]] == -2:
                    copy[point[0], point[1]] = -1
                else:
                    copy[point[0], point[1]] = 0
            
            # Uncover all rows and columns and replace all -2 with 0
            for i in range(n):
                for j in range(n):
                    if copy[i][j] == -2:
                        copy[i][j] = 0
                row_cover[i] = 0
                col_cover[i] = 0

            # Cover all columns containing a marked zero (-1)
            for i in range(n):
                for j in range(n):
                    if copy[i][j] == -1:
                        col_cover[j] = 1
    
    # Calculate number of lines by how many marked zeros (-1)
    num_lines = 0
    for i in range(n):
        for j in range(n):
            if copy[i][j] == -1:
                num_lines += 1
    return num_lines, row_cover, col_cover


def adjust_matrix(cost_matrix, row_cover, col_cover):
    n = len(cost_matrix)
    # Sets min to largest value plus 1 in matrix 
    min = np.max(cost_matrix) + 1
    # Calculates min of uncovered elements
    for i in range(n):
        for j in range(n):
            if row_cover[i] == 0 and col_cover[j] == 0:
                if cost_matrix[i][j] < min:
                    min = cost_matrix[i][j]
    
    # Subtracts min from uncovered rows
    for i in range(n):
        if row_cover[i] == 0:
            cost_matrix[i, :] = cost_matrix[i, :] - min * np.ones((n))
    
    # Adds min to covered columns
    for j in range(n):
        if col_cover[j] == 1:
            cost_matrix[:, j] = cost_matrix[:, j] + min * np.ones((n))

    # Returns new cost_matrix
    return cost_matrix


def optimal_assignment(cost_matrix, formation_positions):
    point_preferences = {}
    n = len(cost_matrix)
    copy = np.copy(cost_matrix)


    for k in range(0, n):
        # Gets number of zeros in each row
        row_zero = np.zeros(n)
        col_zero = np.zeros(n)
        for i in range(n):
            for j in range(n):
                if copy[i][j] == 0:
                    row_zero[i]+=1
                    col_zero[j]+=1
        # Finds the row with the least number of zeros
        row = np.argmax(row_zero)
        min = np.max(row_zero)
        for i in range(n):
            if row_zero[i] != 0 and row_zero[i] < min:
                min = row_zero[i]
                row = i

        # Finds zero with lowest column index
        for j in range(n):
            if(copy[row][j] == 0):
                col = j
                break
        
        zero_count = 0
        for i in range(n):
            for j in range(n):
                if copy[i][j] == 0:
                    zero_count+=1
        # Masks elements
        copy[row, :] =    copy[row, :] + np.ones((n))
        copy[:, col] = copy[:, col] + np.ones((1, n))
        point_preferences[row + 1] = (formation_positions[col])
    # Returns dictionary
    return point_preferences


# Returns Euclidean distance
def euclidean_distance(point1, point2):
    return np.linalg.norm(point2 - point1)


def distance_favour_x(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2)


def distance_favour_y(point1, point2):
    return np.sqrt((point1[1] - point2[1]) ** 2)


def pass_reciever_selector(player_unum, teammate_positions, final_target):
    
    # Input : Locations of all teammates and a final target you wish the ball to finish at
    # Output : Target Location in 2d of the player who is recieveing the ball
    #-----------------------------------------------------------#
    target = find_pass_receiver(player_unum, teammate_positions, final_target)

    if target == - 1:
        rng = np.random.default_rng()
        num = 1.25 * (rng.random() - 1)
        return final_target + np.array([0, num])
    else:
        return teammate_positions[target]


def find_pass_receiver(player_unum, teammate_positions, goal):
    distance = np.zeros(len(teammate_positions))

    curr_pos = teammate_positions[player_unum - 1]
    # If sufficiently close to the goal, try to score
    if(euclidean_distance(curr_pos, goal) < 4):
        return -1
    
    # Finds the best player to pass to
    for i, player in enumerate(teammate_positions):
        distance[i] = (distance_favour_x(curr_pos, player) + euclidean_distance(player, goal))
    
    distance[player_unum - 1] = np.max(distance) + 1
    
    return np.argmin(distance)

