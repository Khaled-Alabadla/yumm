"""Ensure compiled gettext catalogs exist before Django serves requests."""

from __future__ import annotations

from pathlib import Path


def ensure_compiled_translations() -> None:
    """Compile django.po → django.mo when the binary is missing or outdated."""
    try:
        import polib
    except ImportError:
        return

    base = Path(__file__).resolve().parent.parent
    build_script = base / "locale" / "build_ar_translations.py"

    for po_path in base.glob("locale/*/LC_MESSAGES/django.po"):
        mo_path = po_path.with_suffix(".mo")
        rebuild_from_script = (
            build_script.exists()
            and (
                not mo_path.exists()
                or build_script.stat().st_mtime > mo_path.stat().st_mtime
            )
        )
        if rebuild_from_script:
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                "yumm_build_ar_translations", build_script
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.build_po()
            continue

        if not po_path.exists():
            continue
        if mo_path.exists() and mo_path.stat().st_mtime >= po_path.stat().st_mtime:
            continue
        po = polib.pofile(str(po_path))
        po.save_as_mofile(str(mo_path))
