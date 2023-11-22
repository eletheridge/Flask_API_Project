#!/bin/bash

uwsgi --socket 0.0.0.0:5432 --protocol=http -w wsgi:app
