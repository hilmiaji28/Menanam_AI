---
title: Penyakit_Padi_Id
source: Penyakit_Padi_ID.pdf
category: penyakit
total_pages: 78
section: Penyakit
page: 63
crop: padi
---

dan tirus, maka bentuk yang paling jelas dan paling
banyak akan dipilih . Alur prosesnya dapat dijelaskan pada
flowchart gambar 4.7 . Sedangkan a lgoritma untuk proses
analisa tekstur bentuk ditunjukkan pada Algoritma 4.1.
IId jb = OvalBBOOval >0
BBObujur ³ BBObulat
Ç
BBObujur ³ BBOtirus
Apakah jenis bulat, tirus,
bujur atau bintik
jb = BUJUR Aapakah jenis bulat, tirus
atau bintik
BBObulat ³ BBOtirus
jb = BULAT
jb = TIRUS
BBObujur = 0 Ç
BBObulat = 0 Ç
BBOtirus = 0
jb = BINTIK
Ya
Tidak
Ya Tidak
Ya
Tidak
Tidak
Ya
IIIa
IIIa
BBOoval=jumlah objek oval
BBObujur=Jmlah objek bujur
BBObulat=Jumlah objek bulat
BBOtirus=Jumlah objek tirus
BBObintik=Jumlah objek bintik
jb = Jenis Bentuk
Apakah jenis tirus atau
bintik
Gambar 4.7 Flowchart penentuan jenis bentuk kerusakan
Algoritma 4.1 Algoritma analisa tekstur bentuk
Input: citra binary,
Output: Jenis bentuk kerusakan dari daun padi