# Denmark-Mentions
---
### A simple social media scraper for Denmark

#### Files Description
* **yt_channels_list.json:** This file contains a list of youtube channels scraped from [Social Bakers](https://www.socialbakers.com/statistics/youtube/channels/denmark/) in JSON format.
* **fb_pages_list.json:** This file contains a list of facebook pages scraped from [Social Bakers](https://www.socialbakers.com/statistics/facebook/pages/total/denmark/) in JSON format.

* **app /**
    * **facebook_script.py:** This script uses facebook graph api to fetch posts and comments from the pages listed in `fb_pages_list.json` file. This script also saves the results as django models into postgres database.
    * **youtube_script.py:** This script uses youtube data api to fetch comments from all the videos from all the channels listed in `yt_channels_list.json`. This script also saves the results as django models into postgres database.
    * **yt_channels_list.py:** This script works if `yt_channels_list.json` is unavailable, in that case, the script fetches the survey from social bakers website and restores youtube channels list into the same json file.
    * **fb_pages_list.py:** This script works if `fb_pages_list.json` is unavailable, in that case, the script fetches the survey from social bakers website and restores the facebook pages list into the same json file.
    * **forms.py:** This file contains django forms for displaying on homepage.
    * **models.py:** This file contains django models for storing results after fetching data about pages and channels from facebook and youtube respectively.
    * **views.py:** This file contains view function about updating the entire database.
* **dkmentions /**
    * **prod_settings.py:** This file contains database settings for production environment.
    * **settings.py:** This file contains database settings for local development environment.
    * **urls.py:** This file contains url patterns for the website.
    * **views.py:** This file contains all the views for the application except update view.
