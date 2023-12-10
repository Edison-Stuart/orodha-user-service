"""Module which contains definition for user aggregation pipelines."""

def make_user_pipeline(keycloak_id: str):
    """
    Function which returns an aggregation pipeline to be used for
    obtaining id and username values of all users.

    Args:
        keycloak_id(str): The keycloak id of the requesting user. Used to obtain complete data
            for requesting user, while still returning censored data for other users.

    Raises:
        NotImplementedError: This function is not currently in use.

    Returns:
        mongo_pipeline: A custom pipeline used in the Document.objects().aggregate function.
    """
    raise NotImplementedError()
    # mongo_pipeline = [
    #     {
    #         "$project": {
    #             "dateCreated": 0,
    #             "firstName": 0,
    #             "lastName": 0,
    #             "email": 0,
    #         }
    #     }
    # ]
    # return mongo_pipeline
