"""Read-only source checks; --submission adds explicit course-completion gates."""
import argparse, ast, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--submission',action='store_true');args=parser.parse_args()
errors=[]
notebooks=sorted((ROOT/'notebooks').glob('*.ipynb'))
expected=['P2_Images-1_Scrape_Project2.ipynb','P2_Images-2_Preprocessing_Project2.ipynb','P2_Images-3_TransferLearning_Project2.ipynb','P2_Images-4_xAI_Project2.ipynb']
if [p.name for p in notebooks]!=expected:errors.append('Expected exactly four canonical Project2 notebooks.')
for path in ROOT.rglob('*'):
 if not path.is_file() or any(x in path.parts for x in ['.git','__pycache__','.pytest_cache']):continue
 if path.suffix.lower() in {'.jpg','.jpeg','.png','.gif','.webp','.bmp','.svg','.npy','.npz','.zip','.pyc'}:errors.append(f'Forbidden dataset/cache file: {path.relative_to(ROOT)}')
 if path.stat().st_size>=100_000_000:errors.append(f'File exceeds GitHub limit: {path.name}')
 if path.suffix=='.py':
  try:ast.parse(path.read_text(encoding='utf-8'))
  except SyntaxError as e:errors.append(f'{path.name}: {e}')
for path in notebooks:
 n=json.loads(path.read_text(encoding='utf-8'))
 for i,c in enumerate(n['cells']):
  if c['cell_type']!='code':continue
  if ''.join(c['source']).strip():
   try:ast.parse(''.join(c['source']))
   except SyntaxError as e:errors.append(f'{path.name} cell {i}: {e}')
  if any(o.get('output_type')=='error' for o in c.get('outputs',[])):errors.append(f'{path.name}: saved error output')
  if args.submission and c.get('execution_count') is None:errors.append(f'{path.name}: unexecuted cell {i}')
provenance=json.loads((ROOT/'docs/provided_helper_hashes.json').read_text())
for rel,expected_hash in provenance.items():
 if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=expected_hash:errors.append(f'Instructor helper changed: {rel}')
import sys
sys.path.insert(0,str(ROOT/'app'))
try:
 from deployment_utils import load_contract
 load_contract(ROOT/'models')
except Exception as e:errors.append(f'Deployment artifacts: {e}')
if args.submission:
 if 'RECONSTRUCTED SETUP' in (ROOT/'environment.yml').read_text():errors.append('Export environment.yml from the actual notebook conda environment.')
 for rel in ['models/P2_N4_visual_interpretations.csv','models/P2_N4_deployment_judgment.json','docs/LIVE_DEMO_COMPLETED.md']:
  if not (ROOT/rel).exists():errors.append(f'Pending completion artifact: {rel}')
 if 'TEMPLATE ONLY' in (ROOT/'docs/MEETING_MINUTES.md').read_text():errors.append('Complete actual meeting minutes.')
if errors:
 print('\n'.join('FAIL: '+e for e in errors));raise SystemExit(1)
print('PASS: canonical files, source syntax, saved notebook errors, image/array boundaries, instructor helpers, model hashes, preprocessing and class mapping.')
if not args.submission:print('Course-completion checks are separate: run with --submission.')
