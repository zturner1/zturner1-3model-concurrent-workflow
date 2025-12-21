# Style: Technical Planning

## Purpose
Breaking down technical tasks into actionable steps.

## Tone
Precise, practical, implementation-focused.

## Structure
1. Goal statement
2. Prerequisites/dependencies
3. Step-by-step plan (numbered)
4. Potential challenges
5. Success criteria

## Constraints
- Concrete, specific steps
- Include effort indicators (quick/moderate/complex)
- Note decision points
- Identify risks

## Example
> **Goal**: Set up automated backup for project context files
>
> **Prerequisites**:
> - Git installed and configured
> - GitHub/GitLab account
>
> **Steps**:
> 1. Create remote repository (quick)
> 2. Add remote to local git: `git remote add origin <url>`
> 3. Create backup script in `scripts/tools/backup.sh`
> 4. Add to cron/scheduled task (moderate)
>
> **Challenges**:
> - Credential management for automated push
>
> **Success Criteria**:
> - Daily automatic push to remote
> - Email notification on failure
