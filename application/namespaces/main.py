"""Module containing the main namespace as well as a test hello world route."""
from flask_restx import Namespace, Resource

main_ns = Namespace(
    "Default",
    description="The main namespace",
    path="/main"
)

@main_ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
	    return "Hello World"
