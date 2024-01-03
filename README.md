# Image Scraping Python Program

## How it works
It gives a text and searches that in Google, after that it downloads the images resizes them, and saves them in PostgreSQL database.

## Features
 - It's deployable through Docker
 - You can choose the maximum number of images

## Setup and Instructions 
First, make sure you have Python 3.8 installed.
I used poetry as the package manager (install poetry).

Go to project folder and install the dependencies using this command:
```shell
poetry install
```

start the virtual environment using this:
```shell
poetry shell
```

make sure you have set up the PostgreSQL database before and start the project:
```shell
python main.py
```

If you want to run the tests you can run `test.py`.
Thank you :)
