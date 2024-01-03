from scripts.image_scraper import ImageScraper

if __name__ == "__main__":

    query = input("Enter search query: ")
    max_images = int(input("Enter the maximum number of images to fetch: "))
    db_host = input("Enter the database host: ")
    db_port = input("Enter the database port: ")
    db_name = input("Enter the database name: ")
    db_user = input("Enter the database user: ")
    db_password = input("Enter the database password: ")
    db_connection = f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"

    image_scraper = ImageScraper(db_connection)

    # Performing the operation
    image_urls = image_scraper.download_images(query, max_images)
    images = [image_scraper.download_and_resize_image(url) for url in image_urls]
    image_scraper.save_images_to_database(images)
