import sys
import os.path

# The following allows organization of scripts in their own directory
# See the answer by Alex Martelli in this stack overflow post:
# https://stackoverflow.com/questions/1054271/how-to-import-a-python-class-that-is-in-a-directory-above
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
