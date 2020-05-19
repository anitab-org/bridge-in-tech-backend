from flask_restx import Api, Resource

api = Api(
    title="Bridge In Tech API",
    version="1.0",
    description="API documentation for the backend of Bridge In Tech. \n \n"
    + "Bridge In Tech is an application inspired by the existing AnitaB.org Mentorship System, "
    + "It encourages organizations to collaborate with the mentors and mentees on mentoring programs. \n \n"
    + "The main repository of the Backend System can be found here: https://github.com/anitab-org/bridge-in-tech-backend \n \n"
    + "The Android client for the Mentorship System can be found here: https://github.com/anitab-org/bridge-in-tech-web \n \n"
    + "For more information about the project here's a link to our wiki guide: https://github.com/anitab-org/bridge-in-tech-backend/wiki"
    # doc='/docs/'
)
# api.namespaces.clear()

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


api.add_resource(Ping, '/ping')