#!/usr/bin/env python
# coding: utf-8
"""Helper file for database functions."""
from app import db


def commit_entry(entry):
  """Commit an entry to the database and return a dictionary of the result."""
  try:
    db.session.commit()
    return {'status':True, 'message':u'Success', 'entry':entry}
  except Exception as e:
    error = str(e)
    # rollback the session in the event of an error
    db.session.rollback()
    return {'status':False, 'message':u'Error: %s' % unicode(error,'utf-8'), 'entry':None}


def delete_entry(entry):
  """Delete an entry from the database and return a dictionary of the result."""
  try:
    db.session.delete(entry)
    db.session.commit()
    return {'status':True, 'message':u'Success', 'entry':entry.id}
  except Exception as e:
    error = str(e).split('.')[0]
    if entry:
      return {'status':False, 'message':u'Error: %s' % unicode(error,'utf-8'), 'entry':entry.id}
    else:
      return {'status':False, 'message':u'Error: %s' % unicode(error,'utf-8'), 'entry':None}


def raise_error(error_message):
  """Deliberately raise an error back to the controller."""
  return {'status':False, 'message':error_message, 'entry':None}


def get_counts(field, order_by_count=False, limit=None):
  """Get count by specific field from a model.

  Get count by field passed as input
  Ex. get_counts(Supersource.source_property)
  returns a list of tuples that are (field, count)
  e.g [(1, 14), (2, 3)]
  (14 sources of property type 1, etc.)
  """
  query = db.session.query(field, db.func.count(field)).group_by(field)
  if order_by_count:
    query = query.order_by(db.func.count(field).desc())

  if limit:
    query = query.limit(limit)

  return query.all()


def build(query, with_entities=None, first=False):
  """Build a request to bring only specific columns back."""
  if with_entities:
    query = query.with_entities(*with_entities)
  if first:
    return query.first()
  else:
    return query.all()
