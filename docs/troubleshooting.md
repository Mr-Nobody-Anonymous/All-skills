# Troubleshooting Guide

Common issues, diagnostics, and recovery steps.

---

## 1. Diagnostics & Doctor

Run the comprehensive platform diagnostic:

```bash
.\allskills.bat doctor
```

This verifies:
- Python environment and required modules.
- Active agent harnesses and symlinks (`.agents/skills/`, `.claude/`, `.cursor/`, etc.).
- Schema validity of all `SKILL.md` documents.
- Runtime manifest and lockfiles.

---

## 2. Intent Overlaps & Conflicts

If two skills trigger on the same voice utterance:
1. Inspect the conflict resolver log in `data/logs/skill_logs/`.
2. Check priority tiers in [`config/priority_config.yml`](file:///config/priority_config.yml). Higher priority tiers take precedence over lower tiers.
3. User pinning: You can pin a preferred skill for a domain by updating `intent_router.py` user preferences.

---

## 3. Circular Dependencies & Import Errors

Run the circular dependency detector:

```bash
python -c "from scratch_priority_import.circular_dependency_detector import CircularDependencyDetector; print('Clean!')"
```

If an error occurs, inspect the dependency graph in `scratch_priority_import/dependency_graph.py`.

---

## 4. Audio Input / Output Issues

- **Microphone not detected**: Verify your default audio recording device in your OS settings.
- **Vosk / Whisper STT failure**: Ensure model files exist under `data/models/stt_models/` or configure an API fallback in `config/api_keys.yml`.
- **TTS playback silent**: Check volume via Tier 0 volume skill or test via `python plugins/tts/plugin-tts-piper/piper_tts.py --test`.

---

## 5. Disk Space Warnings

If disk space drops below safety thresholds:
- The clone utility (`scripts/clone_all_repos.py`) will automatically halt with `[ERROR] Insufficient disk space`.
- Clean up unused cache in `data/databases/osm_catalog_cache.json` or scratch artifacts in `scratch/`.
