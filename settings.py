# -*- coding: utf-8 -*-
from oioioi.default_settings import *
import os.path
import django
print 'django path', django.__path__

# This should match INSTALLATION_CONFIG_VERSION in
# "oioioi/default_settings.py".
# Before you adjust it, you may consider visiting
# "https://github.com/sio2project/oioioi/#changes-in-the-deployment-directory".
CONFIG_VERSION = 22

# Enable debugging features.
#
# SET DEBUG = False FOR PRODUCTION DEPLOYMENT.
DEBUG = False

if DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = UNCACHED_TEMPLATE_LOADERS
else:
    # Cache compiled templates in production environment.
    TEMPLATES[0]['OPTIONS']['loaders'] = CACHED_TEMPLATE_LOADERS

# The APP_DIRS option is allowed only in template engines that have no custom
# loaders specified.
TEMPLATES[0]['APP_DIRS'] = False

# Site name displayed in the title and used by sioworkersd
# to distinguish OIOIOI instances.
SITE_NAME = 'XIV LO SIO2 - Docker'
SITE_ID = 1

# The website address as it will be displayed to users in some places,
# including but not limited to the mail notifications.
# Defaults to 'http://localhost'.
#PUBLIC_ROOT_URL = 'http://enter-your-domain-name-here.com'

# Email addresses to send error message reports.
ADMINS = (

)

# Sender email address for messages sent by OIOIOI to users.
DEFAULT_FROM_EMAIL = 'sio2@staszic.waw.pl'
DEFAULT_FROM_ADDRESS = DEFAULT_FROM_EMAIL

# Sender email address for error messages sent to admins.
SERVER_EMAIL = DEFAULT_FROM_EMAIL


# Email addresses to send communication from users (for example requests for
# teacher accounts).
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sio2',                      # Or path to database file if using sqlite3.
        'USER': 'sio2',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUESTS': True,         # Don't touch unless you know what you're doing.
    }
}

# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [os.environ['IP']]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/sio/deployment/media'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/sio/deployment/static'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '00000000-0000-0000-0000-000000000000'

# Uncomment once oisubmit is used.
#OISUBMIT_MAGICKEY = '__OTHER_SECRET__'

# SMTP server parameters for sending emails.
EMAIL_SUBJECT_PREFIX = '[SIO2] '
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# Comment to send user activation emails. Needs an SMTP server to be
# configured above.
SEND_USER_ACTIVATION_EMAIL = False

# RabbitMQ server URL for distributed workers.
#
# Uncomment once RabbitMQ is installed. By default SQLAlchemy is used,
# but this is unreliable and not intended for production.
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# Filetracker server settings.
#
# Determines which filetracker database use, availible options are:
# - 'oioioi.filetracker.client.media_root_factory' (the default)
#    Stores files on local filesystem under MEDIA_ROOT, optionally
#    exposing them with a filetracker server (see section below).
# - 'oioioi.filetracker.client.remote_storage_factory'
#    Connects to a filetracker server at FILETRACKER_URL, uses a local
#    cache with recently used files under CACHE_ROOT directory.
#FILETRACKER_CLIENT_FACTORY = 'oioioi.filetracker.client.media_root_factory'

# Uncomment the following lines to enable remote access to Filetracker. This is
# needed if you install separate judging machines. Beware -- there is no
# authorization mechanism in Filetracker. Everyone who can access the server on
# the given port will be able to see all the files. It's recommended to have
# the judging machines on a separate physical network and listen only on the
# corresponding IP address.
FILETRACKER_LISTEN_ADDR = '0.0.0.0'

# Uncomment and change this to run filetracker on non-default port.
FILETRACKER_LISTEN_PORT = 9999

# When using distributed workers set this to url on which workers will be
# able to access filetracker server. When 'remote_storage_factory' is used,
# this also defines the filetracker server oioioi should connect to.
FILETRACKER_URL = 'http://'+os.environ['IP']+':9999'

# When using a remote_storage_factory it's necessary to specify a cache
# directory in which a necessary files will be stored.
#FILETRACKER_CACHE_ROOT = '/home/sio/deployment/cache'

# When using a remote storage it's recommended to enable a cache cleaner deamon
# which will periodically scan cache directory and remove files what aren't
# used. For a detailed description of each option, please read a cache cleaner
# configuration section in the sioworkersd documentation. Please note that
# the cache cleaner can delete *any* file found under FILETRACKER_CACHE_ROOT
# directory, so don't store other files there (unless you want them to be
# periodically deleted).
FILETRACKER_CACHE_CLEANER_ENABLED = True
FILETRACKER_CACHE_CLEANER_SCAN_INTERVAL = '1h'
FILETRACKER_CACHE_CLEANER_CLEAN_LEVEL = '50'
FILETRACKER_CACHE_SIZE = '1G'

