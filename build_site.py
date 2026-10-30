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
