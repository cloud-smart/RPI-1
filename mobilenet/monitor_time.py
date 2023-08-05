import subprocess
import time
import os

# Function to run the command and measure time taken
def measure_process_time(command):
    start_time = time.time()

    # Run the command using subprocess
    subprocess.run(command, shell=True)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print time taken
    s = "Time taken by process: {:.3f} seconds\n".format(elapsed_time)
    
    with open("RESOURCE_LOG.txt", 'a') as file:
        file.write(s + '\n')
      
      
#Delete the resource_log file to freshly write to it
if os.path.exists("RESOURCE_LOG.txt"):
    os.remove("RESOURCE_LOG.txt")
                
#iterate over all test_images
for img in os.listdir("/home/pi/RPI-1/mobilenet/test_images"):
    
    # Command to mrun model
    command = "python3 obj_det.py --prototxt SSD_MobileNet_prototxt.txt --model SSD_MobileNet.caffemodel --image test_images/" + str(img)
    
    print(command + "\n")
    
    # Measure time taken by the command
    measure_process_time(command)