# The logs for one specific logger 'oioioi.zeus' will be
# stored in a specific file: `PROJECT_DIR/logs/zeus.log`.
LOGGING['handlers']['zeus_file'] = {
    'level': 'INFO',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': '/home/sio/deployment/logs/zeus.log',
    'maxBytes': 1024 * 1024 * 5, # 50 MB same as default in supervisord
    'backupCount': 10, # same as in supervisord
    'formatter': 'date_and_level',
}
LOGGING['loggers']['oioioi.zeus'] = {
    'handlers': ['zeus_file'],
    'level': 'DEBUG',
}

# On which interface should the sioworkers receiver listen. You should
# set the address to 0.0.0.0 if you want remote workers to access
# your server.
SIOWORKERS_LISTEN_ADDR = '0.0.0.0'
SIOWORKERS_LISTEN_PORT = 7890

# URL to which should respond sioworkersd, when it has finished its job
# When set to None the default url will be created using the pattern
# http://$SIOWORKERS_LISTEN_ADDR:$SIOWORKERS_LISTEN_PORT
SIOWORKERS_LISTEN_URL = "http://"+os.environ['IP']+":7890"

# Set this to false if you don't need sioworkersd instance (e. g.
# because you use instance started by another instance of OIOIOI)
RUN_SIOWORKERSD = True

# Contest mode - automatic activation of contests.
#
# Available choices are:
#   ContestMode.neutral - no contest is activated automatically,
# users have to explicitly enter into a contest specific page if they want
# to participate. They can visit both contest specific as well as non-contest
# specific pages.
#   ContestMode.contest_if_possible - if there exists a contest, users
# are automatically redirected to one when visiting a page which
# has a contest specific version, e.g. visiting index ('/') could redirect
# to "c" contest's dashboard page ('/c/c/dashboard') if there existed
# a contest "c". The contest picking algorithm is described in detail
# in oioioi.contests.middleware module.
# If a page requires that no contest is active (e.g. user's portal page
# from the "portals" app), it can still be visited and no redirection
# will be made.
#   ContestMode.contest_only - this setting is similar to the previous one
# except that pages requiring no contest to be active can only be visited
# by superusers (other users get "403 - Permission Denied").
#
# Some features may depend on this setting, e.g. the "portals" app requires
# that either the "neutral" or the "contest_if_possible" option is picked.
#
# The default setting is "contest_if_possible".
# To access the contest mode setting you also have to uncomment
# the following import line.
#from oioioi.contests.current_contest import ContestMode
#CONTEST_MODE =

# Similarly comment this out to disable workers running on the server machine.
#RUN_LOCAL_WORKERS = True

# Comment out the following options after you have downloaded the sandboxes
# with
#
#   manage.py download_sandboxes
#
# Before this only system compilers can be used and the safe execution
# supervisor is not available.
#USE_UNSAFE_EXEC = False #tu odk
#USE_LOCAL_COMPILERS = False #tu odk

# WARNING: setting this to False is experimental until we make sure that
# checkers do work well in sandbox
#
# Setting this to False will run checkers in sandbox. This option is
# independent to USE_UNSAFE_EXEC.
#USE_UNSAFE_CHECKER = True #tu odnk

# When USE_SINOLPACK_MAKEFILES equals True, the sinolpack upload workflow uses
# standard sinolpack makefiles, whose behaviour may be modified by a custom
# makefile.user file from a package. The makefiles' execution is not sandboxed,
# hence it should be disabled for untrusted contest admins.
# Whet it equals False, the upload workflow uses sioworkers for programs'
# execution (in a sandboxed environment, if USE_UNSAFE_EXEC is set to False).
USE_SINOLPACK_MAKEFILES = True

# Scorers below are used for judging submissions without contests,
# eg. submitting to problems from problemset.
# DEFAULT_TEST_SCORER = \
#     'oioioi.programs.utils.discrete_test_scorer'
# DEFAULT_GROUP_SCORER = \
#     'oioioi.programs.utils.min_group_scorer'
# DEFAULT_SCORE_AGGREGATOR = \
#     'oioioi.programs.utils.sum_score_aggregator'

