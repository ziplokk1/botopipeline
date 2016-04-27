from setuptools import setup, find_packages

version = '0.1.1'

REQUIREMENTS = [
    'boto',
    'scrapy'
]

setup(
    name='scrapy-sqs-pipeline',
    version=version,
    packages=find_packages(),
    url='https://github.com/ziplokk1/botopipeline',
    license='LICENSE.txt',
    author='Mark Sanders',
    author_email='sdscdeveloper@gmail.com',
    install_requires=REQUIREMENTS,
    description='Write scraped items to Amazon SQS.'
)
