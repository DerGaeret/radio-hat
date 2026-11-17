#!/usr/bin/python3
# DRC mit neu gefuellten Flaechen auf einer Kopie. Aufruf: python3 drc.py Platine.kicad_pcb Arbeitsordner refill
import sys, shutil, os, re, collections, pcbnew
src, work, refill = sys.argv[1], sys.argv[2], sys.argv[3]=='refill'
os.makedirs(work, exist_ok=True)
for ext in ('.kicad_pcb','.kicad_pro','.kicad_dru'):
    if os.path.exists(src.replace('.kicad_pcb',ext)): shutil.copy(src.replace('.kicad_pcb',ext), work)
path=os.path.join(work, os.path.basename(src)); b=pcbnew.LoadBoard(path)
if refill:
    f=pcbnew.ZONE_FILLER(b); f.Fill(b.Zones()); pcbnew.SaveBoard(path, b)
    for z in b.Zones(): print('zone', z.GetZoneName(), 'filled area mm2 %.0f' % (z.GetFilledArea()/1e12) if hasattr(z,'GetFilledArea') else '')
rep=path+'.drc.txt'; pcbnew.WriteDRCReport(b, rep, pcbnew.EDA_UNITS_MILLIMETRES, True)
t=open(rep).read()
print(re.findall(r'\*\* Found.*', t))
print(collections.Counter(re.findall(r'^\[(\w+)\]', t, re.M)).most_common())
