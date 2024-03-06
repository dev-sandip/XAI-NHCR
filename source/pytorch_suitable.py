from pathlib import Path
import shutil
import random
import math

def split_data(src_dir, dest_dir, train_ratio=0.8, test_ratio=0.1, valid_ratio=0.1):
    train_dir = dest_dir / 'train'
    valid_dir = dest_dir / 'validate'
    test_dir = dest_dir / 'test'

    train_dir.mkdir(parents=True, exist_ok=True)
    valid_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    # Iterate through class directories
    for class_dir in src_dir.iterdir():
        if class_dir.is_dir():
            images = list(class_dir.glob('*.jpg')) 

            random.shuffle(images)

            total_images = len(images)
            train_split = math.ceil(total_images * train_ratio)
            valid_split = train_split + math.ceil(total_images * valid_ratio)

            train_images = images[:train_split]
            valid_images = images[train_split:valid_split]
            test_images = images[valid_split:]

            # Create subdirectories in train, validate, and test
            train_class_dir = train_dir / class_dir.name
            valid_class_dir = valid_dir / class_dir.name
            test_class_dir = test_dir / class_dir.name

            train_class_dir.mkdir(parents=True, exist_ok=True)
            valid_class_dir.mkdir(parents=True, exist_ok=True)
            test_class_dir.mkdir(parents=True, exist_ok=True)

            # Copy images to the respective subdirectories
            for img in train_images:
                shutil.copy(img, train_class_dir / img.name)

            for img in valid_images:
                shutil.copy(img, valid_class_dir / img.name)

            for img in test_images:
                shutil.copy(img, test_class_dir / img.name)

if __name__ == "__main__":
    source_directory = Path('/home/pujan/D/datasets/nepali_augmented/nhcd_augmented')
    destination_directory = Path('/home/pujan/D/datasets/nepali_augmented/nhcd_pytorch')

    split_data(source_directory, destination_directory)
