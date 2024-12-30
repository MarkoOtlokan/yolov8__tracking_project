import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

def plot_tracking_data(tracking_data):
    """
    Plot the raw detection probabilities for tracked objects dynamically.

    Args:
        tracking_data (dict): A dictionary where keys are object IDs and values 
                              are tuples containing frame numbers and detection probabilities.
    """
    fig, ax = plt.subplots(figsize=(15, 10))
    lines = {}

    def update(frame):
        ax.clear()
        ax.set_title("Detection Probabilities Over Time")
        ax.set_xlabel("Frame Number")
        ax.set_ylabel("Detection Probability")
        
        for obj_id, data in tracking_data.items():
            frame_numbers, probabilities = data
            if frame_numbers and probabilities:  # Ensure there is data to plot
                ax.plot(frame_numbers, probabilities, label=f"ID {obj_id}")
        
        ax.legend(loc='upper right')
        ax.relim()
        ax.autoscale_view()

    ani = FuncAnimation(fig, update, interval=100)
    plt.show()
    
def smooth_data(data, window_size=5, sigma=5.0):
    """
    Smooth the input data using a Gaussian kernel for better visualization.

    Args:
        data (list or np.ndarray): The data to be smoothed, typically detection probabilities.
        window_size (int): The size of the window used for smoothing (must be odd).
        sigma (float): The standard deviation of the Gaussian kernel used for smoothing.

    Returns:
        np.ndarray: Smoothed version of the input data.
    """
    if len(data) < window_size:
        return data  # Not enough data to smooth, return as-is

    smoothed_data = gaussian_filter1d(data, sigma=sigma)
    return smoothed_data

def plot_tracking_data_smoth(tracking_data):
    """
    Plot the smoothed detection probabilities for tracked objects dynamically.

    Args:
        tracking_data (dict): A dictionary where keys are object IDs and values 
                              are tuples containing frame numbers and detection probabilities.
    """
    fig, ax = plt.subplots(figsize=(15, 10))
    lines = {}

    def update(frame):
        ax.clear()
        ax.set_title("Detection Probabilities Over Time (Smoothed)")
        ax.set_xlabel("Frame Number")
        ax.set_ylabel("Detection Probability")

        for obj_id, data in tracking_data.items():
            frame_numbers, probabilities = data
            if frame_numbers and probabilities:  # Ensure there is data to plot
                smoothed_probabilities = smooth_data(probabilities)
                # Adjust the corresponding frame numbers to match the smoothed data
                adjusted_frame_numbers = frame_numbers[:len(smoothed_probabilities)]
                ax.plot(adjusted_frame_numbers, smoothed_probabilities, label=f"ID {obj_id}")
        
        ax.legend(loc='upper right')
        ax.relim()
        ax.autoscale_view()

    ani = FuncAnimation(fig, update, interval=100)
    plt.show()
