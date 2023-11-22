#!/bin/bash

uwsgi --socket 0.0.0.0:5433 --protocol=http -w wsgi:app
