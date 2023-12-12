"""Module which contains definition for user aggregation pipelines."""

def obtain_bulk_user_pipeline(
    page_size: int=None,
    page_number: int=None,
    targets: list=None) -> list:
    """
    Function which returns an aggregation pipeline to be used for
    obtaining id and username values of all users.

    Args:
        page_size(int): The number of documents to be returned
        page_number(int): The page of documents to be returned
        targets(list): A list of username values that will be included
            in the search.

    Returns:
        mongo_pipeline: A custom pipeline used in the Document.objects().aggregate function.
    """

    if page_size is None:
        page_size = 10
    if page_number is None or page_number == 1:
        page_number = 1
        offset = 0
    else:
        offset = (page_size * page_number) - page_size

    if targets is None:
        mongo_pipeline = [
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
    else:
        mongo_pipeline = [
        {
            "$match": {
                "username": {
                    "$in": targets
                }
            }
        },
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
    return mongo_pipeline
