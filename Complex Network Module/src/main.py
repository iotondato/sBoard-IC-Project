#!/usr/bin/python


import logging
from grab.spider import Spider, Task


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    class ExampleSpider(Spider):
        def task_generator(self):
            for lang in 'python', 'ruby', 'perl':
                url = 'https://www.google.com/search?q=%s' % lang
                yield Task('search', url=url, lang=lang)

        def task_search(self, grab, task):
             print('%s: %s' % (task.lang, grab.doc('//div[@class="s"]//cite').text()))

bot = ExampleSpider(thread_number=2)
bot.run()