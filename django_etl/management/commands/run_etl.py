import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError, DataError, connection
from django.core.management import BaseCommand

from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--only', nargs='*',
                            help='Only run the pipeline at this path/s.')

    def handle(self, *args, **options):
        self.options = options
        self.args = args
        self._output('Processing run_etl management command', 3)
        apps = getattr(settings, 'INSTALLED_APPS')
        self._output('Found django apps: {}'.format(apps), 2)
        for app in apps:
            self._output('Processing app: {}'.format(app), 3)
            try:
                self._output('Looking for pipeline definitions in app: {}'.format(app), 3)
                pipelines = import_string('{}.etl.pipelines'.format(app))
                self._output('Found {} pipelines for app {}'.format(len(pipelines), app), 3)
            except ImportError as e:
                logger.warning('Could not find any django_etl pipelines in {}'.format(app))
                logger.debug(e)
                self._output('Could not find any pipelines in {}'.format(app), 3)
                continue

            for pipeline in pipelines:
                qual_path = pipeline.__module__ + '.' + pipeline.__name__
                self._output('Processing pipeline at {}'.format(qual_path), 2)
                if options['only'] is not None:
                    if qual_path not in options['only']:
                        self._output('Skipping pipeline {} because it was not specified in the --only option'.format(qual_path), 1)
                        continue
                name = pipeline.__name__
                p = pipeline()
                logger.info('Running django_etl pipeline {}'.format(name))
                p.setup()
                logger.debug('Completed setup() for django_etl pipeline {}'.format(name))
                p.extract()
                logger.debug('Completed extract() for django_etl pipeline {}'.format(name))
                p.transform()
                logger.debug('Completed transform() for django_etl pipeline {}'.format(name))
                p.load()
                logger.debug('Completed load() for django_etl pipeline {}'.format(name))
                p.teardown()
                logger.debug('Completed teardown() for django_etl pipeline {}'.format(name))

    def _output(self, msg, verbosity=1):
        if self.options['verbosity'] >= verbosity:
            self.stdout.write(msg)


