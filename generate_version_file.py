import subprocess

def generate_version_file(output_file="version.py"):
    version = subprocess.check_output(
        ["git", "describe", "--abbrev=7", "--dirty", "--always", "--tags"]
    ).decode("utf-8").strip()

    # Écrit le fichier version.py
    with open(output_file, "w") as f:
        f.write(f'VERSION = "{version}"\n')

if __name__ == "__main__":
    generate_version_file()