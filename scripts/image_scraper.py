import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import psycopg2


class ImageScraper:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def download_images(self, query, max_images):
        search_url = f"https://www.google.com/search?q={query}&tbm=isch"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        image_urls = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            if src.startswith('http'):
                image_urls.append(src)

            if len(image_urls) == max_images:
                break

        return image_urls

    def download_and_resize_image(self, url, size=(100, 100)):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img = img.resize(size)
            return img
        except (requests.exceptions.RequestException, OSError, Image.DecompressionBombError) as e:
            print(f"Error downloading image from {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error processing image from {url}: {e}")
            return None

    def save_images_to_database(self, images):
        try:
            conn = psycopg2.connect(self.db_connection)
            cursor = conn.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS images (id serial PRIMARY KEY, data bytea);")

            for img in images:
                data = BytesIO()
                img.save(data, format='PNG')
                data = data.getvalue()
                cursor.execute("INSERT INTO images (data) VALUES (%s);", (data,))

            conn.commit()
            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
