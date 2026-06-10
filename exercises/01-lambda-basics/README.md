# Exercise 01: Lambda Basics

## Problem
Fix the Lambda handler to properly process API Gateway events.

The function should:
1. Parse the JSON body from the event
2. Extract the `name` field
3. Return a proper response with statusCode 200
4. Handle missing `name` with a 400 error

## Running
```bash
python runner.py exercises/01-lambda-basics
```
