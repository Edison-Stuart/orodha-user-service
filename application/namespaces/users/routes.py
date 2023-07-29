from flask_restx import Namespace, Resource

user_ns = Namespace(
    "users",
    description='User related operations',
    path="/user"
    )

# class SomeResource(Resource):
