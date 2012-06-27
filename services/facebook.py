from werkzeug.urls import url_decode
import foauth.providers


class Facebook(foauth.providers.OAuth2):
    # General info about the provider
    provider_url = 'https://facebook.com/'
    docs_url = 'https://developers.facebook.com/docs/'

    # URLs to interact with the API
    authorize_url = 'https://www.facebook.com/dialog/oauth'
    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    api_domain = 'graph.facebook.com'

    available_permissions = [
        (None, 'read your basic, public information'),
        ('email', 'access your email address'),
        ('user_about_me', 'access your profile information'),
        ('user_activities', 'access your favorite activities'),
        ('user_birthday', 'access your birthday'),
        ('user_checkins', 'access your checkins'),
        ('user_education_history', 'access your education history'),
        ('user_events', 'access your events'),
        ('user_groups', 'access your groups'),
        ('user_hometown', 'access your hometown'),
        ('user_interests', 'access your interests'),
        ('user_likes', 'access the things you like'),
        ('user_location', 'access your location'),
        ('user_notes', 'access your notes'),
        ('user_online_presence', 'access your online presence'),
        ('user_photos', 'access your photos'),
        ('user_questions', 'access your questions'),
        ('user_relationships', 'access your relationships'),
        ('user_relationship_details', 'access your relationship details'),
        ('user_religion_politics', 'access your religious and policial affiliations'),
        ('user_status', 'access your most recent status'),
        ('user_videos', 'access your videos'),
        ('user_website', 'access your website address'),
        ('user_work_history', 'access your work history'),
        ('friends_about_me', "access your friends' profile information"),
        ('friends_activities', "access your friends' favoriate activities"), ('friends_birthday', "access your friends' birthdays"),
        ('friends_checkins', "access your friends' checkins"),
        ('friends_education_history', "access your friends' education history"),
        ('friends_events', "access your friends' events"),
        ('friends_groups', "access your friends' groups"),
        ('friends_hometown', "access your friends' hometowns"),
        ('friends_interests', "access your friends' interests"),
        ('friends_likes', "access the things your friends like"),
        ('friends_location', "access your friends' locations"),
        ('friends_notes', "access your friends' notes"),
        ('friends_online_presence', "access your friends' online presence"),
        ('friends_photos', "access your friends' photos"),
        ('friends_questions', "access your friends' questions"),
        ('friends_relationships', "access your friends' relationships"),
        ('friends_relationship_details', "access your friends' relationship details"),
        ('friends_religion_politics', "access your friends' religious and political affiliations"),
        ('friends_status', "access your friends' most recent statuses"),
        ('friends_videos', "access your friends' videos"),
        ('friends_website', "access your friends' website addresses"),
        ('friends_work_history', "access your friends' work history"),
    ]

    def parse_token(self, content):
        data = url_decode(content)
        # Fix Facebook's spelling error
        data['expires_in'] = data.get('expires', None)
        return data

