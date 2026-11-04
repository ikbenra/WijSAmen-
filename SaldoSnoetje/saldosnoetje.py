#!/usr/bin/env python3
import json, re, subprocess, time
from decimal import Decimal
from pathlib import Path
root=Path.home()/'.saldosnoetje'
root.mkdir(exist_ok=True)
state=root/'state.json'
pattern=re.compile(r'(?i)\b(?:beschikbaar\s+saldo|huidig\s+saldo|rekening\s*saldo|saldo)\b\s*(?:[:=]|is)?\s*(?:€\s*)?(-?\d{1,3}(?:\.\d{3})*,\d{2}|-?\d+,\d{2})')
def run(*args):
    try: return subprocess.run(args,capture_output=True,text=True,timeout=6)
    except (OSError,subprocess.TimeoutExpired): return None
def main():
    old=None
    if state.exists():
        try: old=Decimal(json.loads(state.read_text())['last'])
        except (ValueError,KeyError,OSError): pass
    last_clip=None
    print('SaldoSnoetje: kopieer een saldo; Ctrl+C stopt.')
    while True:
        result=run('termux-clipboard-get')
        if result and result.returncode==0 and result.stdout!=last_clip:
            last_clip=result.stdout
            match=pattern.search(last_clip)
            if match:
                current=Decimal(match.group(1).replace('.','').replace(',','.'))
                if old is None: print('Eerste saldo herkend.')
                elif current!=old:
                    kind='happy' if current>old else 'sad'
                    sound=root/(kind+'.mp3')
                    if sound.exists(): run('termux-media-player','play',str(sound))
                    else: run('termux-vibrate','-d','180' if kind=='happy' else '400')
                    print('Saldo gestegen.' if kind=='happy' else 'Saldo gedaald.')
                old=current
                state.write_text(json.dumps({'last':str(current)}))
        time.sleep(3)
try: main()
except KeyboardInterrupt: print('Gestopt.')
