from flask import Flask, request, jsonify
import requests
import json
import base64
import time
from jproperties import Properties

app = Flask(__name__)



configs = Properties()
with open('app-config.properties', 'rb') as config_file:
    configs.load(config_file)
    
gitUser = configs.get("git-User").data
gitPassword = configs.get("git-Password").data  
githubToken = configs.get("github-Token").data

protectionMessageOK = 'Branch protection turn on {0:s}'
protectionMessageKO = 'Could not turn on branch protection {0:s}'

issuesMessageKO = 'Could not create mention in issue {0:s}'
issuesMessageOK = 'Mention successfully created in issue {0:s}'


urlContentsFoundation = "https://api.github.com/repos/knechtelOrganization/{}/contents/README.md"
urlProtectionFoundation = "https://api.github.com/repos/knechtelOrganization/{}/branches/main/protection"
urlIssuesFoundation = "https://api.github.com/repos/knechtelOrganization/{}/issues"


myHeaders = {"Authorization": "token " + githubToken,"Accept":"application/vnd.github.luke-cage-preview+json"}
branchProtection ='{"required_status_checks": null,"enforce_admins": null,"required_pull_request_reviews" : {"dismissal_restrictions": {},"dismiss_stale_reviews": false,"require_code_owner_reviews": true,"required_approving_review_count": 1},"restrictions":null}'

issueMessage = '{"title":"Webook set master branch protection rules","body":"@miknechtel set default respository settings and protected the master branch."}'
readmeConfiguration = '{"message": "my commit message",  "sender_login": {"name": "miknechtel","email": "micheliknechtel@icloud.com"}, "content":"'+ base64.b64encode(b'data to be encoded').decode('ascii') +'"}'

    
@app.route('/payload', methods=['POST'])
def webhook():
	if request.headers.get('X-GitHub-Event') == "ping":
		print('This is a ping event and happens when a webhook is created for the first time!')
	else :
		if request.headers.get('X-GitHub-Event') == "repository":
			# payload parsing	
			requesteData = request.get_json(force=True)
			reposName=requesteData["repository"]["name"]

			urlProtection = urlProtectionFoundation.format(reposName) 
			urlIssues = urlIssuesFoundation.format(reposName) 
			urlContents = urlContentsFoundation.format(reposName) 
		
			# creating session 
			session = requests.Session()
			session.auth = (gitUser, gitPassword)
		
			# check if there is a README.md and if not creates one 
			readmeExist(urlContents, reposName, myHeaders)
		
			# wait a little to make sure file is create when needed
			time.sleep(3)
			# adding to the master branch protection rules
		
			protectionResponse = requests.put(urlProtection, data=branchProtection, headers=myHeaders)
			requestCheck(protectionResponse, reposName, protectionMessageOK, protectionMessageKO, 200)
		
			# adding a issue with @mention to document the branch protection rules change
			issuesResponse = requests.post(urlIssues, data=issueMessage, headers=myHeaders)
			requestCheck(issuesResponse, reposName, issuesMessageOK, issuesMessageKO, 201)
	return 'ok'   

def requestCheck(requestResponse, reposName, messageOK, messageKO, code):
    if requestResponse.status_code == code:
        print (messageOK.format(reposName))
    else:
        print (messageKO.format(reposName))
        print ('Response:', requestResponse.content)
        print ('Code status', requestResponse.status_code)
        
def readmeExist(urlContents, reposName, myHeaders):
    contentResponse = requests.get(urlContents,headers=myHeaders)
    if contentResponse.status_code == 200:
        print ('ok'.format(reposName))
    else:
    	createResponse = requests.put(urlContents, data=readmeConfiguration, headers=myHeaders)


if __name__ == "__main__":
    app.run(host="0.0.0.0")






