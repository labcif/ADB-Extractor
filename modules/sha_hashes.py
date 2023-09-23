import hashlib
import os


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def calculate_sha256_for_directory(root_dir, output_file):
    with open(output_file, "w") as file:
        for foldername, subfolders, filenames in os.walk(root_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                sha256 = calculate_sha256(file_path)
                relative_path = os.path.relpath(file_path, root_dir)
                #ignore if the file is the sha256 file itself
                if "sha256_hashes.txt" not in relative_path:
                    file.write(f"{sha256} *{relative_path}\n")
