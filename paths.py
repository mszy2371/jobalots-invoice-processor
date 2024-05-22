import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MANIFEST_URL_BASE = "https://static.bodysocks.net/joblots/manifests/"
LOGS_DIR = os.path.join(BASE_DIR, "app", "logs")
EMPTY_MANIFEST = os.path.join(BASE_DIR, "app", "utils", "empty_manifest.csv")
MISSING_MANIFESTS_DIR = os.path.join(BASE_DIR, "app", "logs", "missing_manifests")