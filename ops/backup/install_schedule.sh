#!/usr/bin/env bash
# Install (or update) the macOS launchd job that runs backup_ats.sh every day at 21:00.
# If the Mac is asleep at 21:00, launchd runs the job when it wakes.
# Usage: ops/backup/install_schedule.sh        Remove: ops/backup/install_schedule.sh --remove
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
LABEL=in.hrgp.ats-backup
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/hrguru-ats-backup.log"
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
if [ "${1:-}" = "--remove" ]; then rm -f "$PLIST"; echo "Removed $LABEL"; exit 0; fi
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"
cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$HERE/backup_ats.sh</string></array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>21</integer><key>Minute</key><integer>0</integer></dict>
  <key>EnvironmentVariables</key><dict><key>PATH</key><string>/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin:/usr/bin:/bin:/usr/sbin:/sbin</string></dict>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
PLIST
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Installed $LABEL: daily 21:00. Log: $LOG"
echo "Run it now to test:  launchctl kickstart gui/$(id -u)/$LABEL && sleep 20 && tail -n 20 $LOG"
