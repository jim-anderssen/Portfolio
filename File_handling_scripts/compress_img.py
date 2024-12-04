import os
from PIL import Image
import argparse


def compress_image(input_path, quality):
    """
    Compress an image and save it to the output path.
    
    :param input_path: Path to the input image file
    :param output_path: Path to save the compressed image file
    :param quality: Quality setting for compression (1-100)
    """
    file_size = 0
    try:
        input_path = os.path.normpath(input_path)
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"The file {input_path} does not exist.")
        
        file_size = os.path.getsize(input_path) / 1024
        if file_size > 400:
            with Image.open(input_path) as img:
                # Convert image to RGB mode if it's not
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                # Save the image with the specified quality
                img.save(input_path, "JPEG", quality=quality)
                print(f"Compressed and saved: {input_path}")
            file_size -= (os.path.getsize(input_path) / 1024)
    except Exception as e:
        print(f"Failed to compress {input_path}: {e}")
    return file_size

def compress_images_in_directory(directory, quality):
    """
    Compress all images in the given directory and save them to the output directory.
    
    :param directory: Directory to search for image files
    :param output_directory: Directory to save compressed images
    :param quality: Quality setting for compression (1-100)
    """
    total_compressed = 0
    for root, dirs, files in os.walk(directory):
        current_dir = os.path.basename(root)
        if current_dir == '18.Bilagor_till_protokoll' or current_dir == '23.Nykarleby':
            continue
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                input_path = os.path.join(root, file)
                #print('Managed to start comressing')
                total_compressed += compress_image(input_path, quality)
    print('Total amount of compressed: ', total_compressed/(10**6),' GB')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image compresser, choose directory to compress 50 percent')
    parser.add_argument('input',help="input directory")
    #parser.add_argument('quality',help="Compression percentage, 50 is standard")
    args = parser.parse_args()
    print('Input: ',args.input)
    #print('Quality: ',args.quality)

    # Directory to search for image files
    #input_directory = "J:/MILJOHÄLSOVÅRD/hälsoinspektionen-terveysvalvonta/Hälsoskydd/Badvatten"
    #input_directory = 'J:\MILJOHÄLSOVÅRD\hälsoinspektionen -terveysvalvonta\Hälsoskydd/Bilagor till protokoll/Badstränder/Foton'
    # Quality setting for compression (1-100)
    compression_quality = 50

    compress_images_in_directory(args.input, compression_quality)
    #print(f"Image compression complete: ",args.quality,'%')