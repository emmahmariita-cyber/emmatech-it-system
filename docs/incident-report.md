# Incident Report: Brute-Force Login Attempt

**Date:** (sep 30, 2026)
**Reported by:** Security report (automated log analysis)
**Severity:** Medium
**Status:** Resolved

## Summary
Multiple failed login attempts were detected against the account `brian`,
resulting in automatic account lockout.

## Timeline
(jack@patnar-communications-limited:~/emmatech-it-system$ cat activity.log
2026-09-30 16:00:40 | USER_CREATED | Emma Nyanduko | first admin setup
2026-09-30 16:01:09 | LOGIN_SUCCESS | Emma Nyanduko | role=Admin
2026-09-30 16:02:46 | USER_CREATED | Emma Nyanduko | created Emma Mariita as User
2026-09-30 16:03:44 | USER_CREATED | Emma Nyanduko | created Samantha Waraba as User
2026-09-30 16:08:44 | LOGOUT | Emma Nyanduko | 
2026-09-30 16:09:06 | LOGIN_FAILED | Emma Mariita | attempt 1 of 3
2026-09-30 16:09:27 | LOGIN_FAILED | Emma Mariita | attempt 2 of 3
2026-09-30 16:09:41 | LOGIN_FAILED | Emma Mariita | attempt 3 of 3
2026-09-30 16:09:41 | ACCOUNT_LOCKED | Emma Mariita | too many failed attempts
2026-09-30 16:10:08 | LOGIN_SUCCESS | Emma Nyanduko | role=Admin
2026-09-30 16:10:45 | ACCOUNT_UNLOCKED | Emma Nyanduko | unlocked Emma Mariita
2026-09-30 16:12:09 | LOGOUT | Emma Nyanduko | 
jack@patnar-communications-limited:~/emmatech-it-system$ )

## Analysis
- Three consecutive failed logins in a short period.
- The account lockout control triggered as designed.
- The security report flagged the account as suspicious.

## Actions taken
1. Confirmed the lockout in the activity log.
2. Verified with the account owner that the attempts were not legitimate.
3. Unlocked the account and required a password change.

## Recommendations
- Add alerts for repeated failures across many accounts.
- Add multi-factor authentication.
- Add a time-based lockout in place of a permanent lock.