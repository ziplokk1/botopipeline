# Summary

Simple pipeline to write to Amazon's Simple Queue Service (SQS).

The pipeline will write json serialized items to the queue specified in your scrapy settings file.

## Configuration

To configure the pipeline add the following lines to settings.py

```python
AWS_ACCESS_KEY = '<your_access_key>'
AWS_SECRET_KEY = '<your_secret_key>'
AWS_REGION = '<your_aws_region>'
SQS_QUEUE_NAMES = ['<your_sqs_queue_name>']

ITEM_PIPELINES = {
    'sqspipeline.BotoPipeline': 300
}

# Optional
# Default = False
# Raise CloseSpider exception if there are still items in the queue
RAISE_IF_QUEUE_NOT_EMPTY = True
```
