import os
import re

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import connections, transaction
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ....point.models import Point, PointPhoto


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Reset database started ...')

        dbconfig = settings.DATABASES['default']
        connection = connections['default']
        cursor = connection.cursor()

        try:
            cursor.execute('DROP DATABASE `%s`' % dbconfig['NAME'])
            print('Drop old database "%s".' % dbconfig['NAME'])

            print('Create new databse "%s" ...' % dbconfig['NAME'])
            cursor.execute('CREATE DATABASE `%s` CHARACTER SET=utf8 COLLATE=utf8_unicode_ci' % dbconfig['NAME'])

            connection.close()
        except Exception as ex:
            print('ERROR: "%s"' % ex)

        call_command('makemigrations', 'point')
        call_command('migrate')

        self.create_group('Store planner')
        self.create_group('Manager')

        print('Reset database completed.')

    def create_group(self, name):
        new_group, created = Group.objects.get_or_create(name=name)

        for _model in [Point, PointPhoto]:
            for perm in ['add', 'delete', 'update', 'view']:
                ct = ContentType.objects.get_for_model(_model)
                permission, _is_new = Permission.objects.get_or_create(codename='can_%s' % perm,
                                                                       name='Can %s %s' % (perm, _model.__name__),
                                                                       content_type=ct)
                new_group.permissions.add(permission)
        return new_group


def install_inital(sql_files, con='default'):
    connection = connections[con]
    cursor = connection.cursor()

    statements = re.compile(r';[ \t]*$', re.M)

    for sql_file in sql_files:
        file_path = os.path.join(settings.BASE_DIR, sql_file)
        if os.path.exists(file_path):
            f = open(file_path, 'U', encoding='utf8')

            for statement in statements.split(f.read()):
                statement = re.sub(r'--.*([\n\\Z]|$)', '', statement)

                if statement.strip():
                    try:
                        cursor.execute(statement)
                        transaction.commit(using=con)
                        print('Installing initial file: %s' % sql_file)
                    except Exception as ex:
                        print('Error: %s' % ex)
                        print('Could not install initial file: %s' % sql_file)
            f.close()
        else:
            print('Could not find initial file: %s' % sql_file)
