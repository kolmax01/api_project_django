"""
prevents from starting django without db
"""
import time
from typing import Any

from psycopg2 import OperationalError as PsycopgOp2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgOp2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 sec...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available'))
