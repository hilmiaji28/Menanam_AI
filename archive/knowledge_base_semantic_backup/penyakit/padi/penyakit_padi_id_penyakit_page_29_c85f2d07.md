---
title: Penyakit_Padi_Id
source: Penyakit_Padi_ID.pdf
category: penyakit
total_pages: 78
section: Penyakit
page: 29
crop: padi
---

( ) ( ) ( )
(2.1)
dengan adalah per bedaan tingkat kecerahan antara dua
warna, dan adalah perbe daan kromatik antara dua
warna.
Algoritma 2.1 Algoritma model warna CIE L*a*b*
Input: Ruang warna RGB ( )
Output: Ruang warna CIE L*a*b*
1: Ubah nilai RGB ( ) ke dalam model warna
CIE XYZ (Persamaan 2.2).
[
] [
] [
] (2.2)
2: Ubah nilai XYZ ke dalam model warna CIE L*a*b*,
dengan mencari nilai L*, a* dan b* (Persamaan 2.3a dan
2.3b).
 Nilai L* (luminance) diperoleh dari Persamaan
2.3a:
{
(
)
(
)
(2.3a)
 Koordinat chroma a* dan b* diperoleh dari
Persamaan 2.3b:
[ (
) (
)]
[ (
) (
)]
dengan
(
) √