#!/bin/bash

psql -U library_db_user library_db -qtc "drop table borrowings; drop table books_count; drop table books; drop table users;"
