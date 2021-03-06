# Micheli Knechtel - GitHub Technical Interview

This repository was created as part of the gitHub technical interview for the **French-speaking** **Solutions Architect** position that falls under **Professional Services org**.

# ****Getting Started****

The technical solution consists of a ***WebHook*** that sends events and a ***WebService*** that listens to them.

- ***WebHook***:
    - Is configured at the organisation level and trigger an event when a repository is created.
- ***WebServer***:
    - Listen to repository event, and perform the following actions:
        - Creates a **readme.md** file, if it does not exist.
        - Sets protection of the default branch.
        - Add an issue with a @mention to outline that protection was added.

## Requirements

Have docker installed in your machine, also I’m assuming that you’re using **MacOs**.

## Repository content

This repository contains five files:
1. [Dockerfile](https://github.com/miknechtel/interview/blob/main/Dockerfile) used to create the webserver container image.
2. [README.md](https://github.com/miknechtel/interview/blob/main/README.md) file that has the detailed description of this project.
3. [app-config.properties](https://github.com/miknechtel/interview/blob/main/app-config.properties) file where you can find user, password and token.
4. [app.py](https://github.com/miknechtel/interview/blob/main/app.py) is where you have all definitions of routes and functions to perform for each action.
5. [gitHub Technical Exercise.postman_collection.json](https://github.com/miknechtel/interview/blob/main/gitHub%20Technical%20Exercise.postman_collection.json) postman file which has all the HTTP requests that can be performed against the web server.
6. [presentation.pdf](https://github.com/miknechtel/gitInterview/blob/main/presentation.pdf) material that I will use to present myself and my project.

## Installation guidelines

1. You need to pull the image from my docker hub :
    
    ```bash
    docker pull micheliknechtel/webserver-micheli:latest
    ```
    
2. Install Ngrok to exposes container server.
    
    ```bash
    # for more information, have a look at https://ngrok.com/download 
    brew install ngrok/ngrok/ngrok
    ```
    

## ****Executing program****

As the technical solution consistes in two components: GitHub and WebServer application, first you need to start the web server, following the steps described in section **Server side**. 

Once the web server is running, you need to login into GitHub with my user and password, provided in file [app-config.properties](https://github.com/miknechtel/interview/blob/main/app-config.properties). 

Finally, to run the entire workflow, you need to create a new repository under knechtelOrganizaton, to do so, follow the steps described in **GitHub** section. 

*Alternatively, if you have postman installed in your computer, you can use the file blabla to import the HTTP request, so you can run queries against the server from Postman.* 

### Server side

1. Create a container from the image webserver-micheli
    
    ```bash
    docker run --name webserver-micheli -p 5000:5000 webserver-micheli
    ```
    
2. In the command line, expose port 5000 using Ngrok 
    
    ```bash
    # expose port 5000
    ngrok http 5000
    ```
    

### GitHub

1. Update the webhook with the payload url generated by Ngrok, to do so use the following link https://github.com/organizations/knechtelOrganization/settings/hooks/352393074
2. Create a public repository under knechtelOrganization to do so use the following link https://github.com/knechtelOrganization
3. Verify that you have an entrie in issue saying that the protection was added to the branch
4. Check if the protection branch is setup correctly, for more information please see the link https://docs.github.com/en/github-ae@latest/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/managing-a-branch-protection-rule#editing-a-branch-protection-rule  


## Additional commands

If you wanna create your own image using the Dockerfile provide by me, make sure that the files: [Dockerfile](https://github.com/miknechtel/interview/blob/main/Dockerfile), [app.py](https://github.com/miknechtel/interview/blob/main/app.py) and  [app-config.properties](https://github.com/miknechtel/interview/blob/main/app-config.properties) are in the same folder, so you can use the steps bellow.

```bash
# go to the directory where you have all the files mentioned above
cd [your_directory]
 
# if you wanna create your own image using the dockerFile provide
docker image build -t [your_image_name]

# to create a container from your brand new image
docker run -p 5000:5000 -d [your_image_name]

# if you wanna get inside of container to have a look
docker container exec -it [your_container_id] sh

# ah, to know the container id
docker ps -a
```

## **References**

[Creating a new organization from scratch - GitHub Docs](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/creating-a-new-organization-from-scratch)

[Creating webhooks - GitHub Docs](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks)

[Installation - Flask Documentation (2.1.x)](https://flask.palletsprojects.com/en/2.1.x/installation/)

[ngrok - download](https://ngrok.com/download)

[Welcome to Python.org](https://www.python.org/about/)
