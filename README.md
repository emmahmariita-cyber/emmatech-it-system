# EmmaTech IT Management System

A command-line user management and security-monitoring system built in Python
as a hands-on cybersecurity practice project.

## Features
- Role-based access control (Admin / User)
- Password hashing with per-user salts (PBKDF2-SHA256)
- Password strength enforcement
- Account lockout after 3 failed login attempts
- Timestamped activity logging
- Security report that flags suspicious login activity
- Input validation

## Security concepts demonstrated
Authentication, access control, hashing and salting, logging and monitoring,
brute-force detection, incident response.

## How to run
    python3 main.py

## Documentation
See `docs/incident-report.md` for a simulated brute-force incident investigation.

## Limitations and future work
- Data stored in a JSON file (a real system would use a database)
- No multi-factor authentication
- No network alerting

## Author
Emma Mariita, Information Security and Forensics (BSc, KCA University)