#Upper bounds for tests' time [ms] and memory [KiB] limits.
MAX_TEST_TIME_LIMIT_PER_PROBLEM = 1000 * 60 * 60 * 30
MAX_MEMORY_LIMIT_FOR_TEST = 768 * 1024

# Controls if uwsgi in default configuration shall use gevent loop.
# To use it, you have to install gevent - please consult
# https://github.com/surfly/gevent
# This is recommended for heavy load, but you may still need to tune uwsgi
# options in deployment/supervisord.conf
UWSGI_USE_GEVENT = False

# EXTRA MODULES
#
# Comment/uncomment components to disable/enable them.
#
# Additional components usually have to be prepended to the list in
# INSTALLED_APPS, because they may want to override some templates. But this is
# not always the case. Please consult the documentation of particular extension
# you're configuring.
#
# Some components need also corresponding lines in TEMPLATE_CONTEXT_PROCESSORS
# and/or AUTHENTICATION_BACKENDS commented/uncommented.

INSTALLED_APPS = (
#     'oioioi.rankings',
#     'staszic.swimmingpool',
#     'staszic.timetable',
     'staszic.tree',
     'staszic.feedback',
     'staszic.queue',
     'staszic.utils',
     'staszic.limits',
     'staszic.reports',
     'staszic.extras',
     'staszic.languages',
     'staszic.python',
     'staszic.polygon',
#     'staszic.nasm',
     'staszic.rankings',
     'staszic.virtual',
     'staszic.archive',
     'staszic.sinol2pack',
    'oioioi.contestlogo',
#    'oioioi.avatar',
#    'oioioi.teachers',
#    'oioioi.ipdnsauth',
#    'oioioi.ipauthsync',
    'oioioi.participants',
    'oioioi.oi',
    'oioioi.contestexcl',
#    'oioioi.oisubmit',
#    'oioioi.zeus',
#    'oioioi.testrun',
    'oioioi.printing',
    'oioioi.scoresreveal',
#    'oioioi.oireports',
#    'oioioi.ontak',
#    'oioioi.complaints',
#    'oioioi.confirmations',
#    'oioioi.acm',
#    'oioioi.forum',
#    'oioioi.disqualification',
    'oioioi.sharingcli',
#    'oioioi.ctimes',
#    'oioioi.suspendjudge',
#    'oioioi.submitservice',
#    'oioioi.timeline',
#    'oioioi.amppz',
#    'oioioi.balloons',
#    'oioioi.statistics',
#    'oioioi.publicsolutions',
#    'oioioi.testspackages',
#    'oioioi.pa',
#    'oioioi.notifications',
#    'oioioi.prizes',
#    'oioioi.mailsubmit',
#    'oioioi.portals',
#    'oioioi.globalmessage',
#    'oioioi.newsfeed',
    'staszic.results_editor',
    'staszic.blog',
    'staszic.acl',
    'staszic.new_acm',
    'staszic.new_base',
    'staszic.timelimits',
    'staszic.showmodel',
) + INSTALLED_APPS

# Additional Celery configuration necessary for 'prizes' app.
if 'oioioi.prizes' in INSTALLED_APPS:
    CELERY_IMPORTS.append('oioioi.prizes.models')
    CELERY_ROUTES.update({
        'oioioi.prizes.models.prizesmgr_job': dict(queue='prizesmgr'),
    })

# Set to True to show the link to the problemset with contests on navbar.
PROBLEMSET_LINK_VISIBLE = True

# Comment out to show tags on the list of problems
#PROBLEM_TAGS_VISIBLE = True

# Set to True to allow every logged in user to add problems directly to Problemset
EVERYBODY_CAN_ADD_TO_PROBLEMSET = False

TEMPLATES[0]['OPTIONS']['context_processors'] += [
#    'oioioi.contestlogo.processors.logo_processor',
#    'oioioi.contestlogo.processors.icon_processor',
#    'oioioi.avatar.processors.gravatar',
#    'oioioi.notifications.processors.notification_processor',
#    'oioioi.globalmessage.processors.global_message_processor',
#    'oioioi.portals.processors.portal_processor',
]

MIDDLEWARE_CLASSES += (
#    'oioioi.ipdnsauth.middleware.IpDnsAuthMiddleware',
#    'oioioi.contestexcl.middleware.ExclusiveContestsMiddleware',
#    'oioioi.ipdnsauth.middleware.ForceDnsIpAuthMiddleware',
)

AUTHENTICATION_BACKENDS += (
#    'oioioi.teachers.auth.TeacherAuthBackend',
#    'oioioi.ipdnsauth.backends.IpDnsBackend',
)

