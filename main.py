from PIL import Image
import numpy as np
import random

def image_to_binary(image_name):
    img = Image.open(image_name + '.png').convert('RGB')
    img_array = np.array(img)
    height, width, _ = img_array.shape
    binary_string = ''.join (
        format(pixel, '08b') 
        for row in img_array 
        for pixel in row.flatten()
    )
    with open(image_name + '.txt', 'w') as file:
        file.write(f"{width} {height}\n")
        file.write(binary_string)

def binary_to_image(image_name):
    with open(image_name + '.txt', 'r') as file:
        lines = file.readlines()
        width, height = map(int, lines[0].strip().split())
        binary_string = ''.join(lines[1:]).strip()
    num_pixels = width * height
    pixels_binary = [binary_string[i:i+24] for i in range(0, len(binary_string), 24)]
    pixel_values = np.array([[
            int(pixels_binary[i][0:8], 2),
            int(pixels_binary[i][8:16], 2),
            int(pixels_binary[i][16:24], 2)
        ] for i in range(num_pixels)
    ], dtype=np.uint8).reshape((height, width, 3))
    img = Image.fromarray(pixel_values, 'RGB')
    img.save(image_name + '.png')

def randomly_swap_bits_in_color_data(input_image, output_image, swap_percentage):
    with open(input_image + '.txt', 'r') as file:
        lines = file.readlines()
        dimensions = lines[0].strip()
        binary_string = ''.join(lines[1:]).strip()
    total_bits = len(binary_string)
    num_bits_to_swap = int(total_bits * swap_percentage)
    swap_indices = random.sample(range(total_bits), num_bits_to_swap)
    binary_list = list(binary_string)
    for index in swap_indices:
        binary_list[index] = '1' if binary_list[index] == '0' else '0'
    modified_binary_string = ''.join(binary_list)
    with open(output_image + '.txt', 'w') as file:
        file.write(f"{dimensions}\n")
        file.write(modified_binary_string)

def compare_images(first_image, second_image):
    def read_binary_data(txt_file):
        with open(txt_file, 'r') as file:
            lines = file.readlines()
            width, height = map(int, lines[0].strip().split())
            binary_string = ''.join(lines[1:]).strip()
        return width, height, binary_string
    def binary_to_pixel_values(width, height, binary_string):
        num_pixels = width * height
        pixels_binary = [binary_string[i:i+24] for i in range(0, len(binary_string), 24)]
        pixel_values = np.array([[
                int(pixels_binary[i][0:8], 2),
                int(pixels_binary[i][8:16], 2),
                int(pixels_binary[i][16:24], 2)
            ] for i in range(num_pixels)
        ], dtype=np.uint8).reshape((height, width, 3))
        return pixel_values
    width1, height1, binary_string1 = read_binary_data(first_image + '.txt')
    width2, height2, binary_string2 = read_binary_data(second_image + '.txt')
    if (width1, height1) != (width2, height2):
        raise ValueError("Images have different dimensions and cannot be compared.")
    pixel_values1 = binary_to_pixel_values(width1, height1, binary_string1)
    pixel_values2 = binary_to_pixel_values(width2, height2, binary_string2)
    differing_pixels = np.sum(np.any(pixel_values1 != pixel_values2, axis=-1))
    return differing_pixels

def count_pixels(image_name):
    img = Image.open(image_name + '.png')
    width, height = img.size
    num_pixels = width * height
    return num_pixels

original_image = 'image_0'
image_to_binary(original_image)
print(f"Number of pixels in {original_image}: {count_pixels(original_image)}")

first_image = 'image_1'
randomly_swap_bits_in_color_data(original_image, first_image, 0.1)
binary_to_image(first_image)
print(f"Differing pixels of {first_image}: {compare_images(original_image, first_image)}")

second_image = 'image_2'
randomly_swap_bits_in_color_data(original_image, second_image, 0.05)
binary_to_image(second_image)
print(f"Differing pixels of {second_image}: {compare_images(original_image, second_image)}")

third_image = 'image_3'
randomly_swap_bits_in_color_data(original_image, third_image, 0.01)
binary_to_image(third_image)
print(f"Differing pixels of {third_image}: {compare_images(original_image, third_image)}")
