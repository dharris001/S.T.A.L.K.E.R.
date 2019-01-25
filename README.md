# S.T.A.L.K.E.R.

Application to track social media posts based on usernames with a goal to support a wide range of social channels. S.T.A.L.K.E.R. will scrape the supported social channels and return well formatted posts to a Slack webook for consumption.

### Motivation

This project was created as a learning exercise for Python, consuming REST APIs, and general application architecture and testing.

### Application Structure

`/services/runner.py` - Instantiates social classes based on social channel and calls required  
`/services/db.py` - Service for interacting with SQLite3 datastore  
`/services/slack.py` - Starts a webhook and parses Slack Event API messages  
`/services/commands.py` - Available commands for interacting with the app methods  
`/social` - Contains social classes with respective logic  
`/datastore` - Empty directory to bind sqlite3 docker data for persistence.  
`/main.py` - Entry point for Python

### Getting Started

###### Prerequisites

[Docker](https://www.docker.com/)

###### Setup

```
$ git clone git@github.com:MikeyDunn/S.T.A.L.K.E.R..git
$ cd S.T.A.L.K.E.R.
$ cp config_sample.yml config.yml
$ vi config.yml
// fill in your channels information
```

###### Commands

`Make build` - Create Docker image  
`Make run` - Run Stalker within Docker image  
`Make test` - Run Pytest within Docker image  
`Make shell` - Open Docker image at terminal

###### Supported Platforms

[Reddit](https://reddit.com) -
[Twitter](https://twitter.com) -
[Instagram](https://instagram.com)

### Author

Mike Dunn is a senior Front-end Developer with 5+ years of professional experience. Seeking to help deliver high quality applications through excellent coding practices and technical leadership. Specializing in semantics, optimization and system design.

### Contributors

[Levi Noecker](https://github.com/levi-rs)  
[Eric McBride](https://github.com/ericmcbride)
