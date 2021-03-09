 BridgeInTech Development Setup Instructions (Docker)

Before you start, you need to have the following installed:
- [Docker-desktop](https://www.docker.com/products/docker-desktop)

If you have these already installed, you are ready to start.

## 1st, Fork, Clone, and Remote
1. Follow the instruction on the [Fork, Clone, and Remote](https://github.com/anitab-org/bridge-in-tech-backend/wiki/Fork,-Clone-&-Remote) page for this step.

<!--This can be removed once the changes to the BIT branch have been merged-->
## 2nd, Clone mentorship-backend for BIT
1.Follow the instruction on the mentorship system [Fork, Clone, and Remote](https://github.com/anitab-org/mentorship-backend/wiki/Fork,-Clone-&-Remote) page for this step. Make sure the two projects are cloned in the same directory. 

## 3rd, Create .env file from .env.template 

You can ignore all the environment variables below flask_app(included) as they have already been set up in docker. <!--TODO add guide to environment variables--> 
 
## 4th running the app locally
Run the command `docker-compose up`.If you can use Makefiles then you can also run `make docker_dev`. If this is your first time it may take a while to download the images and get everything set up properly. Once this is complete you should be able to see the app running on http://localhost:5000 and the mentorship system running on http://localhost:4000. You can also connect to the Postgres server using `port 5432`.

## 5th Running test cases 
Run the command `docker-compose -f docker-compose.test.yml up --exit-code-from bit` to run the test cases. If you can use Makefiles then you can also run `make docker_test`. Linux and MacOS support make out of the box, but you can also use makefiles on windows by installing MinGW.




