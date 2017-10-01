# Architecture Overview

This document describes the architecture of web-application.


```
                                                      ┌────────────────────────────────┐
                                                      │          Chat Server           │
                                                      │ ┌────────────────────────────┐ │
                                                      │ │* Node.js                   │ │
                                       ┌─────────────▶│ │* Websocket Interface       │ │
                                       │              │ │* Low latency               │ │
                                       │              │ │* Full-duplex communication │ │
                                       │              │ └────────────────────────────┘ │
                                       │              └────────────────────────────────┘
┌────────────────────────┐        Websocket                            ▲
│      Chat Client       │             │                               │
│   ┌────────────────┐   │             │                               │
│   │* Web interface │   │             │                               │
│   │* jQuery        │   │◀────────────┤                               │
│   │* Bootstrap     │   │             │                               │
│   │* socket.io     │   │             │                               │
│   └────────────────┘   │             │                               │
└────────────────────────┘             │                               ▼
                                       │              ┌────────────────────────────────┐
                                     HTTP             │             Django             │
                                       │              │     ┌─────────────────────┐    │
                                       │              │     │* Python             │    │
                                       │              │     │* Web framework (MVC)│    │
                                       └─────────────▶│     │* Authentication     │    │
                                                      │     │* Data model         │    │
                                                      │     │* Administration     │    │
                                                      │     └─────────────────────┘    │
                                                      └────────────────────────────────┘
                                                                       ▲
                                                                       │
                                                                       │
                                                                       │
                                                                       │
                                                                       ▼
                                                      ┌────────────────────────────────┐
                                                      │            Storage             │
                                                      │          ┌─────────┐           │
                                                      │          │* SQLLite│           │
                                                      │          │* MySQL  │           │
                                                      │          └─────────┘           │
                                                      └────────────────────────────────┘

Created with Monodraw
```