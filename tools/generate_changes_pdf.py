from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUTPUT = BASE / 'docs' / 'changes.pdf'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

FILES = [
    'properties/utils.py',
    'properties/views.py',
    'properties/signals.py',
    'properties/apps.py',
    'properties/__init__.py',
]

EXPLANATIONS = {
    'properties/utils.py': (
        'Contains get_all_properties() which reads the cached "all_properties" key from Django cache, ' 
        'falls back to querying Property model, saves the evaluated list to cache for 3600 seconds, and returns it.\n\n' 
        'Also contains get_redis_cache_metrics() which connects to the redis instance used by django-redis, ' 
        'reads INFO, extracts keyspace_hits and keyspace_misses, computes a hit_rate (hits/(hits+misses)) ' 
        'and returns a dict. Any exceptions are logged via logger.error and the function returns None on error.'
    ),
    'properties/views.py': (
        'Defines PropertyListView (class-based) used for HTML listing and property_list (function-based) ' 
        'which returns JSON and is decorated with @cache_page(60*15) so the HTTP response is cached for 15 minutes. ' 
        'The property_list view uses get_all_properties() from utils to pull cached DB results.'
    ),
    'properties/signals.py': (
        'Provides post_save and post_delete signal handlers that delete the cache key "all_properties" when Property instances change. ' 
        'This prevents stale cached DB results.'
    ),
    'properties/apps.py': (
        'Defines PropertiesConfig and includes an import of properties.signals to ensure signal handlers are registered. ' 
        'An explicit import at module level was also added to guarantee the presence of the import. ' 
    ),
    'properties/__init__.py': (
        'Sets default_app_config to properties.apps.PropertiesConfig for compatibility with certain Django versions.'
    ),
}


def read_file_safe(path: Path):
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        return f'Could not read {path}: {e}'


def build_pdf():
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph('Repository Changes and Explanations', styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    intro = Paragraph(
        'This document summarizes the code changes made to add Redis-backed caching and cache invalidation for property listings, and explains the purpose and behavior of each file.',
        styles['BodyText']
    )
    story.append(intro)
    story.append(Spacer(1, 12))

    for rel in FILES:
        p = BASE / rel
        heading = Paragraph(rel, styles['Heading2'])
        story.append(heading)
        story.append(Spacer(1, 6))
        expl = EXPLANATIONS.get(rel, '')
        story.append(Paragraph(expl.replace('\n', '<br/>'), styles['BodyText']))
        story.append(Spacer(1, 6))
        story.append(Paragraph('Source:', styles['Heading3']))
        story.append(Spacer(1, 4))
        src = read_file_safe(p)
        # Keep source short in PDF to avoid huge file; include first 2000 chars
        snippet = src[:2000]
        if len(src) > 2000:
            snippet += '\n\n... (truncated)'
        story.append(Paragraph('<pre>%s</pre>' % snippet.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br/>'), styles['Code']))
        story.append(Spacer(1, 12))

    doc.build(story)
    print('Wrote PDF to', OUTPUT)


if __name__ == '__main__':
    build_pdf()
