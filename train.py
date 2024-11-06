import os
import subprocess

# Define paths
base_dir = os.getcwd()
data_dir = os.path.join(base_dir, 'data')
model_dir = os.path.join(base_dir, 'model')
yolov7_dir = os.path.join(base_dir, 'yolov7-git')

# Paths for training script and weights
train_script = os.path.join(yolov7_dir, 'train.py')
data_yaml_path = os.path.join(base_dir, 'data.yaml')

# Define the paths
exp_path = "./runs/train/exp6"
weights_path = os.path.join(exp_path, "weights", "best.pt")


# Check if all required files and directories exist
if not os.path.isfile(weights_path):
    raise Exception(f"Pre-trained weights file '{weights_path}' does not exist.")
if not os.path.isfile(train_script):
    raise Exception(f"Training script '{train_script}' not found.")

# Optimized training command
cmd = [
    'python', train_script,
    '--img', '416',          # Reduced image resolution
    '--batch', '32',         # Increased batch size
    '--epochs', '70',        # Fewer epochs for quicker training
    '--data', data_yaml_path,
    '--weights', weights_path,
    '--device', '0'         # Set to '0,1' if using multiple GPUs
    # "--cfg", "cfg/training/yolov7.yaml"
]

# Run the training command
try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"Training failed: {e}")
