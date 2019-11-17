import base64
import json
import requests
import tweepy
import twitter


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from demo import settings

class Tweets(APIView):
    """
    """
    def get(self, request):
        """
        """
        try:
            twitter_api = twitter.Api(consumer_key=settings.consumer_key,
                            consumer_secret=settings.consumer_secret,
                            access_token_key=settings.access_token,
                            access_token_secret=settings.access_secret)

            # get all the followers and their tweets
            followers_tweets = {}
            followers = twitter_api.GetFollowers()
            for follower in followers:
                followers_tweets.setdefault(follower.screen_name,[])
                try:
                    time_line = twitter_api.GetUserTimeline(follower.id)
                    for time_line_obj in time_line:
                        followers_tweets.get(follower.screen_name).append(
                            {'tweet':time_line_obj.text,
                            'created_at':str(time_line_obj.created_at),
                            'status_id':time_line_obj.id})
                except Exception as e:
                    continue

            status_id = 1120943438281601024
            # add new tweet
            res = twitter_api.PostUpdate(status='python tweeter api')
            # like the someone's tweet 
            liketweet = twitter_api.CreateFavorite(status_id=status_id,include_entities=True)
            # comment on the tweet
            auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
            auth.set_access_token(settings.access_token, settings.access_secret)
            twitter_api2 = tweepy.API(auth)
            res = twitter_api2.update_status('@RaviJatav35 happy bday', status_id)
            # retweet
            retweet = twitter_api.PostRetweet(status_id, trim_user=False)
            
            # search and follow
            search_user = twitter_api.GetUsersSearch(term='BarackObama',page=1,count=1)
            if len(search_user) > 0:
                new_friend = twitter_api.CreateFriendship(user_id=search_user[0].id, 
                                    screen_name=search_user[0].screen_name, 
                                    follow=True, retweets=True)
            # search tweets
            search_text = 'python'
            search_tweets_result = twitter_api.GetSearch(term=search_text)
            search_result = {}
            for obj in search_tweets_result:
                search_result.setdefault(obj.user.screen_name,[]).append({
                    "created_at": obj.created_at,
                    "text": obj.text
                })
            return Response({"followers_tweets":followers_tweets,"search_result":search_result,
                            "search_text":search_text})
        except Exception as e:
            print(e)
            return Response(repr(e))