# File System Overview

This document describes how the file system of the repo is organized.

```
tree -R -L 5 -d
source
├── Team_Documentation
│   ├── Team_1
│   ├── Team_2
│   └── Team_3
├── database
├── deploy_tools
└── group1
    ├── comm
    │   ├── migrations
    │   ├── static
    │   └── templates
    ├── communication
    │   ├── django
    │   │   ├── comm
    │   │   │   ├── migrations
    │   │   │   └── templates
    │   │   └── group2
    │   └── node
    │       ├── node_modules
    │       └── test
    ├── group1
    ├── issue_tracker
    │   ├── management
    │   │   └── commands
    │   ├── migrations
    │   ├── static
    │   │   ├── css
    │   │   ├── fonts
    │   │   ├── images
    │   │   ├── js
    │   │   └── libs
    │   └── templates
    ├── project_router
    │   ├── migrations
    │   ├── static
    │   └── templates
    ├── requirements
    │   ├── migrations
    │   ├── models
    │   ├── static
    │   │   ├── bootstrap
    │   │   ├── bs-datetimepicker
    │   │   ├── css
    │   │   ├── images
    │   │   ├── img
    │   │   ├── js
    │   │   ├── projects
    │   │   └── sb-admin
    │   ├── templates
    │   ├── templatetags
    │   ├── tests
    │   └── views
    ├── selenium_tests
    │   ├── issue_tracker
    │   ├── project_router
    │   └── requirements
    └── unit_tests
        ├── chat
        ├── issue_tracker
        ├── project_router
        └── requirements

95 directories
```