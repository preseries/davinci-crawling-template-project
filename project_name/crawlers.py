# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 PreSeries Tech, SL

import logging

from caravaggio_rest_api.solr import CaravaggioSearchPaginator
from datetime import datetime

from dateutil.parser import parse as date_parse

from solrq import Q, Range, ANY
from caravaggio_rest_api.query import CaravaggioSearchQuerySet

from {{ project_name }} import CRAWLER_NAME
from {{ project_name }}.utils import \
    get_from_date, RESET_FROM_DATE_ARG, FROM_DATE_ARG, \
    LAST_EXECUTION_DATE_CTL_FIELD
from .models import BovespaCompanyFile, FILE_STATUS_NOT_PROCESSED

from davinci_crawling.crawler import Crawler
from davinci_crawling.io import put_checkpoint_data, get_checkpoint_data
from davinci_crawling.time import mk_datetime

# The name of the checkpoint block
CRAWLER_FILE_CTL = CRAWLER_NAME


_logger = logging.getLogger("davinci_crawler_{}".format(CRAWLER_NAME))


class {{ project_name }}Crawler(Crawler):

    __crawler_name__ = CRAWLER_NAME

    def add_arguments(self, parser):
        self._parser.add_argument(
            '--from-the-beginning',
            required=False,
            action='store_true',
            dest='{}'.format(RESET_FROM_DATE_ARG),
            default=None,
            help="Crawl all since the beginning."
                 "It is a way to short-circuit the global last execution date."
                 " Ex. '2007-09-03T20:56:35.450686Z")
        # Process files from an specific date
        self._parser.add_argument(
            '--from-date',
            required=False,
            action='store',
            dest='{}'.format(FROM_DATE_ARG),
            default=None,
            type=mk_datetime,
            help="The date from which we want to crawl all the company files."
                 "It is a way to short-circuit the global last/current dates."
                 " Ex. '2007-09-03T20:56:35.450686Z")

    def crawl_params(self, **options):
        now = options.get("current_execution_date", datetime.utcnow())
        _logger.debug("{0}: Current execution time: {1}".
                      format(CRAWLER_NAME, now))

        # Check if there is an internal checkpoint, use to save the status of
        # the crawler between executions
        checkpoint_data = get_checkpoint_data(
            CRAWLER_NAME, CRAWLER_FILE_CTL, default={})\

        from_date = get_from_date(options, checkpoint_data)

        ###### The Crawler logic to obtain the objects to be crawl comes here

        # DEMO
        crawling_params = range(20)

        checkpoint_data[LAST_EXECUTION_DATE_CTL_FIELD] = now

        # Let's signal that we have processed the latest files (til 'now')
        # To process the new ones the last time we run the process
        put_checkpoint_data(CRAWLER_NAME,
                            CRAWLER_FILE_CTL,
                            checkpoint_data)

        return crawling_params

    def crawl(self, crawling_params, options):
        _logger.info(
            "{0}: Crawling param [{1}]".
                format(CRAWLER_NAME, crawling_params))

        ###### The Crawler logic to crawl the data using the crawling params

        # DEMO
        num_loops = 3
        while num_loops:
            sleep(5)
            _logger.info(
                "{0}: Still crawling data for param [{}]...".
                    format(CRAWLER_NAME, crawling_params))
            num_loops -= 1