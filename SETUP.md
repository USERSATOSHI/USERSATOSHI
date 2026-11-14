# Install and schedule your profile

Copy the complete contents of this package into the root of `USERSATOSHI/USERSATOSHI`, including the hidden `.github` folder, and commit them to the default branch. It includes the README, assets, Python build scripts, and source data.

Open **Actions → Update profile → Run workflow** once to check the setup. After that, it runs on the first day of each month at **07:47 IST / 02:17 UTC**. Scheduled runs use the workflow on the default branch; GitHub may start them later than the scheduled minute.

To run daily instead, edit `.github/workflows/update-profile.yml`:

```yaml
schedule:
  - cron: '17 2 * * *'
```

Monthly uses `17 2 1 * *`. Keep only one active cron line. Both schedules support the manual **Run workflow** button.

## What gets updated

Each run fetches the rolling GitHub contribution calendar, the four selected repositories' star counts, and commits attributed to USERSATOSHI on their default branches. It updates the snapshot date, renders the slash calendar, and rebuilds the linked project cards and footer. It commits generated assets and data only after validation passes. The finished portrait and banner composition are reused; there are no AI calls or image-generation fees.

The workflow uses the automatic `GITHUB_TOKEN` for commits, with `contents: write`. Repository rules must permit that bot to push to the default branch. If direct pushes are blocked, use your repository's permitted PR process rather than bypassing its rules.

Public data reads use `PROFILE_READ_TOKEN`, falling back to an existing `METRICS_TOKEN`, then `GITHUB_TOKEN`. Try the manual run first. If your automatic token cannot read user contribution data or the upstream repositories, create a repository Actions secret named `PROFILE_READ_TOKEN` with access to public GitHub GraphQL data. A classic personal access token with no selected scopes can read public information. Private-repository access is unnecessary for this public profile. Never put a token in a file.

A failed fetch or render does not commit partial artwork. Overlapping runs are serialized. Pushes are ordinary pushes; a conflicting remote update fails safely. GitHub can disable scheduled workflows in public repositories after 60 days without repository activity; re-enable the workflow in Actions if needed.

## Rebuild locally

Install Python 3, GitHub CLI (`gh`), `rsvg-convert`, FFmpeg, ImageMagick (`magick` or `convert`), Liberation fonts and DejaVu fonts. Authenticate `gh`, then run from the repository root:

```sh
python3 build/refresh_data.py
python3 build/build_calendar.py
python3 build/build_animation.py
python3 build/build_clickable.py
python3 build/build_about.py
python3 build/validate_profile.py
```

To render the saved snapshot offline, omit the refresh command. Generated frame directories are ignored by Git.

## Artwork and data definitions

The banner/calendar are static PNGs. Each whole project card links to its repository and has a 12-second, 48-frame corner-brightness pulse, varying only from 94% to 100% opacity. Mobile layouts and reduced-motion stills are included. The slash calendar uses one glyph per day, sized logarithmically by the actual contribution count. Desktop shows the full calendar and mobile the latest 26 weeks; both display the full-period total.

The supplied portrait was recoloured/masked with ImageMagick and then AI-cleaned with permission for anti-aliasing and line continuity. Its original credit area was restored. Both versions are included. Static bidirectional vector masks provide inversion and small refractive offsets while excluding the face. The cleanup prompt is recorded in `AI-CLEANUP-PROMPT.txt`.

Stars belong to the upstream project. Commit figures count commits attributed to USERSATOSHI on the upstream default branch; they are not merged-PR counts. aoi.js and Gutenberg are upstream contributions; Kouro and Kasanome are personal projects. The selected projects remain fixed across refreshes.

References: [GitHub scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [automatic token permissions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication), [personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
