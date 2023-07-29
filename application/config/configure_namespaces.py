from flask import Blueprint
from flask_restx import Api


def configure_namespaces(blueprint: Blueprint, *namespaces):
    '''Accepts an Api rest_x object as well as a flask blueprint and connects them.

        Args:
            blueprint: Our root blueprint to be connected to our Api object.
            namespaces(Namespace): All of the namespaces that we want to attach to our Api.
    '''
    api = Api(
        blueprint,
        title="Orodha List Service"
    )
    if namespaces:
        for namespace in namespaces:
            api.add_namespace(namespace)
