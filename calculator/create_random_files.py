import random
import string
import os

# Generate two random filenames
def random_filename(length=8):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length)) + '.txt'

file1 = random_filename()
file2 = random_filename()

# Ensure filenames are unique
while file1 == file2:
    file2 = random_filename()

# Generate random content
content1 = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 50)))
content2 = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 50)))

# Write to files
with open(file1, 'w') as f:
    f.write(content1)

with open(file2, 'w') as f:
    f.write(content2)

print(f"Created file1: {file1}")
print(f"Created file2: {file2}")