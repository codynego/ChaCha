# write me a feeds algorithm based on users interests and location


class FeedAlgorithm():
    def __init__(self, user, stories):
        self.user = user
        self.stories = stories

    
    def get_feed(self):
        user = self.user
        stories = self.stories
        feeds = []

        pass

    def get_feeds_by_interest(self):
        feeds = self.stories.filter(user__interest__in=self.user.interests.all())
        return feeds
    

    def get_feeds_by_location(self):
        feeds = self.stories.filter(user__location=self.user.location)
        return feeds
    
    