# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pdfplumber

path = r"C:\Users\claud\Downloads\Esercizi simplesso_221220_181341.pdf"
with pdfplumber.open(path) as pdf:
    print(f"Totale pagine: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            print(f"\n{'='*60}")
            print(f"PAGINA {i+1}")
            print('='*60)
            print(text)