# Number of concurrently evaluated submissions (default is 1).
#EVALMGR_CONCURRENCY = 30

# Number of concurrently processed problem packages (default is 1).
#UNPACKMGR_CONCURRENCY = 1

PROBLEM_SOURCES += (
    'staszic.polygon.problem_sources.PolygonProblemSource',
    'oioioi.sharingcli.problem_sources.RemoteSource',
#    'oioioi.zeus.problem_sources.ZeusProblemSource',
)

SHARING_SERVERS = (
#    ('site_url', 'sharing_url', 'client_id', 'client_secret'),
)

ZEUS_INSTANCES = {
#    'zeus_id': ('zeus_url', 'zeus_login', 'zeus_secret'),
}

# URL prefix (protocol, hostname and port)
# hit by the Zeus callback after a submission is judged
#ZEUS_PUSH_GRADE_CALLBACK_URL = 'https://sio2.dasie.mimuw.edu.pl'

# Complaints
#COMPLAINTS_EMAIL = 'email_to_send_complaints_to'
#COMPLAINTS_SUBJECT_PREFIX = '[oioioi-complaints] '

# Cache
# To use the more efficient memcached, install it and uncomment the following:
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}

# Notifications configuration (client)
# This one is for JavaScript socket.io client.
# It should contain actual URL available from remote machines.
#NOTIFICATIONS_SERVER_URL = 'http://localhost:7887/'

# Notifications configuration (server)
#NOTIFICATIONS_SERVER_ENABLED = True

# URL connection string to a Notifications Server instance
#NOTIFICATIONS_OIOIOI_URL = 'http://localhost:8000/'

# URL connection string for RabbitMQ instance used by Notifications Server
#NOTIFICATIONS_RABBITMQ_URL = 'amqp://localhost'

# Port that the Notifications Server listens on
#NOTIFICATIONS_SERVER_PORT = 7887

# Domain to use for serving IP to hostname mappings
# using ./manage.py ipauth-dnsserver
#IPAUTH_DNSSERVER_DOMAIN = 'oioioi.example.com'

# Error reporting
import raven

RAVEN_CONFIG = {
    # Won't do anything with no dsn
    # tip: append ?timeout=5 to avoid dropouts during high reporting traffic
    'dsn': '',
    # This should be a path to git repo
    'release': raven.fetch_git_sha(
        os.path.join(os.path.dirname(oioioi.__file__), os.pardir)),
}

# Bonus to judging priority ang judging weight for each contest on this
# OIOIOI instance.
#OIOIOI_INSTANCE_PRIORITY_BONUS = 0
#OIOIOI_INSTANCE_WEIGHT_BONUS = 0

UWSGI_ENABLE = 'yes'

INTERNAL_APPS_PREFIXES = [
    'oioioi.',
    'staszic.',
]

# LDAP

#AUTHENTICATION_BACKENDS = ('staszic.auth_ldap.backends.StaszicLDAPBackend', ) + AUTHENTICATION_BACKENDS

SUBMITTABLE_EXTENSIONS = {
        'C': ['c'],
        'C++': ['cpp', 'cc'],
        'Pascal': ['pas'],
        'Java': ['java'],
        'Python': ['py'],
}

CELERY_IMPORTS += [
    'staszic.polygon.importmgr',
]

CELERY_ROUTES.update({
    'staszic.polygon.importmgr.importmgr_job': dict(queue='importmgr'),
})

PROBLEM_PACKAGE_BACKENDS = ['staszic.sinol2pack.package.Sinol2PackageBackend'] + list(PROBLEM_PACKAGE_BACKENDS)

GOOGLE_RECAPTCHA_SECRET_KEY = ''

LOCALE_PATHS = ["/home/sio/staszic/locale", "/home/sio/oioioi/oioioi/locale"]

FEEDBACK_SERVER_PORT = 7899

SHARING_SERVERS = (
#    ('site_url', 'sharing_url', 'client_id', 'client_secret'),
)

MAX_TEST_TIME_LIMIT_PER_PROBLEM = 10*60*1000


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
            'date_and_level': {
                'format': '[%(asctime)s %(levelname)s %(process)d:%(thread)d]'
                          ' %(message)s',
            },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'date_and_level',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'emit_notification': {
            'level': 'DEBUG',
            'class': 'oioioi.base.notification.NotificationHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'oioioi': {
            'handlers': ['console', 'emit_notification'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

