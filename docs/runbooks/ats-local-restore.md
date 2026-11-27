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

**B1. From a PostgreSQL dump**

```bash
docker compose exec -T ats-db pg_restore -U hrguru -d hrguru_ats --no-owner < hrguru_ats.dump
```

(For a plain `.sql` dump use `psql -U hrguru -d hrguru_ats` instead of `pg_restore`.)

**B2. From a legacy SQLite `ats.db`** (the HR Guru case: the file is on the MacBook).
`scripts/restore_from_sqlite.sh` works on a **copy** of the file, so the original is never changed. It:
- upgrades the copy to the current ATS schema;
- migrates every table into the empty PostgreSQL database;
- prints row counts and the newest record dates.

It refuses to run if the database already has ATS tables.

1. Back up the original file first:

```bash
cp /Users/surindersingh/Coding/ats/ats.db ~/ats-backup-$(date +%Y%m%d).db
```

2. One-time Python setup for the ATS tools (from the repo root):

```bash
cd apps/ats && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

3. Restore into the `ats-db` container. Use the `ATS_DB_PASSWORD` from your root `.env`:

```bash
DATABASE_URL="postgresql://hrguru:YOUR_ATS_DB_PASSWORD@127.0.0.1:5433/hrguru_ats" PYTHON=.venv/bin/python scripts/restore_from_sqlite.sh /Users/surindersingh/Coding/ats/ats.db
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

## E. Make it reachable for recruiters (no public IP needed, free)
Use a **Cloudflare Tunnel**. The domain `hrgp.in` is already on Cloudflare, and a tunnel was used before (`hireflow.hrgp.in`).

```bash
brew install cloudflared
```

```bash
cloudflared tunnel login
```

```bash
cloudflared tunnel create hrguru-ats
```

```bash
cloudflared tunnel route dns hrguru-ats ats.hrgp.in
```

```bash
cloudflared tunnel run --url http://localhost:5001 hrguru-ats
```

Then:
- In Google Cloud console → OAuth client, keep the redirect URI `https://ats.hrgp.in/login/callback`.
- Set `PUBLIC_BASE_URL=https://ats.hrgp.in` and `PREFERRED_URL_SCHEME=https` in `apps/ats/.env`.
- Keep the Mac awake during working hours: System Settings → Battery/Energy → prevent sleep on power adapter, or run `caffeinate -s` in a terminal.

## F. Backups (do not skip: the last outage lost the host)
Nightly at 21:00 via launchd (TS-EA-06): `pg_dump -Fc` plus a tar of `ats-uploads`. Keep 14 copies locally and copy them to a second location (external disk or Google Drive). Do a restore drill monthly using procedure B1 into a scratch database.

## G. Known limits of running on a laptop
Single point of failure (sleep, reboot, travel, power). RAM is shared with TalentScout's local LLM, so avoid heavy model runs during working hours. Logged as risk R-12. Revisit hosting when budget allows.
