import os
from openai import OpenAI
from datetime import datetime
import sys
import json
import base64

from PIL import Image
import matplotlib.pyplot as plt

from pydantic import BaseModel

from utils_response import *
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--filename', type=str, help='filename', required=True)

    args = parser.parse_args()

    print(f'filename: {args.filename}')

if __name__ == '__main__':
    main()