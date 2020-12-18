'''
Main file
'''
from src.BallTracker import BallTracker

# For Soccer
ball_lower = (20,200,100)
ball_upper = (35,255,200)

# For Ping
# ball_lower = (30,0,0)
# ball_upper = (40,255,255)

track = BallTracker("test_vids/Soccer.mp4", ball_lower, ball_upper)
track.read_vid()
