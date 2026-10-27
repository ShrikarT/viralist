---
status: proposed
---
# Keep one domain model with a durable media worker

Use a React client and Python API/worker sharing PostgreSQL state, with private media storage and versioned provider adapters. A separate leased worker costs more setup than request-local tasks but permits restart recovery, deletion fencing and cost accounting; a PostgreSQL job table avoids adding a broker before workload evidence warrants one. Rejected alternatives are request-only serverless processing and a microservice per stage; provider choice and paid deployment remain unapproved.
