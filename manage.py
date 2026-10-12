"""Command-line utilities.

    python manage.py init-db            create tables (idempotent)
    python manage.py load-sample        create tables and load the synthetic sample semesters
    python manage.py write-sample-csv   regenerate dataset/sample/* CSV files and templates
    python manage.py experiments        run the multi-seed comparison and save results
    python manage.py hash-password      print a password hash for AETHERIS_ADMIN_PASSWORD_HASH
"""
from __future__ import annotations

import argparse
import sys

import config
from src.database import init_db, session_scope
from src.logging_setup import setup_logging


def cmd_init_db(_args) -> None:
    init_db()
    print(f"Database ready: {config.DATABASE_URL}")


def cmd_load_sample(_args) -> None:
    from src.sample_loader import load_all_samples

    init_db()
    with session_scope() as s:
        ids = load_all_samples(s)
    print(f"Sample semesters available (ids): {ids}")


def cmd_write_sample_csv(_args) -> None:
    from src.import_service import template_frame
    from src.sample_data import SPRING_SPEC, SampleSpec, write_sample_csvs
    from src.validation import IMPORT_ORDER

    for folder, spec in (("fall_2026", SampleSpec()), ("spring_2027", SPRING_SPEC)):
        paths = write_sample_csvs(config.SAMPLE_DIR / folder, spec)
        print(f"wrote {len(paths)} files to {config.SAMPLE_DIR / folder}")
    config.TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    for entity in IMPORT_ORDER:
        template_frame(entity).to_csv(config.TEMPLATE_DIR / f"{entity}_template.csv", index=False)
    print(f"wrote templates to {config.TEMPLATE_DIR}")


def cmd_experiments(args) -> None:
    from scripts.run_experiments import main as run

    run(seeds=args.seeds, iterations=args.iterations, particles=args.particles, save=not args.no_save)


def cmd_hash_password(args) -> None:
    """Print a PBKDF2 hash for AETHERIS_ADMIN_PASSWORD_HASH (the password itself is never stored)."""
    import getpass

    from src.auth import hash_password

    password = args.password or getpass.getpass("New admin password: ")
    if not password:
        raise SystemExit("empty password")
    print(hash_password(password))


def main(argv=None) -> int:
    setup_logging()
    parser = argparse.ArgumentParser(description=config.APP_NAME)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init-db").set_defaults(func=cmd_init_db)
    sub.add_parser("load-sample").set_defaults(func=cmd_load_sample)
    sub.add_parser("write-sample-csv").set_defaults(func=cmd_write_sample_csv)
    hp = sub.add_parser("hash-password", help="hash a new admin password for AETHERIS_ADMIN_PASSWORD_HASH")
    hp.add_argument("--password", help="password (omit to be prompted without echo)")
    hp.set_defaults(func=cmd_hash_password)
    exp = sub.add_parser("experiments")
    exp.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    exp.add_argument("--iterations", type=int, default=200)
    exp.add_argument("--particles", type=int, default=30)
    exp.add_argument("--no-save", action="store_true", help="do not store runs in the database")
    exp.set_defaults(func=cmd_experiments)
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
