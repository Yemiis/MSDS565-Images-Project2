"""Read local folder structure to resolve actual classes without inventing labels.

Run on the Windows computer: python scripts/inspect_dataset.py
This never moves/deletes images or assigns provenance. Output is saved externally.
"""
import json
import os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
config=json.loads((ROOT/'config/project.json').read_text(encoding='utf-8'))
raw_path=os.environ.get('P2_DATA_ROOT',config['data_root'])
if os.name!='nt' and len(raw_path)>1 and raw_path[1]==':':
    raise SystemExit('Run this on the Windows computer, or set P2_DATA_ROOT to an accessible data folder.')
data=Path(raw_path).expanduser()
if not data.is_dir():raise SystemExit(f'Dataset directory not found: {data}')
scan_root=data/'raw' if (data/'raw').is_dir() else data
suffixes={'.jpg','.jpeg','.png','.webp','.bmp','.tif','.tiff','.gif','.avif'}
folders=[]
for directory in sorted(scan_root.iterdir()):
    if not directory.is_dir() or directory.name in {'prepared','scrape_batches','.git','__pycache__'}:continue
    files=[path for path in directory.rglob('*') if path.is_file() and path.suffix.lower() in suffixes]
    if files:folders.append({'folder':directory.name,'image_file_count':len(files),
                             'note':'Unverified count; not a manual-cleaning or usable-image total.'})
output={'scan_root':str(scan_root),'candidate_class_folders':folders,
        'source_manifest_exists':(data/'P2_source_manifest.csv').exists(),
        'top_level_image_count':sum(path.is_file() and path.suffix.lower() in suffixes for path in scan_root.iterdir())}
path=data/'P2_dataset_inventory.json'
path.write_text(json.dumps(output,indent=2),encoding='utf-8')
print(json.dumps(output,indent=2));print('Saved inventory:',path)
print('Confirm real labels/queries in config/project.json. Counts alone do not certify class quality.')
