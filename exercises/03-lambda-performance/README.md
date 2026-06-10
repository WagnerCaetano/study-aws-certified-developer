# Exercise 03: Lambda Performance

## Problem
Optimize the Lambda function for better cold start performance.

The function should:
1. Initialize AWS SDK clients OUTSIDE the handler
2. Use connection reuse patterns
3. Handle timeouts gracefully

## Running
```bash
python runner.py exercises/03-lambda-performance
```
