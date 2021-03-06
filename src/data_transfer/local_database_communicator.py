#!/usr/bin/env python3
# Copyright (c) 2019 FRC Team 1678: Citrus Circuits
"""Holds functions for database communication.

All communication with the MongoDB local database go through this file.
"""

import re

from pymongo import MongoClient

from data_transfer.database import Database
import utils

DB = Database()


def get_collection_name(path):
    """Gets the new corresponding collection name

    path is the old path to the dataset
    Returns what the collection is now called
    """
    # Matches raw collections (e.g. raw_qr, raw_obj_pit)
    if raw_pattern := re.fullmatch(r'raw\.(.*)', path):
        return 'raw_' + raw_pattern[1]
    # Matches calc collections (e.g. obj_tim, tba_team)
    if calc_processed_pattern := re.fullmatch(r'processed\.calc_(.+)', path):
        return calc_processed_pattern[1]
    # subj_aim and uncle tim doesn't match the above because old version did not begin with 'calc'
    if processed_pattern := re.fullmatch(r'processed\.(.+)', path):
        return processed_pattern[1]
    print(f'Could not convert {path} to new collection name using {path} instead')
    return path


def read_dataset(path, **filter_by):
    """Filters by filter_by if given, or reads entire dataset.

    path is a string in dot notation showing which fields the data is under
    (eg. 'raw.obj_pit').
    competition is the competition code. **filter_by is of the form foo=bar
    and is the key value pair to filter data by.
    """
    return DB.find(get_collection_name(path), filter_by)


def select_tba_cache(api_url):
    """Finds cached tba data from MongoDB.

    If cache exists, returns data. If not, returns None.
    api_url is the url that caches are stored under, competition is the competition code.
    """
    return DB.get_tba_cache(api_url)


def overwrite_tba_data(data, api_url):
    """Overwrites data in a tba cache under an api url.

    data is the new data to add. api_url is the url to add it under.
    competition is the competition key.
    """
    # Takes data from tba_communicator and updates it under api_url
    DB.update_tba_cache(data, api_url)


def remove_data(path, **filter_by):
    """Removes the document containing the specified filter_bys.

    path is a string showing where data is located,
    filter_by is a kwarg that show data points in the document.
    """
    # Creates dictionary to contain the queries to apply to the specified path
    DB.delete_data(get_collection_name(path), filter_by)


def append_to_dataset(path, data):
    """Extends the dataset given by path with the data given by data

    'path' is the path to the dataset, (e.g. 'raw.qr', 'processed.calc_obj_tim'), use dot notation.
    'data' is the data to append to the dataset, must be a list.
    'competition' is the TBA event key.
    """
    DB.insert_documents(get_collection_name(path), data)


def update_dataset(path, new_data, query):
    """Updates a single dictionary within a dataset, if the query matches a dictionary within a
    dataset, replace the data given, if it does not exist create a new dictionary and add the query
    and data given by function parameter

    'path' is the path to the dataset, (e.g. 'raw.qr', 'processed.calc_obj_tim'), use dot notation.
    'data' is the data to either add, or to replace if the query matches in the dataset, must be a
    dictionary.
    'query' is a query to search through the given datset for the first occurence within a
    dictionary.
    'competition' is the tba event key.
    """
    # Update one document within the specified collection
    # Adds a document comprised of the query and the update data when no document is found
    DB.update_document(get_collection_name(path), new_data, query)


def add_competition(client) -> None:
    """Adds indexes into competition collections"""
    DB.set_indexes()
