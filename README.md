# StrandsAgenticExamples

## Getting started

### Create new python venv
python3.13 -m venv .

### Activate
source ./bin/activate

### Install requirements
pip install -r requirements.txt

### Export secrets

> You only need to export the secrets that you'll personally test. If you don't have PagerDuty, skip it! You do need AWS creds to be able to run these agents, since they consume AI services from Bedrock to work. 

#### AWS
> export your AWS user and secret from SSO or for a User with a secret created. 

#### PagerDuty
export PAGERDUTY_USER_API_KEY='xxxxxxx' 

#### GitHub

> GitHub PAT which has at least read access
export GITHUB_TOKEN=ghp_xxxxx

#### AWS Bedrock Knowledge Base

> AWS Bedrock Knowledge Base if you have it
export AWS_REGION=us-west-2
export KNOWLEDGE_BASE_ID=XXXXXX
