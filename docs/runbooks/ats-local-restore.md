# Runbook: run the HR Guru ATS locally (macOS)

The production ATS ran on AWS EC2 (Nginx, Waitress, Flask, PostgreSQL, Cloudflare DNS at `ats.hrgp.in`). That host was torn down. This runbook brings it back on the Mac with Docker, and makes it reachable for 25 recruiters.

## 0. Before you start: what data do we have?

| Source | Where it might be | Use procedure |
|---|---|---|
| PostgreSQL dump (`pg_dump`) of `hrguru_ats` | EC2 snapshot, S3, a laptop download | **B1** (preferred) |
| EBS volume snapshot of the old EC2 | AWS console → EC2 → Snapshots | Attach, copy `/var/lib/postgresql`, or `pg_dump` it → **B1** |
| Legacy SQLite `ats.db` | `/Users/surindersingh/Coding/ats/ats.db` or an old Windows copy `D:\hrguru-ats` | **B2** (data may be older than production) |
| Uploaded CVs/JDs (`uploads/`) | EC2 snapshot, local copies | Copy into the `ats-uploads` volume (step C) |
| Nothing | — | **B3** fresh, empty ATS |

> Production had ~3,600 candidates and ~400 requirements (knowledge base §9). Check counts after restoring.

## A. One-time setup
1. Install and start Docker Desktop. Settings → Resources: memory ≥ 6 GB.
2. In the repo root, create the root env file and set `ATS_DB_PASSWORD`:

```bash
cp .env.example .env
```

3. Create the ATS env file and set `SECRET_KEY`, `ADMIN_PASSWORD`, and the Google/Gmail values if used:

```bash
cp apps/ats/.env.example apps/ats/.env
```

4. Start the database:

```bash
docker compose up -d ats-db
```

## B. Load data (choose one)

**B1. From a PostgreSQL dump** (start the database first: `docker compose up -d ats-db`)

```bash
docker compose exec -T ats-db pg_restore -U hrguru -d hrguru_ats --no-owner < hrguru_ats.dump
```

(For a plain `.sql` dump use `psql -U hrguru -d hrguru_ats` instead of `pg_restore`.)

**B2. From a legacy SQLite `ats.db`** (the HR Guru case: the file is on the MacBook).
`scripts/restore_from_sqlite.sh` works on a **copy** of the file, so the original is never changed. It:
- upgrades the copy to the current ATS schema;
- migrates every table into the empty PostgreSQL database;
- prints row counts and the newest record dates.

It refuses to run if the database already has ATS tables. It runs **inside the ATS container**, so it needs no Python on the Mac and no host port.

1. Back up the original file first:

```bash
cp /Users/surindersingh/Coding/ats/ats.db ~/ats-backup-$(date +%Y%m%d).db
```

2. Build the ATS image:

```bash
docker compose build ats
```

3. Run the restore. This also starts `ats-db`; the file is mounted read-only:

```bash
docker compose run --rm -v /Users/surindersingh/Coding/ats/ats.db:/restore/ats.db:ro ats scripts/restore_from_sqlite.sh /restore/ats.db
```

4. Check the printed counts against the last known production figures (about 3,600 candidates and 400 requirements). Also check the **newest created_at** dates: production moved from SQLite to PostgreSQL around May–June 2026, so anything entered after that move is not in `ats.db`. Record the result in TS-EA-04.

Existing users and passwords come across with the data, so recruiters log in as before.

**B3. Fresh, empty ATS.** This refuses to run if tables already exist:

```bash
docker compose run --rm -e PYTHON=python ats scripts/bootstrap_empty_postgres.sh
```

## C. Restore uploaded files (if you have them)

```bash
docker compose run --rm -v /path/to/old/uploads:/restore:ro ats sh -c 'cp -a /restore/. /app/uploads/'
```

## D. Start and verify

```bash
docker compose up -d ats
```

```bash
curl -s http://localhost:5001/healthz
```

Then log in at http://localhost:5001 as `admin` and check the candidate and requirement counts.

## D2. Logins

**Password login (works immediately).** Accounts and passwords come from the restored data. To see them, or to reset a password (it is asked for with a hidden prompt):

```bash
docker compose run --rm ats python scripts/manage_users.py list
```

```bash
docker compose run --rm ats python scripts/manage_users.py set-password admin
```

**Google login.** On first Google sign-in, the ATS creates an account automatically for any team member whose email is in Team Members. That is why the restore has only a few accounts. To enable it:

1. In Google Cloud Console → APIs & Services → Credentials, open the existing **OAuth 2.0 Client ID** used for `ats.hrgp.in`, or create one of type *Web application*. This is free.
2. Under **Authorised redirect URIs**, add both:
   - `http://localhost:5001/login/callback` (local use)
   - `https://ats.hrgp.in/login/callback` (recruiters, after section E)
3. Put the client ID and secret into `apps/ats/.env` (`GOOGLE_CLIENT_ID=`, `GOOGLE_CLIENT_SECRET=`).
4. Recreate the container so it reads the new values:

```bash
docker compose up -d --force-recreate ats
```

Until this is done, the Google button shows *"Google login is not configured"* instead of Google's error page.

## E. Make it reachable for recruiters: Cloudflare Tunnel (free, no open ports)

