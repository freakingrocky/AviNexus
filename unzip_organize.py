import multiprocessing
import os
import shutil
import zipfile
from pathlib import Path

from tqdm import tqdm


def list_zip_files():
    """
    List all ZIP files in the current directory.
    """
    return list(Path('.').glob('*.zip'))

def extract_zip_file(zip_file, extract_to):
    """
    Extract a ZIP file to a specific location.
    """
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f'Extracted: {zip_file}')

def is_image_file(filename):
    """
    Check if a file is an image based on its extension.
    """
    return filename.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']

def move_files_to_data_folder(root_dir, target_dir='data'):
    """
    Move files to target data directory based on categories inferred from directory names.
    """
    root_path = Path(root_dir)
    target_path = Path(target_dir)
    image_files = [f for f in root_path.rglob('*') if f.is_file() and is_image_file(f)]

    for file in image_files:
        category_name = file.parent.name
        target_category_path = target_path / category_name
        target_category_path.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file), str(target_category_path / file.name))
        print(f'Moved: {file} to {target_category_path / file.name}')

def process_folder(folder):
    """
    Process each folder by extracting and moving files.
    """
    extract_root = f'extracted_files_{Path(folder).stem}'
    extract_zip_file(folder, extract_root)
    move_files_to_data_folder(extract_root)
    shutil.rmtree(extract_root)

def main():
    # Step 1: List ZIP files
    zip_files = list_zip_files()

    # Step 2: Use multiprocessing to handle each ZIP file concurrently
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for _ in tqdm(pool.imap_unordered(process_folder, zip_files), total=len(zip_files), desc="Processing ZIP files"):
            pass

if __name__ == "__main__":
    main()
