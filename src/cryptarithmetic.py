#!/usr/bin/env python
# Cryptarithmetic

from sys import argv
from datetime import datetime,timedelta

if len(argv) != 2:
  print("Masukkan nama file input")
  exit(1)
f = open(argv[1]).read().split('\n\n')
f = list(map(lambda x: x.split('\n'), f))

probs = [{} for _ in range(len(f))]

# baca soal
for idxSoal in range(len(f)):
  probs[idxSoal] = { 'operands': [], 'letters': [], 'firstLetters': [], 'letterIndex': {}, 'tests': 0}
  for line in f[idxSoal]:
    if line[0] == '-': continue
    l = line.strip().rstrip('+')
    if len(l) > 0:
      probs[idxSoal]['firstLetters'] += l[0]
      for c in l:
        if c not in probs[idxSoal]['letters']:
          probs[idxSoal]['letterIndex'][c] = len(probs[idxSoal]['letters'])
          probs[idxSoal]['letters'] += c
      probs[idxSoal]['operands'].append(l)

# buat permutasi angkanya
def permute(l, firstLetters):
  if len(l) > 1:
    for perm in permute(l[1:], firstLetters):
      for i in range(10):
        if not (l[0] in firstLetters and i == 0):
          if i not in perm:
            yield([i] + perm)
  else:
    for i in range(10):
      if not (l[0] in firstLetters and i == 0):
        yield([i])

# mulai proses

success = False
totTime = timedelta(0)
for i in range(len(probs)):
  p = probs[i]
  tests = 0
  #print("Soal ke-", i+1, sep="")
  print("-"*8)
  start = datetime.now()

  # buat permutasi
  for perm in permute(p['letters'], p['firstLetters']):
    # substitusi huruf -> angka untuk "permutasi sekarang"
    subOp = [int(''.join(map(lambda x: str(perm[p['letterIndex'][x]]), str(op)))) for op in p['operands']]
    # jumlahkan semua operand
    guessSum = 0
    for op in subOp[:len(subOp)-1]: guessSum += op
    # sum ada di akhir list operand, cek sudah cocok belum
    success = guessSum == subOp[len(subOp)-1]
    p['tests'] += 1
    if success:
      p['sols'] = subOp
      break
  
  end = datetime.now()
  p['time'] = end - start
  totTime += p['time']

  longest = len(p['operands'][len(p['operands'])-1])
  if success:
    mid = ' '*3
    print("Solusi:")
    for i in range(len(p['operands'])-1):
      spc = ' '*(longest-len(p['operands'][i]))
      print(spc, p['operands'][i], mid, ' ', spc, p['sols'][i], sep="")
    print("-"*longest, '+', mid, '-'*longest, '+', sep="")
    print(p['operands'][len(p['operands'])-1], mid, ' ', p['sols'][len(p['operands'])-1], sep="")
  else:
    print("Tidak ada solusi")

  print("waktu eksekusi:", p['time'])
  print("jumlah total tes:", p['tests'])
  print("-"*8)

print("total waktu eksekusi: ", totTime)
