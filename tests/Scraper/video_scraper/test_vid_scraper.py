import unittest
from unittest.mock import patch, Mock
from Scraper.video_scraper.vid_scraper import (extract_video_info_pexels, extract_video_info_pixabay,
                                               get_videos_from_pexels, get_videos_from_pixabay,
                                               extract_video_id_from_url, get_videos_for_keywords)


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
        video_data_high = {
            'videos': {'high': {'url': 'sample_link_high'}, 'medium': {'url': 'sample_link_medium'}},
            'duration': 120
        }
        result_high = extract_video_info_pixabay(video_data_high, 'nature')
        expected_high = {
            'keyword': 'nature',
            'url': 'sample_link_high',
            'quality': 'high',
            'duration': 120
        }
        self.assertEqual(result_high, expected_high)

        video_data_medium = {
            'videos': {'medium': {'url': 'sample_link_medium'}},
            'duration': 120
        }
        result_medium = extract_video_info_pixabay(video_data_medium, 'nature')
        expected_medium = {
            'keyword': 'nature',
            'url': 'sample_link_medium',
            'quality': 'medium',
            'duration': 120
        }
        self.assertEqual(result_medium, expected_medium)

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

    def test_extract_video_id_from_url(self):
        url1 = "https://cdn.pixabay.com/vimeo/176748903/stomach-band-surgery-4040.mp4?width=1280&hash=7aff560afd1084b56a31376f283f2d6112cf9aab"
        expected1 = "stomach-band-surgery-4040"
        self.assertEqual(extract_video_id_from_url(url1), expected1)

        url2 = "https://player.vimeo.com/external/504320527.sd.mp4?s=f190eee964adbf63b51cba72020e80f048c733f3&profile_id=165&oauth2_token_id=57447761"
        expected2 = "504320527.sd"
        self.assertEqual(extract_video_id_from_url(url2), expected2)

        url3 = "https://player.vimeo.com/external/504349109.hd.mp4?"
        expected3 = "504349109.hd"
        self.assertEqual(extract_video_id_from_url(url3), expected3)


if __name__ == '__main__':
    unittest.main()
