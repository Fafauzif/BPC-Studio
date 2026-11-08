# Start BPC Studio

Give an AI agent file access to this repository and say:

> Read AGENTS.md and skills/build-bpc-proposals/SKILL.md. Use BPC Studio for my task below. Read my latest guidebook, rubric and supplied current files. Preserve accepted decisions. Default proposal text to Indonesian unless I choose another language. Develop a compelling operating business and keep its economics reconstructable. Produce only the requested scope and continue through the necessary review and repair.
>
> Task: …
> Materials: …
> Output: …

A complete proposal is the primary workflow. BMCs, decks, scripts and Q&A are supporting routes used when requested. No extra deck, questionnaire or validation dossier is compulsory.

For a local capability check and clean project:

```bash
python studio.py doctor
python studio.py new usaha-baru
python studio.py --help
```

Read [setup](docs/setup.md) for dependencies and [the runnable example](examples/ruang-rapi/README.md) for a complete demonstration. `doctor` inventories availability; actual compilation and rendering are separate checks.

To resume, provide the project's `project-record.json`, `HANDOFF.md`, latest accepted artifact and current request. The repository cannot remember unseen previous chats.
