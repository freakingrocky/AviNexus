import os
import random
import shutil
import subprocess

# Define the classes based on your category_map
classes = [
    'bottles', 'cans', 'cardboard', 'clothes', 'detergent', 'glass', 'metal',
    'paper', 'plastic', 'recyclable', 'organic-recyclable', 'biological',
    'non-recyclable', 'shoes', 'teabags', 'battery', 'trash'
]

# Paths (adjusted based on your folder structure)
base_dir = os.getcwd()  # Current working directory
data_dir = os.path.join(base_dir, 'data')
model_dir = os.path.join(base_dir, 'model')
yolov7_dir = os.path.join(base_dir, 'yolov7-git')

# Ensure the 'data' directory exists
if not os.path.isdir(data_dir):
    raise Exception(f"The data directory '{data_dir}' does not exist.")

# Create directories for training, validation, and test sets
train_images_dir = os.path.join(data_dir, 'train', 'images')
val_images_dir = os.path.join(data_dir, 'val', 'images')
test_images_dir = os.path.join(data_dir, 'test', 'images')
train_labels_dir = os.path.join(data_dir, 'train', 'labels')
val_labels_dir = os.path.join(data_dir, 'val', 'labels')
test_labels_dir = os.path.join(data_dir, 'test', 'labels')

# Create directories if they don't exist
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(test_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)
os.makedirs(test_labels_dir, exist_ok=True)

# Split ratios
train_ratio = 0.7
val_ratio = 0.15  # validation ratio
test_ratio = 0.15  # test ratio

# Process each category folder
for class_name in classes:
    class_dir = os.path.join(data_dir, class_name)
    if not os.path.isdir(class_dir):
        print(f"Warning: The class directory '{class_dir}' does not exist. Skipping.")
        continue  # Skip if the class directory doesn't exist

    # List all image files in the class directory
    images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        print(f"Warning: No images found in '{class_dir}'. Skipping.")
        continue

    random.shuffle(images)
    num_images = len(images)
    num_train = int(num_images * train_ratio)
    num_val = int(num_images * val_ratio)
    num_test = num_images - num_train - num_val  # Ensure all images are used

    train_images = images[:num_train]
    val_images = images[num_train:num_train + num_val]
    test_images = images[num_train + num_val:]

    class_index = classes.index(class_name)

    # Copy images and create label files for the training set
    for img_name in train_images:
        img_src = os.path.join(class_dir, img_name)
        img_dst = os.path.join(train_images_dir, img_name)
        shutil.copyfile(img_src, img_dst)

        # Create label file with the entire image as bounding box
        label_dst = os.path.join(train_labels_dir, os.path.splitext(img_name)[0] + '.txt')
        with open(label_dst, 'w') as f:
            f.write(f"{class_index} 0.5 0.5 1.0 1.0\n")

    # Copy images and create label files for the validation set
    for img_name in val_images:
        img_src = os.path.join(class_dir, img_name)
        img_dst = os.path.join(val_images_dir, img_name)
        shutil.copyfile(img_src, img_dst)

        # Create label file with the entire image as bounding box
        label_dst = os.path.join(val_labels_dir, os.path.splitext(img_name)[0] + '.txt')
        with open(label_dst, 'w') as f:
            f.write(f"{class_index} 0.5 0.5 1.0 1.0\n")

    # Copy images and create label files for the test set
    for img_name in test_images:
        img_src = os.path.join(class_dir, img_name)
        img_dst = os.path.join(test_images_dir, img_name)
        shutil.copyfile(img_src, img_dst)

        # Create label file with the entire image as bounding box
        label_dst = os.path.join(test_labels_dir, os.path.splitext(img_name)[0] + '.txt')
        with open(label_dst, 'w') as f:
            f.write(f"{class_index} 0.5 0.5 1.0 1.0\n")

# Create the data.yaml file for YOLOv7
data_yaml_path = os.path.join(base_dir, 'data.yaml')
data_yaml_content = f"""
train: {train_images_dir.replace(os.sep, '/')}
val: {val_images_dir.replace(os.sep, '/')}
test: {test_images_dir.replace(os.sep, '/')}

nc: {len(classes)}
names: {classes}
"""
with open(data_yaml_path, 'w') as f:
    f.write(data_yaml_content)

# Path to the pre-trained weights
weights_path = os.path.join(model_dir, 'yolo.pt')

# Check if the weights file exists
if not os.path.isfile(weights_path):
    raise Exception(f"The weights file '{weights_path}' does not exist.")

# Training command using subprocess
train_script = os.path.join(yolov7_dir, 'train.py')
cmd = [
    'python', train_script,
    '--img', '640',
    '--batch', '16',
    '--epochs', '100',
    '--data', data_yaml_path,
    '--weights', weights_path,
    '--device', '0'
]

# Execute the training command
subprocess.run(cmd, check=True)
a