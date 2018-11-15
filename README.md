# :light_rail:  Bartbot

*Oh shoot.*

***You, yelling*** *into your phone as you sprint from your Prius*:

> Do I need to run to catch the Bayfair train to Powell?

***Bartbot***:

> **4 min** until the next train from **Bayfair to Powell**. Smell the roses - but not for too long. :rose:

***You***, *taking a moment to catch your breath*:

> :sunglasses:

## :thought_balloon:  Motivation

<!-- TODO: This section is not done yet -->

"Should I run to catch the train?" This was the main question that I wanted to answer with Bartbot.

I have always wanted to make some sort of quick access to the BART API but didn't know where to start developing. Then one day, as I looked for open-source projects to contribute to, I found some examples of Facebook Messenger chatbots! It was then that I became super inspired to create my own chatbot. Thus, Bartbot was born.

Being able to message (or even speak) to BART about the next trains seemed like such a convenient idea. So far, I've learned an incredible amount, since this project covers so much!

Things Bartbot taught me:

* Writing libraries
  * Semantic Versioning
  * Readme-Driven Development
* Logging & debugging
* Package logistics
* RESTful APIs
  * All the protocols
  * How to design them and how to call them
  * Key/secret management
* Object Oriented Programming
  * Not the theoretical stuff they teach you in school
  * Inheritance is amazing
* Functional Programming
  * Concurrency comes by design
  * It isn't always useful to run concurrently
* Serverless programming
* Natural language processing
* NoSQL databases

## :gift:  Implementation

<!-- TODO: This section is not done yet -->

I went through plenty of design iterations for how to structure the code, but I have settled with the stack below:

* [Facebook Messenger](messenger)
  * Periodic GET requests for challenge (verify my webhook is online)
  * POST requests for messages and postback events
* [Amazon Web Services](aws)
  * [botocore](boto)
  * [Lambda](lambda)
    * Hosts my Serverless Flask application
  * [API Gateway](apigateway)
    * Exposes a RESTful API endpoint for my Lambda function
  * [S3](s3)
    * Hosts user data, sessions, and caches
  * [Systems Manager/Parameter Store](parameterstore)
    * Houses my secrets like API keys and the lot
* [Wit.ai](wit)
  * Natural language processing for requests
* [Python 3.6](python3)
  * [Serverless Framework](serverless)
    * Handles AWS configurations to set up Lambda and API Gateway
    * Originally, I went with [Zappa](zappa). It seemed pretty well done but ultimately didn't work for Bartbot.
  * [Flask](flask)
    * Routes HTTP requests within app
    * I was playing around with [Bottle](bottle) and [Zappa](zappa) in another iteration, but neither were functional enough for Bartbot.
  * [Requests](requests)
    * Makes HTTP requests easy-peasy
  * [unittest](unittest)
    * Testing testing testing! Helps with unit testing and some integration testing
  * [virtualenv](venv)
    * Configures development environment
    * I customized some of the BASH scripts to include adding environment variables
  * Have a look at the Python [requirements](requirements)
* [BART API](bartapi)
  * API endpoint for BART information
* Future Features
  * [Pybart](pybart) _(In Development)_
    * A Python library for accessing the BART API with caching
  * [Dark Sky](darksky) _(Future Support)_
    * API endpoint for weather information at specific stations
  * Transfer and arrival notifications
    * I've thought hard about how to implement these with AWS Lambda constraings (and even AWS Step Functions), but haven't come to any solid ideas yet, since neither can take the ~2hr longest trip (Antioch to Dublin Pleasanton). Please shoot me a message if you happen to have a work-around!
  * Increased use of concurrency (even though I'm working in Python)
    * I can easily see implementing futures

<!-- emoji test :smile: :monorail: :light_rail: :metro: -->

## :wrench: Set It Up

<!-- TODO: This section is not done yet -->

I will detail this section more at v1.0 release.

## :sparkles: Releases/Changelog

Ayy [check it](releases).

## :pray:  Contributing

<!-- TODO: This section is not done yet -->

I'm not sure if I'll be supporting contributors before v1.0, but watch the repo and see the [contributing guideline](contributing) if you're interested! It'll be soon.

Also, check out the [functions-to-implement checklist](toimplement).

## :trophy:  Acknowledgements

<!-- TODO: This section is not done yet -->

This is an awesome get-started article!

* [Run Node.js Facebook Messenger Chat Bot on AWS Lambda](nodetutorial) by [Igor Khomenko](khomenko)

This Serverless tutorial got my app up and running.

* [Serverless tutorial!](serverlesstutorial)

## :key:  Licensing

[GNU GLPv3](license) Copyright 2018, [Anthony Ho](gitprof).

<!-- https://kogalkbizj.execute-api.us-west-1.amazonaws.com/default/jsProcessMessages -->

> *Doot doot*, my dudes.

<!-- URLS -->

<!-- Stack -->
[apigateway]:         https://aws.amazon.com/api-gateway/
[aws]:                https://aws.amazon.com/
[bartapi]:            http://api.bart.gov/docs/overview/index.aspx
[boto]:               https://github.com/boto/botocore
[bottle]:             https://bottlepy.org/
[darksky]:            https://darksky.net/dev/
[gitprof]:            http://github.com/anwyho/
[lambda]:             https://aws.amazon.com/lambda/
[messenger]:          https://messenger.com/
[messengerapps]:      https://messenger.fb.com/
[parameterstore]:     https://aws.amazon.com/systems-manager/
[pybart]:             https://github.com/anwyho/pybart/
[python3]:            https://www.python.org/
[requests]:           http://docs.python-requests.org/en/master/
[s3]:                 https://aws.amazon.com/s3/
[serverless]:         https://serverless.com/
[unittest]:           https://docs.python.org/3/library/unittest.html
[venv]:               https://virtualenv.pypa.io/en/stable/
[wit]:                https://wit.ai/
[zappa]:              https://www.zappa.io/

<!-- Articles -->
[khomenko]:           https://tutorials.botsfloor.com/@igorkhomenko?source=post_header_lockup
[nodetutorial]: https://tutorials.botsfloor.com/run-facebook-messenger-chat-bot-on-aws-lambda-2fa800a67d76
[serverlesstutorial]:
                      https://serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb/

<!-- Repo References -->
[contributing]:       ./CONTRIBUTING.md
[license]:            ./LICENSE
[releases]:           ./RELEASES.md
[requirements]:       ./requirements.txt
[toimplement]:        ./functionsToImplement.md
