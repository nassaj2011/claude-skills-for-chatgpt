# Disposable synthetic recovery drill

The unit tests **create their own one-file fake backup**, compute a hash manifest, restore into a new isolated directory and verify content. They also demonstrate corruption detection, missing files and fail-closed no-overwrite. All temporary records are fictional and the only cleanup is inside self-created disposable test fixtures.

Run: python -m unittest discover -s examples/restore-drill -p "test_*.py" -v

The tool does not restore a real database, verify logical consistency, replay a WAL or measure production RPO/RTO. Production backup files and existing folders are never touched in this test. For an actual restore drill obtain specific authorization, independent destination, service keys and owners.
