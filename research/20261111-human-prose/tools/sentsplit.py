# /// script
# requires-python = ">=3.10"
# dependencies = ["sudachipy>=0.6.8", "sudachidict-core>=20240409"]
# ///
"""One body sentence per paragraph, as flow.py reads them."""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import flow, koyobun
for f in sys.argv[3:]:
    text, err = koyobun.read_source_file(Path(f))
    sents = flow.read_sentences(text)
    Path(sys.argv[2], Path(f).name).write_text("\n\n".join(s["text"].strip() for s in sents) + "\n", encoding="utf-8")
