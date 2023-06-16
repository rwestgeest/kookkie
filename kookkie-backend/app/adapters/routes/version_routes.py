from flask import jsonify
from .route_builder import RouteBuilder


class VersionRoutes:
    @staticmethod
    def create():
        return VersionRoutes()

    def register(self, app):
        route = RouteBuilder(app)
        version = read_version()

        @route('/api/version', methods=['GET'], login_required=False)
        def get_version():
            return jsonify(version=version), 200
  
        return route


def read_version():
    with open('VERSION') as f: 
        return f.read().strip()
