---
title: Penyakit_Padi_Id
source: Penyakit_Padi_ID.pdf
category: penyakit
total_pages: 78
section: Penyakit
page: 45
crop: padi
---

Output: Image binary,
1:
2:
Dapatkan setiap nilai piksel pada image asal
berdasarkan nilai merah, hijau dan biru.
Hitung nilai matrik kejadian histogram dua dimensi
untuk setiap piksel warna pada image yang
berukuran , dengan ialah nilai maksimum
grey scale.
3: Hitung nilai local entropi berdasarkan matrik
kejadian dua dimensi tersebut. Jika dipilih sebagai
nilai ambang, maka bagi matrik kepada empat bagian
(Kuadran A, B, C dan D).
Hitung nilai local entropi pada kuadran A dan C.
Nilai ambang akan memaksimumkan jumlah entropi
untuk setiap kuadran yang mewakili objek dan
latarbelakang yang dipilih.
Misal adalah satu matrik, maka normal -kan
supaya jumlah nilai bagi setiap kuadran adalah 1.
Tentukan objek yang cerah adalah elemen dalam
kuadran C dibagi dengan dan elemen dalam
kuadran A dibagi oleh .
Dengan
∑ ∑
∑ ∑
Maka, nilai entropi ( ) dan ( ) untuk objek
dan background-nya ialah