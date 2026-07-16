#!/usr/bin/env bash
# check-summary-tally.sh <report.md>
#
# Asserts a writing-requirements report's Summary counts reconcile with the
# body tagged-line counts, the invariant added after run 2's MD-6 finding:
#   - Info Resolved cell        == number of [INFO] lines
#   - Info Resolved cell        == report-level Outstanding info figure
#   - Warning Resolved cell     == number of [WARNING-RESOLVED] lines
#   - Warning Unresolved cell   == number of [WARNING-UNRESOLVED] lines
#   - Blocking Resolved cell    == number of [BLOCKING-RESOLVED] lines
#   - Blocking Unresolved cell  == number of [BLOCKING-UNRESOLVED] lines
#
# Deterministic, disk-only, no skill run. Exit 0 = pass, 1 = reconciliation
# failure, 2 = usage/lookup error. Built from grep/sed only.

set -u
report="${1:?usage: check-summary-tally.sh <report.md>}"
[ -f "$report" ] || { echo "FAIL: report not found: $report"; exit 2; }

# Body counts: one tagged finding per line.
info_body=$(grep -c '\[INFO\]' "$report")
warn_res_body=$(grep -c '\[WARNING-RESOLVED\]' "$report")
warn_unres_body=$(grep -c '\[WARNING-UNRESOLVED\]' "$report")
block_res_body=$(grep -c '\[BLOCKING-RESOLVED\]' "$report")
block_unres_body=$(grep -c '\[BLOCKING-UNRESOLVED\]' "$report")

# Summary cells. In each row the first integer is Resolved, the second is
# Unresolved. An N/A cell yields no integer, so Info returns only its Resolved.
row_nums() { grep -E "^\| *$1 " "$report" | grep -oE '[0-9]+'; }
info_sum=$(row_nums Info | sed -n 1p)
warn_res_sum=$(row_nums Warning | sed -n 1p)
warn_unres_sum=$(row_nums Warning | sed -n 2p)
block_res_sum=$(row_nums Blocking | sed -n 1p)
block_unres_sum=$(row_nums Blocking | sed -n 2p)

# Report-level Outstanding info: the info figure on the last Outstanding line.
out_info=$(grep 'Outstanding:' "$report" | sed -n '$p' | grep -oE '[0-9]+ info' | grep -oE '[0-9]+')

fail=0
chk() { # label  summary-value  body-value
  if [ "${2:-}" = "${3:-}" ]; then
    printf '  ok    %-26s %s\n' "$1" "${2:-<empty>}"
  else
    printf '  FAIL  %-26s summary=%s body=%s\n' "$1" "${2:-<empty>}" "${3:-<empty>}"
    fail=1
  fi
}

echo "Summary-reconciles-body: $report"
chk "Info resolved = [INFO]"   "$info_sum"        "$info_body"
chk "Info = Outstanding info"  "$info_sum"        "$out_info"
chk "Warning resolved"         "$warn_res_sum"    "$warn_res_body"
chk "Warning unresolved"       "$warn_unres_sum"  "$warn_unres_body"
chk "Blocking resolved"        "$block_res_sum"   "$block_res_body"
chk "Blocking unresolved"      "$block_unres_sum" "$block_unres_body"

if [ "$fail" -eq 0 ]; then echo "PASS"; exit 0; else echo "FAILED"; exit 1; fi
