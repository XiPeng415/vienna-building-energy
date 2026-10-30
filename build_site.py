from pathlib import Path
import hashlib,json,zipfile,stat
root=Path(__file__).resolve().parent
meta=json.loads((root/'site-manifest.json').read_text())
archive=root/'site.zip'
whole=hashlib.sha256()
with archive.open('wb') as target:
 for part in meta['parts']:
  data=(root/part['file']).read_bytes()
  assert len(data)==part['bytes'] and hashlib.sha256(data).hexdigest()==part['sha256'],part['file']
  target.write(data);whole.update(data)
assert whole.hexdigest()==meta['archive_sha256']
dest=root/'_site';dest.mkdir(exist_ok=True)
with zipfile.ZipFile(archive) as z:
 assert sum(i.file_size for i in z.infolist())==meta['site_bytes']<1_000_000_000
 for i in z.infolist():
  out=(dest/i.filename).resolve()
  assert out.is_relative_to(dest.resolve()) and not stat.S_ISLNK(i.external_attr>>16)
 z.extractall(dest)
for entry in meta['files']:
 p=dest/entry['path']
 assert p.stat().st_size==entry['bytes']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],entry['path']
assert (dest/'index.html').is_file()
print('Verified',meta['site_files'],'static files;',meta['site_bytes'],'bytes')

# Presentation-only update after verifying the immutable building-data snapshot.
# Remove the About navigation, modal markup, content and event handlers.
index=dest/'index.html'
html=index.read_text(encoding='utf-8')
about_link='            <a href="#" id="about-link">About</a>\n'
assert html.count(about_link)==1, 'Expected one About navigation link'
html=html.replace(about_link,'')
modal_start=html.index('        <div id="overlay" class="overlay"></div>')
modal_end=html.index('    <!-- BEGIN VIENNA STARTUP SCREEN -->',modal_start)
assert 'id="popup"' in html[modal_start:modal_end]
html=html[:modal_start]+html[modal_end:]

bundle=dest/'file-view/main.js'
script=bundle.read_text(encoding='utf-8')
about_start=script.index('var ege=`')
about_end=script.index('var tP1=[];',about_start)
removed=script[about_start:about_end]
assert 'About the Buildings.city Platform' in removed
assert 'document.getElementById("about-link")' in removed
script=script[:about_start]+script[about_end:]
assert 'about-link' not in script and 'About the Buildings.city Platform' not in script
bundle.write_text(script,encoding='utf-8',newline='\n')

# Refresh the bundle URL so returning visitors load the revised interface.
previous='./file-view/main.js?v=936cb37d5a4a'
assert html.count(previous)==1
html=html.replace(previous,'./file-view/main.js?v='+hashlib.sha256(script.encode('utf-8')).hexdigest()[:12])
assert 'about-link' not in html and 'id="popup"' not in html
index.write_text(html,encoding='utf-8',newline='\n')
print('Removed Vienna About navigation and modal; building data unchanged')
