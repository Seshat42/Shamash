# Summary
- Added PyInstaller spec files for the client and server that bundle the configuration directory for reproducible builds.
- Expanded the CI workflow to a Linux, macOS, and Windows matrix and introduced a tag-triggered release pipeline that tests, packages, and uploads platform archives.
- Documented the release workflow in the READMEs and promoted the accumulated changes into the 0.2.0 changelog entry.

# Testing
- `pyinstaller packaging/pyinstaller/shamash_client.spec --noconfirm --distpath /tmp/pyi-dist --workpath /tmp/pyi-build`
- `pyinstaller packaging/pyinstaller/shamash_server.spec --noconfirm --distpath /tmp/pyi-dist --workpath /tmp/pyi-build`
- `pytest`