The tunnel container makes an **outbound** connection to Cloudflare. Cloudflare serves `https://ats.hrgp.in` (with a certificate) and forwards requests to the `ats` container. No router port forwarding and no public IP are needed.

**E1. Free up the hostname.** In the Cloudflare dashboard, go to `hrgp.in` → DNS → Records. Delete the old **A** record for `ats` that points to the torn-down EC2 IP. If there is an old `hireflow` tunnel CNAME you no longer use, delete it too.

**E2. Create the tunnel.** In Zero Trust (free plan), go to Networks → Tunnels → **Create a tunnel** → type **Cloudflared**, named `hrguru-ats`. On the install screen, choose *Docker* and copy only the **token**: the long string after `--token`.

**E3. Add the public hostname.** In the same wizard (Public Hostname tab):
- Subdomain `ats`, domain `hrgp.in`, path empty
- Service type `HTTP`, URL `ats:5001` (the container name on the compose network, not localhost)

**E4. Give the token to compose.** In the root `.env` add `CLOUDFLARE_TUNNEL_TOKEN=<token>`. It is git-ignored; never commit it.

**E5. Point the ATS at its public URL.** In `apps/ats/.env` set:
- `PUBLIC_BASE_URL=https://ats.hrgp.in`
- `PREFERRED_URL_SCHEME=https`
- `GOOGLE_REDIRECT_URI=https://ats.hrgp.in/login/callback`

Make sure that redirect URI is in the Google OAuth client's list. Then recreate the ATS:

```bash
docker compose up -d --force-recreate ats
```

**E6. Start the tunnel:**

```bash
docker compose --profile live up -d tunnel
```

```bash
docker compose logs --tail 20 tunnel
```

Look for `Registered tunnel connection` (normally 4 lines). The tunnel then shows **Healthy** in the dashboard.

**E7. Verify** from a phone on mobile data (not office Wi-Fi):
- `https://ats.hrgp.in/healthz` returns `"ok":true`.
- Google login and password login work.

**E8. Recommended hardening (free for up to 50 users): Cloudflare Access.** The ATS is a legacy app with known weaknesses (R-15), and the tunnel makes it reachable from the whole internet. In Zero Trust → Access → Applications, add a *Self-hosted* app for `ats.hrgp.in` with a policy that allows only HR Guru emails (Google or one-time PIN). Recruiters then pass a Cloudflare login before the ATS login. If external client users also use the ATS, add their emails or domains to the policy.

**E9. Keep the Mac serving during working hours:**
- Docker Desktop → Settings → General → *Start Docker Desktop when you sign in*.
- System Settings → Battery/Energy → *Prevent automatic sleeping when the display is off* (on power adapter).
- All ATS containers use `restart: unless-stopped`, so they come back after a reboot once Docker starts.

## F. Backups (do not skip: the last outage lost the host)

Scripts are in `ops/backup/`:
- **`backup_ats.sh`** writes three files to `BACKUP_DIR`, then optionally copies them to `OFFSITE_DIR` and deletes copies older than `KEEP_DAYS`:
  - `pg_dump` of the database (compressed);
  - an archive of the uploaded CVs and JDs;
  - SHA-256 checksums.

  If the database dump is empty or the off-Mac folder is missing, it fails loudly and shows a macOS notification.
- **`restore_drill.sh`** restores the newest backup into a **scratch** database, compares row counts with the live database, and drops the scratch copy. The live database is only read.
- **`install_schedule.sh`** installs a launchd job that runs the backup every day at 21:00. If the Mac is asleep then, the job runs when it wakes.

**Setup (once):**
1. Create a settings file and set `OFFSITE_DIR` to a folder that is **not only on this Mac**: a Google Drive or iCloud Drive folder that syncs to the cloud, or an external disk.

```bash
cp ops/backup/backup.env.example ops/backup/backup.env
```

2. Run a backup now and check the result:

```bash
ops/backup/backup_ats.sh
```

3. Prove that the backup restores:

```bash
ops/backup/restore_drill.sh
```

4. Schedule it nightly:

```bash
ops/backup/install_schedule.sh
```

5. **macOS permission for cloud folders.** A scheduled (background) job cannot open Google Drive, iCloud or OneDrive folders until you allow it. Go to System Settings → Privacy & Security → **Full Disk Access** → **+** → Cmd+Shift+G → `/bin/bash`, and turn it on. Without this the scheduled run fails with *"macOS blocked access …"*, even though running the script by hand works.

6. Test the scheduled run once:

```bash
launchctl kickstart gui/$(id -u)/in.hrgp.ats-backup && sleep 30 && tail -n 10 ~/Library/Logs/hrguru-ats-backup.log
```

**Current setup (2026-11-28):** the off-Mac copy goes to Google Drive `My Drive/HRGuruBackups`. First backup and restore drill passed (9,988 candidates, 1,685 requirements). The scheduled run is verified.

**Monthly:** run `restore_drill.sh` and note the result in Jira (TS-14).

To restore for real after a disaster, use procedure **B1** with the newest `hrguru_ats-*.dump`, then procedure **C** with the matching `uploads-*.tgz` (extract it first).

## G. Known limits of running on a laptop
Single point of failure (sleep, reboot, travel, power). RAM is shared with TalentScout's local LLM, so avoid heavy model runs during working hours. Logged as risk R-12. Revisit hosting when budget allows.
