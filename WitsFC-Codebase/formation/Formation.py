import numpy as np

class Formation:

    formation = []
    ball_location = np.zeros(2)

    def __init__(self, formation = [
        np.array([-14, 0]), # Goalkeeper
        np.array([-9, -5]), # Right Defender
        np.array([-9, 0]), # Centre Defender
        np.array([-9,  5]), # Left Defender
        np.array([-5, -5]), # Right Midfielder
        np.array([-5, -0]), # Centre Midfielder
        np.array([-5,  5]),  # Left Midfielder
        np.array([-1, -6]), # Right Forward
        np.array([-1, -2]), # Centre Right Forward
        np.array([-5, -5]), # Centre Left Forward
        np.array([-1,  6]) # Left Forward
    ], ball_location = np.zeros(2)):
        self.formation =  np.copy(formation)
        self.ball_location = np.copy(ball_location)

        
    
    def update_formation(self):
        # Set goalkeeper and defence
        self.formation[0] = np.array([-14, self.ball_location[1] / 10 ])
        self.formation[1] = np.array([-11, -5])
        self.formation[2] = np.array([-9, 0])
        self.formation[3] = np.array([-11,  5])

        if self.ball_location[0] >= 0:
            self.formation[4] = self.ball_location + np.array([-2, -7]) 
            self.formation[5] = self.ball_location + np.array([5, -2]) 
            self.formation[6] = self.ball_location + np.array([-2, 7]) 
            self.formation[7] = self.ball_location + np.array([3, -5]) 
            self.formation[8] = self.ball_location + np.array([3, 5]) 
            self.formation[9] = self.ball_location + np.array([5, 2]) 
            self.formation[10] = self.ball_location + np.array([-5, 0]) 
        else:
            self.formation[4] = self.ball_location + np.array([-3, -7]) 
            self.formation[5] = self.ball_location + np.array([-5, 0]) 
            self.formation[6] = self.ball_location + np.array([-3, 7]) 
            self.formation[7] = self.ball_location + np.array([3, -5]) 
            self.formation[8] = self.ball_location + np.array([3, 5]) 
            self.formation[9] = self.ball_location + np.array([-5, 0]) 
            self.formation[10] = self.ball_location + np.array([3, 3]) 

        for i in range(len(self.formation)):
            if self.formation[i][0] >=15:
                self.formation[i][0] = 14
            if self.formation[i][1] >=10:
                self.formation[i][1] = 9
            if self.formation[i][0] <= - 15:
                self.formation[i][0] = -14
            if self.formation[i][1] <= -10:
                self.formation[i][1] = -9


    def get_formation(self):
        return self.formation

    
