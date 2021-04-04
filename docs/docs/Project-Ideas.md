---
id: Project-Ideas
title: Project Ideas
---

## Origin
BridgeInTech (BIT) was founded by Maya Treacy as an original project for AnitaB.org Open Source for a project submitted to Google Summer of Code 2020.

## Project Summary
Bridge In Tech is an application that allows industries/companies, mentors, and students to actively collaborate with one another. There is a backend written with Python and a Web application written in Javascript and React.

## Status
Web app at https://bridge-in-tech-web-heroku.herokuapp.com/

Backend API at https://bridgeintech-bit-heroku-psql.herokuapp.com/

## Repo Links
[Bridge In Tech (Backend)](https://github.com/anitab-org/bridge-in-tech-backend)
[Bridge In Tech (Web)](https://github.com/anitab-org/bridge-in-tech-web)

## Project ideas
### Backend + Frontend (full features)

| Idea | Description |
| ---- | ----------- |
| Users data service | Ideally there will be one single point to keep user data across all AnitaB Open Source Projects. Here we start with the Mentorship System (MS) and BridgeInTech (BIT). The service needs to have a single database that holds user data, a backend server which provides API endpoints for both MS and BIT on user related data, and a frontend web server which can be used by Admins of a particular project to manage their users data.
| Remote servers | At the moment there is a bottleneck on the Heroku remote servers for BridgeInTech application due to BIT complex architecture clashes with Heroku limited services on free tier option. Find a solution or alternative remote hosting to solve this issue on both backend and frontend.
| Forgot password | Allow user to reset their password on Login page if they forgot their password | 
| Deactivate account | Ability for a user to shut down an account, removing any sensitive data, while still keeping data integrity. This is very important if a user wishes to be removed from the app. |
| Third-party apps authentication (OAuth) | Authenticate using Slack, Facebook, Twitter, Google+, etc |
| App Admin API endpoints and Dashboard | Allow the BridgeInTech Admin user to manage other users, organisations and programs through a dashboard within the application | 
| Notifications | Define settings configuration for types and frequency of notifications the user receives / Different types of notifications: Push Notifications; Email and in-app notifications screen; |
| Apply to a program | Allow a user to apply to a program offered by an organization |
| Send Request to a mentor or mentee | Allow organization to request a mentor or mentee to work on their program |
| Alternative solution to keeping user token as Cookies | Currently on both backend and frontend, user token is saved as a cookie. As this may raise a security issue, a better solution to deal with user authentication is needed. |
| ... | ... | ... |

### Backend Only
| Idea | Description | Difficulty |
| ---- | ----------- | ---------- |
| Mentorship System and BridgeInTech code integration | Ensure BridgeInTech and Mentorship System can be fully integrated by applying BridgeInTech's Mentorship System related code base on the Mentorship System repository without breaking the existing features on both applications. | Medium |
| Add another representative to organization | Allow an Organization representative to add another user to become the organization representative to help manage programs | Medium |
| ... |	... | ... |

### Frontend Only
| Idea | Description |
| ---- | ----------- |
| User's portfolio page | Allow user to view a porfolio page (their own and other's) and see an overview of their/other's activities in BIT (programs involved, feedback from mentors/mentees, etc). |
| Implement redesign of the app | Implement redesign of the app to have a consistent design across screens and follow AnitaB.org branding styles |
| Organization Dashboard | Allow user who is a representative of an organization see an overview of the activities relevant to the programs their organization is offering. |
| Program's progress page | Allow user to see the progress of the program (ratio to completion, task/s status, etc) |
| ... | ... |


## Development Environment
#### Backend Development Environment

* Technologies Used: Python
* Difficulty: Novice to Intermediate

#### Web Development Environment

* Technologies Used: HTML, CSS, JavaScript, React
* Difficulty: Novice to Intermediate

## Communicate with Us on Zulip!
If you have an idea of how to improve Bridge In Tech, drop us a message on the #bridge-in-tech stream to discuss it :)