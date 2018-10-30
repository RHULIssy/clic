# The full project path
PROJECT_PATH ?= $(shell git rev-parse --show-toplevel)
# The project directory name
PROJECT_NAME ?= $(notdir $(PROJECT_PATH))

include $(PROJECT_PATH)/local-conf.mk

# Project mode, development/production
PROJECT_MODE ?= development

# Set PROJECT_REV from a tag on head, or if that fails (branch):(sha)
PROJECT_REV = $(shell git describe --exact-match HEAD 2>/dev/null || true)
ifeq ($(PROJECT_REV),)
    PROJECT_REV = $(shell git rev-parse --abbrev-ref HEAD):$(shell git rev-parse --short HEAD)
endif

###################
# Configuration options for serving client

WWW_SERVICE_NAME ?= $(PROJECT_NAME)
WWW_SERVER_NAME ?= $(shell hostname --fqdn)
ifeq ($(PROJECT_MODE),development)
    WWW_UWSGI_CACHE_ZONE ?= off
else
    WWW_UWSGI_CACHE_ZONE ?= api_cache
endif
WWW_UWSGI_TIMEOUT ?= 5m
WWW_UWSGI_API_CACHE_TIME ?= 60m

###################
# Configuration options for running API server

API_SERVICE_FILE ?= /etc/systemd/system/$(PROJECT_NAME).service
ifeq ($(PROJECT_MODE),development)
    # Default to user that checked out code (i.e the developer)
    API_USER ?= $(shell stat -c '%U' $(PROJECT_PATH)/.git)
    API_GROUP ?= $(shell stat -c '%U' $(PROJECT_PATH)/.git)
else
    API_USER ?= nobody
    API_GROUP ?= nogroup
endif
API_SOCKET ?= /tmp/$(PROJECT_NAME)_uwsgi.$(PROJECT_MODE).sock
API_UWSGI_PROCESSES ?= 4
API_UWSGI_THREADS ?= 4
API_UWSGI_HARAKIRI ?= 0
API_UWSGI_CACHE_SIZE ?= 1g

###################
# DB configuration options

# The user that has root access to DB
DB_SUDO_USER ?= postgres
# The hostname / socket path to connect to
DB_HOST ?= /var/run/postgresql/
# The DB to create
DB_NAME ?= $(shell echo -n $(PROJECT_NAME) | sed 's/\W/_/g')_db
# The credentials that the app will use
DB_USER ?= $(API_USER)
# The credentials that the app will use
DB_PASS ?=

###################

# Anything depending on conf.mk should be rebuilt on commits / local-conf.mk changes
$(PROJECT_PATH)/conf.mk: \
    $(PROJECT_PATH)/local-conf.mk \
    ../.git/logs/HEAD
	touch $(PROJECT_PATH)/conf.mk

# Create empty local-conf.mk if it doesn't exist
$(PROJECT_PATH)/local-conf.mk:
	[ -e $(PROJECT_PATH)/local-conf.mk ] || touch $(PROJECT_PATH)/local-conf.mk

.EXPORT_ALL_VARIABLES:
