import os
import subprocess

password = "admin123"

def run():
    user_input = input("Enter command: ")
    subprocess.call(user_input, shell=True)

if __name__ == "__main__":
    run()
