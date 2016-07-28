import petl


def will_change(o1, o2):
    '''
    Given two lists of data (a row) both in the same order check to see if the two lists are equal.
    :param o1: First list of data (row)
    :param o2: Second list of data (row)

    :return: True if the two lists are different, False if they are the same
    '''
    v = zip(o1, o2)
    for i in v:
        if i[0] != i[1]:
            return True
    return False


def new_update_stale_keys(source, existing):
    '''
    Given a list of primary keys in the data source and a list from the current data
    return 3 lists, new keys, keys possibly needing updates and stale keys which exist in the db but not in the source.
    :param source: A list of keys from the data source (incoming data)
    :param existing: A list of keys from the data currently in the DB

    :return: A tuple (new, update, stale) where 
        - new are any keys that exist in the source but not the existing lists
        - update are keys that exist in both lists
        - stale are keys from existing that do not appear in the source
    '''
    new = [s for s in source if s not in existing]
    stale = [e for e in existing if e not in source]
    update = [u for u in source if u in existing]
    return (new, update, stale)


def records_for_update(source, existing, update_keys, key='id', source_key=None, existing_key=None):
    '''
    Return a petl compatible list of data which represents any source rows whose keys appear in update_keys
    and whose data is different from the corresponding row in existing.

    :param source: A petl table of source data
    :param existing: A petl table of existing data
    :param update_keys: A list of keys prefiltered to include only those keys that _could_ be source_update_candidates
    :param key: The name of the primary key field
    '''
    if source_key is None and existing_key is None:
        source_key = existing_key = key

    source_update_candidates = petl.transform.select(source, lambda rec: rec[source_key] in update_keys).lookup(source_key)
    existing_update_candidates = petl.transform.select(existing, lambda rec: rec[existing_key] in update_keys).lookup(existing_key)

    to_update = [petl.header(source)]
    for k, source_rec in source_update_candidates.items():
        existing_rec = existing_update_candidates[k]
        if will_change(source_rec, existing_rec):
            to_update.append(source_rec)
    return to_update


def extract_column(table, column):
    '''
    Return a list of all values minus the header row for a given petl table
    :param table: A  petl data table
    :param column: The name of the column to extract
    '''
    a = petl.cut(table, column)
    return [i[0] for i in a][1:]
