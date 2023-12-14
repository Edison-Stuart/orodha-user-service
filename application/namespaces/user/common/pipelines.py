"""Module which contains definition for user aggregation pipelines."""

def obtain_bulk_user_pipeline(
    page_size: int=None,
    offset: int=None,
    targets: list=None) -> list:
    """
    Function which returns an aggregation pipeline to be used for
    obtaining id and username values of all users.

    Args:
        page_size(int): The number of documents to be returned
        offset(int): The number of documents to skip, giving us page size.
        targets(list): A list of username values that will be included
            in the search.

    Returns:
        mongo_pipeline: A custom pipeline used in the Document.objects().aggregate function.
    """
    base_mongo_pipeline = [
        {
            "$sort": {
                "dateCreated": -1
            }
        },
        {"$skip": offset},
        {"$limit": page_size},
        {
            "$project": {
                "dateCreated": 0,
                "firstName": 0,
                "lastName": 0,
                "email": 0,
            }
        }
    ]
    if targets:
        mongo_pipeline = [
        {
            "$match": {
                "username": {
                    "$in": targets
                }
            }
        }
        ] + base_mongo_pipeline
    else:
        mongo_pipeline = base_mongo_pipeline
    return mongo_pipeline
