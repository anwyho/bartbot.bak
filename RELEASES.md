# Releases

This change log tries its best to follow [Semantic Versioning](semver). Since this is not a library, I tried to apply the recommendations from this [Stack Exchange post](seRecs).

[semver]: https://semver.org/
[seRecs]: (https://softwareengineering.stackexchange.com/questions/255190/how-does-semantic-versioning-apply-to-programs-without-api)

## [Unreleased]

### To Be Added

* Support for BART API through a [pybart](pybart) session
* Concurrency and multi-threading!
  * Classes made response times slower

## [1.0.0] - 2018-MM-DD

* Anticipating 1.0 release! Getting ready to ship it :shipit:

### Notes

* The 1.0.0 release will come with the ability to query the BART API
  * As a result, it won't be reached until my project [pybart](pybart) is finished

[pybart]: https://github.com/anwyho/pybart/

## [0.8.1] - 2018-11-DD

### Todo

* Phrases
  * `get_phrase()` is not very smooth to use
* Tests!

## [0.8.0] - 2018-11-14

### Added

* **Basic functionality!**
  * Bartbot now knows how to handle basic arrival and departure trip requests
* Wit processing class
  * Entities are processed in initialization

### Changed

* Typing and seen indicators are now handled in the controller rather than for all events

### Removed

* Refactored much of the `receive` module to cut bulk of preprocessing time before handling actual message contents

## [0.7.1] - 2018-10-30

### Removed

* Deprecated events and phrases packages

## [0.7.0] - 2018-10-29

### Notes

* This was a **big release**. I've been working on a separate branch called `organize_classes` and today is the day that it was pushed.
* *Why is this a big release?* If you look through the files, the structure is way more organized.
  * I implemented classes very heavily, so now there are Messages and Responses.
  * A Controller class now facillitates Messages and Responses.
  * Almost everything is abstracted
    * **Bartbot can easily become ____bot.**
    * Another goal I had was to use Bartbot as a framework for mass producing other bots.
  * UX development just got a lot more ergonomic with all the Template and Button classes available.
* I also deleted deprecated files in the `clean_deprecated` branch.

### Added

* Classes make flow of processing much easier
  * Comes at cost of slower responses
* New phrases (e.g. 'wait')
* Response and ResponseBuilders
  * Allow for quick response creation
* Template and Button

### Changed

* Phrases is now a class
  * Still needs work for ergonomics of creating phrases
* Getting a map now uses generators and has a different force-refresh option

### Deprecated

* Previously, events used procedural processing
  * Efficient but messy and not good for scaling
* Old phrases module is deprecated in favor of newer and abstracted phrases module
  * Old tests for phrases module are only half-deprecated since they still need to be reimplemented

### Updated

* FB Graph API version was updated from v2.6 to v2.7

### Security

* Requests is updated to v2.20.0 for HTTP vs. HTTPS things

## [0.6.2] - 2018-09-11

### Notes

* From now on, I'll be more conscious of contributing to versions and patches. I'm still learning and hope to be an expert at managing projects soon!
* Also, much of the research has been completed. In the near future I will be focusing on implementation and pushing towards the final product. The goal is to reach v1.0.0 by October! :octocat:

### Added

* This file [RELEASES.md](.) wow so meta
* Changed [`get_phrases`](./bartbot/utils/phrases/phrase.py) to format phrases based on an options dictionary `opt`
* Changed default amount of memory for Lambda function in [`serverless.yml`](./serverless.yml) from 1024MB to 512MB

### Changed

* Updated Messenger Profile scripts
  * Added debugging webhook for running specific scripts
  * Experimented with persistent menu function
* Added tests related to locales to phrase tests
* Reorganized URLs in readme and simplified shortcuts to links

## [0.6.1] - 2018-09-10

### Added

* Created boilerplate code for different locale phrases

### Changed

* Lots of readme updates
  * Outlined entire program stack
* Connected `phrases.py`, `locales.py`, and `emoji.py`

### Fixed

* Local write for map attachment ID was throwing errors in Lambda
  * Removed local write

## [0.6.0] - 2018-09-07

### Added

* Support for multiple locales in the future
  * Added modules specifically for English and other languages (Spanish, Chinese, Japanese)
  * Changed Wit.ai NLP to process for English specifically
* `logging.shutdown` for flushing logs

### Changed

* Polished and added more details for how to load [`set_env_vars`](./bartbot/scripts/set_env_vars) script

## [0.5.1] - 2018-09-06

### Added

* BASH script for adding AWS Parameter Store variables to environment ([`set_env_vars`](./bartbot/scripts/set_env_vars))

### Changed

* Toggling seen and typing indicators for post-message
* Reorganized keys for local environment access
* Moved all phrases into a dict
* Moved challenge handling into webhook module
  * It's too simple to need its own module
* Renamed `tests` directory to `test`

## [0.5.0] - 2018-09-05

### Added

* Emojis are finally here!
* Added keyword handling
* Created tests for emoji module

## [0.4.2] - 2018-09-04

### Added

* Added `__init__.py` files to submodules
* Pylint dependency for development
* Created non-shell scripts for updating Messenger Profile API
* Added Wit Setup script for later implementation

### Changed

* BART map moved to online GitHub raw content for Messenger saved assets
* Converted most `str.format`ed strings to `f-strings`
* Updated `serverless.yml`
  * Deploy without dev dependencies
  * Exclude pycache and tests

## [0.4.1] - 2018-09-03

### Changed

* Map delivery process
* Updated `serverless.yml` to have correct main function name
* Added some functions to implement

### Fixed

* HACK: Prevented `get_phrase` from returning incorrectly substituted phrases
  * Creates significnant hang time in specific cases (`while` loop with RNG exit)

## [0.4.0] - 2018-09-02

### Added

* Sends map when detected by Wit API
* Excluded files from Serverless packaging
* Wrote cURL tests for localhost
* Uploaded BART map
* Much more logging for debugging purposes
* unittest testing modules for `phrases.py`

### Changed

* Changed `src/**` package root to `bartbot/**`
* Updated git ignore

## [0.3.1] - 2018-09-01

### Added

* Python logging package
* Python typing for static type checking
* Added different phrases for responses
* Simple message handling and response

### Changed

* Serverless app name
* Finalized webhook challenge handling
* Moved keys and authentication process to its own file `src/keys.py`
* Isolated webhook endpoint and moved all functions out to more dedicated modules
* Made message processing more robust
* Begin adding error checking

## [0.3.0] - 2018-08-31

### Added

* New Python handler written with Flask and Requests
* Integrated Serverless framework for AWS Lambda
* GitHub pages
* Added POSTs to Messenger API for seen and typing indicators

### Changed

* Updated readme and git ignore
* Boiled down imports
* Improved file structure

### Deprecated

* Zappa is no longer used after this patch
* Bottle is no longer used after this patch

### Fixed

* AWS Lambda response with new handler

### Removed

* Removed Bottle and Zappa support (even though it was deprecated in this release as well)

## [0.2.3] - 2018-08-22

## Changed

* Reorganized files and keys
* Updated readme and git inore

### Removed

* Pybart support - migrated to its own [repository](https://github.com/anwyho/pybart/)

## [0.2.2] - 2018-08-18

### Changed

* Refreshed keys and put them into a new location

## [0.2.1] - 2018-08-16

### Added

* Initial Pybart commit (BART API Python endpoint)

## [0.2.0] - 2018-08-15

### Added

* Zappa for easy Lambda serverless configuration
* Bottle framework for handling requests
* Moved keys to environment variables

### Changed

* File organization logic

### Deprecated

* Python Flask handler switched out for Python Bottle

## [0.1.1] - 2018-08-14

### Added

* git ignore
* Bash scripts for updating Lambda handler and S3 buckets (5d2d3856)

### Changed

* (Naively) unified all keys into a file (without encryption)

### Deprecated

* Node.js + Request handler no longer supported - switched to Python Flask
* Node modules removed from source code

## [0.1.0] - 2018-08-11

### Added

* Handler for AWS Lambda

### Changed

* Readme and functions to implement

## [0.0.5] - 2018-08-07

### Changed

* Readme, API keys, and functions to implement

## [0.0.4] - 2018-08-01

### Added

* API key support

## [0.0.3] - 2018-07-30

### Changed

* Readme and functions to implement

## [0.0.2] - 2018-07-28

### Added

* License
* Contribution guideline
* List of functions to implement
* `updateStations.py` calls BART API to store station list as JSON in `/resources`
* Read [Readme Driven Development](http://tom.preston-werner.com/2010/08/23/readme-driven-development.html) and decided to work on [`README.md`](./README.md) more

## [0.0.1] - 2018-07-25

### Added

* Started [`README.md`](README.md)
* Initialized environment and initial dependencies

<!-- Categories for headers
`Added` for new features.
`Changed` for changes in existing functionality.
`Deprecated` for once-stable features removed in upcoming releases.
`Removed` for deprecated features removed in this release.
`Fixed` for any bug fixes.
`Security` to invite users to upgrade in case of vulnerabilities.
-->

