# ChronoPath AI

Location-aware historical storytelling MVP migrated from the n8n prototype shape
to a Python multi-agent architecture.

## Run Demo

```bash
python main.py --user 1 --lat 18.5196 --lng 73.8553
```

Expected output includes:

```json
{
  "place": "Shaniwar Wada",
  "context": "Peshwa Era",
  "story": "..."
}
```

## MVP Scope

- Mock location, profile, journey, history, and network tools
- Supervisor-driven end-to-end flow
- JSON responses
- Simple in-memory journey write
- No vector DB, auth, Cloud Run, media generation, or real evaluation
