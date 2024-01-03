import unittest
from unittest.mock import patch, Mock, call
from scripts.image_scraper import ImageScraper
from io import BytesIO


class TestImageScraper(unittest.TestCase):

    @patch('scripts.image_scraper.requests.get')
    @patch('scripts.image_scraper.Image.open')
    def test_download_and_resize_image(self, mock_open, mock_get):
        url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        mock_response = Mock()
        mock_response.content = b"dummy_content"
        mock_get.return_value = mock_response
        mock_image = Mock()
        mock_open.return_value = mock_image

        image_scraper = ImageScraper("dummy_db_connection")
        result = image_scraper.download_and_resize_image(url)

        mock_get.assert_called_once_with(url)
        mock_response.raise_for_status.assert_called_once()

        # Checking if the 'open' was called with any BytesIO object
        mock_open.assert_called_once()
        args, _ = mock_open.call_args
        self.assertIsInstance(args[0], BytesIO)

        # Checking for the response content before resize
        if mock_response.content:
            self.assertTrue(mock_image.resize.called)

        # Testing the mock objects
        self.assertEqual(result.call_args, mock_image.call_args)

    @patch('scripts.image_scraper.requests.get')
    def test_download_images(self, mock_get):
        query = "cat"
        max_images = 5
        mock_response = Mock()
        mock_get.return_value = mock_response
        mock_soup = Mock()
        mock_soup.find_all.return_value = [
            {'src': 'https://example.com/image1.jpg'},
            {'src': 'https://example.com/image2.jpg'},
            {'src': 'https://external.com/image3.jpg'},
            {'src': 'invalid_url'},
            {'src': 'https://example.com/image4.jpg'}
        ]
        mock_response.text = "dummy html"
        with patch('scripts.image_scraper.BeautifulSoup', return_value=mock_soup):
            image_scraper = ImageScraper("dummy_db_connection")
            result = image_scraper.download_images(query, max_images)

        mock_get.assert_called_once_with(f"https://www.google.com/search?q={query}&tbm=isch")
        mock_soup.find_all.assert_called_once_with('img', src=True)

        expected_result = [
            'https://example.com/image1.jpg',
            'https://example.com/image2.jpg',
            'https://external.com/image3.jpg',
            'https://example.com/image4.jpg'
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
