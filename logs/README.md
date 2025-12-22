# Logs

Runtime logs and execution history.

## Files

- `run.log` - Main execution log (auto-rotates at 100MB)

## Viewing Logs

Via REPL:
```
/log    # Show recent log entries
```

Or directly:
```bash
tail -f logs/run.log
```
