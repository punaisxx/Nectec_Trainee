#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 File name: fake_landuse_classification.py
 Date Create: 17/7/2024 AD 08:23
 Author: Wongnaret Khantuwan 
 Email: wongnaet.khantuwan@nectec.or.th, wongnaret@gmail.com
 Python Version: 3.9
"""

import os
import random
import time
import string
import click

def generate_random_text(length):
    """Generate random text of a given length."""
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for _ in range(length))

def create_random_file(file_path):
    """Create a random text file at the given file path."""
    # Ensure the directory exists
    with open(file_path, 'w') as file:
        file.write(generate_random_text(
            random.randint(100, 1000)))  # random content length between 100 and 1000 characters
    print(f"Created file: {file_path}")

def create_temp_file(temp_path):
    """Create a temporary file."""
    with open(temp_path, 'w') as temp_file:
        temp_file.write("This is a temporary file.")
    print(f"Created temporary file: {temp_path}")

def delete_temp_file(temp_path):
    """Delete the temporary file."""
    if os.path.exists(temp_path):
        os.remove(temp_path)
        print(f"Deleted temporary file: {temp_path}")
    else:
        print(f"Temporary file not found: {temp_path}")

@click.command()
@click.option('-f', '--filename', type=click.Path() ,help='The output file path')
def export_file(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    create_temp_file(filename+'.tmp')

    delay = random.uniform(30, 40)  # delay between 30 seconds and 5 minutes
    # delay = random.uniform(600, 1200)
    # delay = random.uniform(1, 2)
    print(f"Waiting for {delay:.2f} seconds before creating the next file.")
    time.sleep(delay)

    create_random_file(file_path=filename)
    delete_temp_file(filename+".tmp")
    return 0

if __name__ == "__main__":
    export_file()
