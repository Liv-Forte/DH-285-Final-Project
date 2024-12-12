import cv2
import os

# Read the video from specified path
video = cv2.VideoCapture("/Users/oliviaforte/DH 285 Final Project/Code/mp4_to_images/test.mp4")

# Get the video's frame rate (FPS) and total frame count
fps = int(video.get(cv2.CAP_PROP_FPS))
frame_interval = fps * 10  # Number of frames to skip for a 10-second interval

folder_name = ""  # Stores the folder name chosen by user

try:
    # Creating a folder with user given name
    correct_folder_name = False
    while correct_folder_name == False:
        folder_name = input("Enter the name that you want your file to be: ")
        file_confirmation = input(f"Are you sure you want to create a file with the name {folder_name}? (Y/N) ").lower()
        if file_confirmation == "y":
            correct_folder_name = True
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0
frame_count = 0

while (True):

    # reading from frame
    ret, frame = video.read()

    if not ret:
        # If no frame is returned, the video has ended
        break

    # Save the frame only if it is at the correct interval
    if frame_count % frame_interval == 0:
        image_name = os.path.join(folder_name, f'{folder_name}_image{currentframe}.jpg')
        print(f'Creating... {image_name}')
        cv2.imwrite(image_name, frame)
        currentframe += 1

    # Increment frame count
    frame_count += 1

# Release all space and windows once done
video.release()
cv2.destroyAllWindows()

print('Done!')
