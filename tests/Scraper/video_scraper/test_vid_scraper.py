import unittest
from unittest.mock import patch, Mock
from Scraper.video_scraper.vid_scraper import (extract_video_info_pexels, extract_video_info_pixabay,
                                               get_videos_from_pexels, get_videos_from_pixabay, get_videos_for_keywords)


class TestVideoFunctions(unittest.TestCase):

    def test_extract_video_info_pexels(self):
        video_data = {
            'video_files': [{'link': 'sample_link', 'quality': '720p'}],
            'duration': 120
        }
        result = extract_video_info_pexels(video_data, 'nature')
        expected = {
            'keyword': 'nature',
            'url': 'sample_link',
            'quality': '720p',
            'duration': 120
        }
        self.assertEqual(result, expected)

    def test_extract_video_info_pixabay(self):
        video_data = {
            'videos': {'medium': {'url': 'sample_link'}},
            'duration': 120
        }
        result = extract_video_info_pixabay(video_data, 'nature')
        expected = {
            'keyword': 'nature',
            'url': 'sample_link',
            'quality': 'medium',
            'duration': 120
        }
        self.assertEqual(result, expected)

    @patch('requests.get')
    def test_get_videos_from_pexels(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'videos': [{'video_files': [{'link': 'sample_link', 'quality': '720p'}], 'duration': 120}]
        }
        mock_get.return_value = mock_response

        result = get_videos_from_pexels('nature', 'sample_api_key')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['url'], 'sample_link')

    @patch('requests.get')
    def test_get_videos_from_pixabay(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'hits': [{'videos': {'medium': {'url': 'sample_link'}}, 'duration': 120}]
        }
        mock_get.return_value = mock_response

        result = get_videos_from_pixabay('nature', 'sample_api_key')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['url'], 'sample_link')

    @patch('Scraper.video_scraper.vid_scraper.get_videos_from_pexels')
    @patch('Scraper.video_scraper.vid_scraper.get_videos_from_pixabay')
    def test_get_videos_for_keywords(self, mock_pixabay, mock_pexels):
        mock_pexels.return_value = [{'url': 'pexels_link'}]
        mock_pixabay.return_value = [{'url': 'pixabay_link'}]

        result = get_videos_for_keywords(['nature'], 'sample_pexels_key', 'sample_pixabay_key')
        self.assertEqual(len(result), 2)
        self.assertIn({'url': 'pexels_link'}, result)
        self.assertIn({'url': 'pixabay_link'}, result)

if __name__ == '__main__':
    unittest.main()
