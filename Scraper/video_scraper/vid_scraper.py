import requests

def extract_video_info_pexels(video, keyword):
    """
    Extract relevant video information from a Pexels video object.
    
    :param video: Video data as returned by the Pexels API.
    :type video: dict
    :param keyword: The search keyword used to obtain this video.
    :type keyword: str
    :return: A dictionary containing relevant video information.
    :rtype: dict
    """
    return {
        'keyword': keyword,
        'url': video['video_files'][0]['link'],
        'quality': video['video_files'][0]['quality'],
        'duration': video['duration']
    }


def extract_video_info_pixabay(video, keyword):
    """
    Extract relevant video information from a Pixabay video object.
    
    :param video: Video data as returned by the Pixabay API.
    :type video: dict
    :param keyword: The search keyword used to obtain this video.
    :type keyword: str
    :return: A dictionary containing relevant video information.
    :rtype: dict
    """
    return {
        'keyword': keyword,
        'url': video['videos']['medium']['url'],
        'quality': 'medium',
        'duration': video['duration']
    }


def get_videos_from_pexels(keyword, pexels_api_key):
    """
    Fetch videos related to a given keyword from Pexels.
    
    :param keyword: The keyword to search for.
    :type keyword: str
    :param pexels_api_key: The API key for Pexels.
    :type pexels_api_key: str
    :return: A list of video information dictionaries.
    :rtype: list
    """
    url = "https://api.pexels.com/videos/search"
    querystring = {"query": keyword, "per_page": "5", "orientation": "landscape", "size": "medium"}
    headers = {'Authorization': pexels_api_key}
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"Pexels API request failed with status {response.status_code}")
        return []

    data = response.json()
    if 'videos' not in data:
        print(f"No videos found for keyword {keyword}")
        return []

    videos = data['videos']
    return [extract_video_info_pexels(video, keyword) for video in videos]


def get_videos_from_pixabay(keyword, pixabay_api_key):
    """
    Fetch videos related to a given keyword from Pixabay.
    
    :param keyword: The keyword to search for.
    :type keyword: str
    :param pixabay_api_key: The API key for Pixabay.
    :type pixabay_api_key: str
    :return: A list of video information dictionaries.
    :rtype: list
    """
    url = "https://pixabay.com/api/videos/"
    querystring = {
        "key": pixabay_api_key, 
        "q": keyword, 
        "video_type": "film", 
        "per_page": "5", 
        "orientation": "horizontal", 
        "video_quality": "720"
    }
    response = requests.get(url, params=querystring)
    videos = response.json()['hits']
    return [extract_video_info_pixabay(video, keyword) for video in videos]


def get_videos_for_keywords(keywords, pexels_api_key, pixabay_api_key):
    """
    Fetch videos related to a list of keywords from both Pexels and Pixabay.
    
    :param keywords: A list of keywords to search for.
    :type keywords: list
    :param pexels_api_key: The API key for Pexels.
    :type pexels_api_key: str
    :param pixabay_api_key: The API key for Pixabay.
    :type pixabay_api_key: str
    :return: A list of video information dictionaries from both platforms.
    :rtype: list
    """
    videos = []
    for keyword in keywords:
        videos.extend(get_videos_from_pexels(keyword, pexels_api_key))
        videos.extend(get_videos_from_pixabay(keyword, pixabay_api_key))
    return videos
