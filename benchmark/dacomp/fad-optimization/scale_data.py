"""Whole-row synthetic scaling with deterministic lineage; no FAD input."""
import argparse
import hashlib
import json
import random
import sqlite3
import time
from pathlib import Path


def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--rows',type=int,default=1000000);p.add_argument('--seed',type=int,default=20260910)
    args=p.parse_args();out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():raise FileExistsError(out)
    start=time.perf_counter();source_hash=sha(args.source)
    src=sqlite3.connect(Path(args.source).resolve().as_uri()+'?mode=ro',uri=True)
    schema=src.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='sheet1'").fetchone()[0]
    columns=[r[1] for r in src.execute('PRAGMA table_info(sheet1)')]
    data=src.execute('SELECT * FROM sheet1 ORDER BY rowid').fetchall()
    id_col=columns.index('Waybill Number');original_ids={r[id_col] for r in data}
    full,extra=divmod(args.rows,len(data))
    remainder=sorted(random.Random(args.seed).sample(range(len(data)),extra))
    db=sqlite3.connect(out);db.execute(schema)
    sql='INSERT INTO sheet1 VALUES('+','.join('?' for _ in columns)+')'
    generated=0
    # Cycle 0 retains original identifiers, including existing duplicate IDs.
    for cycle in range(full+bool(extra)):
        indices=range(len(data)) if cycle<full else remainder
        batch=[]
        for index in indices:
            row=list(data[index])
            if cycle:
                row[id_col]=f'SYN{cycle:04d}-{index+1:05d}'
                if row[id_col] in original_ids:raise ValueError('synthetic ID collision')
            batch.append(row);generated+=1
            if len(batch)==5000:db.executemany(sql,batch);batch=[]
        if batch:db.executemany(sql,batch)
    db.commit()
    # Read back every row, compare every business field and exact source lineage.
    checked=0
    for output_index,row in enumerate(db.execute('SELECT * FROM sheet1 ORDER BY rowid')):
        cycle,index=divmod(output_index,len(data))
        if cycle==full:index=remainder[index]
        original=data[index]
        assert all(a==b for j,(a,b) in enumerate(zip(row,original)) if j!=id_col)
        expected_id=original[id_col] if cycle==0 else f'SYN{cycle:04d}-{index+1:05d}'
        assert row[id_col]==expected_id
        checked+=1
    assert checked==args.rows==generated
    def profile(c):
        return {'rows':c.execute('SELECT COUNT(*) FROM sheet1').fetchone()[0],
                'distinct_waybills':c.execute('SELECT COUNT(DISTINCT "Waybill Number") FROM sheet1').fetchone()[0],
                'south_china_rows':c.execute("SELECT COUNT(*) FROM sheet1 WHERE Destination LIKE 'South China%'").fetchone()[0],
                'date_range':c.execute('SELECT MIN(Date),MAX(Date) FROM sheet1').fetchone(),
                'products':c.execute('SELECT COUNT(DISTINCT "Consigned Product") FROM sheet1').fetchone()[0],
                'destinations':c.execute('SELECT COUNT(DISTINCT Destination) FROM sheet1').fetchone()[0]}
    before,after=profile(src),profile(db)
    assert after['distinct_waybills']==args.rows-(len(data)-len(original_ids))
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert not db.execute("SELECT name FROM sqlite_master WHERE type='index'").fetchall()
    db.close();src.close();assert sha(args.source)==source_hash
    manifest={'mode':'whole-row replication plus seeded sampling without replacement',
              'source':str(Path(args.source).resolve()),'source_sha256':source_hash,
              'output':str(out.resolve()),'output_sha256':sha(out),'output_bytes':out.stat().st_size,
              'seed':args.seed,'full_copies':full,'remainder_rows':extra,
              'remainder_source_row_ordinals_1_based':[i+1 for i in remainder],
              'identifier_rule':'cycle 0 unchanged; later cycles SYN{cycle:04d}-{source_ordinal:05d}',
              'original_duplicate_waybills_preserved':len(data)-len(original_ids),
              'business_fields_verified_rows':checked,'source_profile':before,'output_profile':after,
              'schema_preserved':True,'base_indexes':0,'integrity_check':'ok',
              'generation_and_validation_seconds':time.perf_counter()-start}
    out.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if not k.startswith('remainder_source')},indent=2),flush=True)

if __name__=='__main__':main()
