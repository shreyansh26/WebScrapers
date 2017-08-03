# -*- coding: utf-8 -*-
import scrapy


class RedditbotSpider(scrapy.Spider):
    name = 'redditbot'
    allowed_domains = ['http://www.reddit.com/r/gameofthrones/']
    start_urls = ['http://www.reddit.com/r/gameofthrones//']

    custom_settings = {
		'FEED_URI' : 'tmp/reddit.csv'
	}

    def parse(self, response):
        # Extracting the content
        titles = response.css(".title.may-blank::text").extract()
        votes = response.css('.score.unvoted::text').extract()
        times = response.css('time::attr(title)').extract()
        comments = response.css('.comments::text').extract()

        #Give the extracted content row wise
        for item in zip(titles, votes, times, comments):
        	# create a dictionary for scraped info
        	scraped_info = {
        		'title': item[0],
        		'vote': item[1],
        		'created_at': item[2],
        		'comments': item[3]
        	}

        	yield scraped_info
