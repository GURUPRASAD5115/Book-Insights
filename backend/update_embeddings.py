import os
import django

# -----------------------------
# SETUP DJANGO
# -----------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from books.models import BookChunk
from rag.embeddings import EmbeddingManager

print("🚀 Starting embedding update...")

manager = EmbeddingManager()

updated = 0
skipped = 0

# -----------------------------
# UPDATE ALL CHUNKS
# -----------------------------
for chunk in BookChunk.objects.all():

    try:
        if not chunk.text:
            skipped += 1
            continue

        embedding = manager.embed_text(chunk.text)

        # 🔥 NEVER allow None
        if not embedding:
            print(f"⚠️ Skipping chunk {chunk.id} (empty embedding)")
            skipped += 1
            continue

        chunk.embedding = embedding
        chunk.save()

        updated += 1

        print(f"✅ Updated chunk {chunk.id}")

    except Exception as e:
        print(f"❌ Error in chunk {chunk.id}: {e}")
        skipped += 1


# -----------------------------
# FINAL OUTPUT
# -----------------------------
print("\n🎯 DONE")
print(f"✅ Updated: {updated}")
print(f"⚠️ Skipped: {skipped}")