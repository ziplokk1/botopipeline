import json
from collections import deque

from boto import sqs
from boto.sqs import message


class BotoPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler
        self.aws_access_key_id = crawler.settings.get('AWS_ACCESS_KEY')
        self.aws_secret_key = crawler.settings.get('AWS_SECRET_KEY')
        self.region = crawler.settings.get('AWS_REGION')
        self.queue_names = crawler.settings.get('SQS_QUEUE_NAMES')
        if not self.aws_access_key_id:
            raise ValueError('please set AWS_ACCESS_KEY in settings')
        elif not self.aws_secret_key:
            raise ValueError('please set AWS_SECRET_KEY in settings')
        elif not self.region:
            raise ValueError('please set AWS_REGION in settings')
        elif not self.queue_names:
            raise ValueError('please set SQS_QUEUE_NAMES in settings')
        self.connection = sqs.connect_to_region(self.region,
                                                aws_access_key_id=self.aws_access_key_id,
                                                aws_secret_access_key=self.aws_secret_key)
        self.queues = deque([(self.connection.get_queue(q), q) for q in self.queue_names])

    def process_item(self, item, spider):
        boto_item = item.__dict__.get('_values')
        msg_attrs = {
            'item_name': {
                'data_type': 'String',
                'string_value': item.__class__.__name__
            },
            'spider_name': {
                'data_type': 'String',
                'string_value': spider.__getattribute__('name') or 'scrapyspider'
            }
        }
        msg = message.Message()
        msg.set_body(json.dumps(boto_item))
        msg.message_attributes = msg_attrs

        # Write to one queue, then rotate to the next.
        # This way you can have multiple queues sharing the
        # load and multiple clients reading.
        q, name = self.queues[0]
        q.write(msg)
        self.crawler.stats.inc_value('SQS_writes/%s' % name)
        self.queues.rotate(-1)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
