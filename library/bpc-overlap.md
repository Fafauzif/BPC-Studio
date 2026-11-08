# Hubungan isi terbatas antarcontoh BPC

Pemeriksaan ini mendokumentasikan overlap yang benar-benar terlihat pada BPC-37/BPC-49 (SnapStone) dan pengulangan venture BPC-28/BPC-58 (BeeGuard). Tujuannya mengelola pembelajaran korpus: materi berulang tidak dihitung sebagai validasi pasar, pengujian, atau hasil usaha yang independen. Temuan tidak menetapkan kepengarangan, urutan versi, izin penggunaan, niat, ataupun plagiarisme. Status pemenang tidak disimpulkan dari nama berkas.

## Identitas yang dibandingkan

| ID | Nama original | Halaman fisik | SHA-256 |
|---|---|---:|---|
| BPC-37 | Olivia IX 2024_BisnisPlan_SnapStone_Randi Saputra_Universitas Padjadjaran.pdf | 25 | `4542624b480a5309072f99837aaa2896cfb9eb80305ff411e8b07b1470cbd821` |
| BPC-49 | Proposal_Business_Plan_Pretty_Smart (2).pdf | 17 | `2114b7fe1c21a88f658a4b110c36a001688b2d767e4365971ca206d7bd1556ea` |
| BPC-28 | Emeraldo Ariesusandi_BEEGUARD_ INOVASI SISTEM SARANG MADU DIGITAL - Alexander Emeraldo.pdf | 20 | `d722a73ebb97d71f245ad4e69b9790a53b8a800008aafeb482e1809f05a49c69` |
| BPC-58 | Tim Yukaku_PROPOSAL BPC_BeeGuard_ Inovasi Sistem Sarang Lebah Digital - Alexander Emeraldo.pdf | 28 | `7f728810ee5348a47240bd9d1c3504f96565c9a50d08c53ea85071051769dd1e` |

Arsip asli masing-masing berada pada `library/originals/bpc/BPC-XX.pdf`. Seluruh lokator di laporan ini adalah halaman fisik PDF.

## Metode dan batas angka

Pembacaan penuh BPC-49/BPC-58 dilakukan melalui teks native/OCR dan visual; pembaca BPC-28/BPC-37 melakukan pembacaan penuh dalam tugas paralel. Untuk laporan ini, bagian pasangan yang cocok diperiksa langsung lagi: teks native pencocokan serta tabel/gambar BPC-37 halaman 9–10, 14–16, dan 20 dibandingkan dengan BPC-49 halaman 6–9 dan 14.

Ukuran berikut dihitung dari teks native PyMuPDF pada badan naskah: BPC-37 halaman 4–18 dengan BPC-49 halaman 3–12; BPC-28 halaman 3–19 dengan BPC-58 halaman 4–23. Cover, daftar isi, daftar pustaka, dan lampiran di luar rentang tersebut tidak masuk ukuran badan. Teks dinormalisasi Unicode NFKC, huruf kecil, lalu dipecah dengan pola Python `\w+`; tanda baca diabaikan, angka dan penomoran yang tertangkap tetap masuk. Dua ukuran digunakan:

1. Jumlah token dalam blok identik berurutan minimal 20 token dari `difflib.SequenceMatcher(autojunk=False)`. Blok algoritme tidak saling tumpang tindih, tetapi pilihan blok dipengaruhi urutan bagian.
2. Jumlah tipe 8-gram unik yang sama, dibagi jumlah tipe 8-gram unik pada masing-masing badan dokumen. Satu 8-gram adalah delapan token berturutan.

| Pasangan | Token badan A / B | Blok identik ≥20 token | Token di blok tersebut | Proporsi token A / B | Tipe 8-gram sama | Proporsi tipe 8-gram A / B |
|---|---:|---:|---:|---:|---:|---:|
| 37 / 49 | 2.799 / 2.258 | 15 | 932 | 33,3% / 41,3% | 1.165 | 45,4% / 55,9% |
| 28 / 58 | 2.490 / 4.739 | 18 | 1.213 | 48,7% / 25,6% | 1.214 | 48,9% / 25,7% |

Penyebut tipe 8-gram adalah 2.567/2.084 untuk 37/49 dan 2.483/4.730 untuk 28/58. Persentase ini adalah ukuran teks native dalam rentang terpilih, **bukan persentase keseluruhan dokumen, skor plagiarisme, atau ukuran asal-usul**. Teks raster, isi tabel gambar, dan teks yang hanya tersedia melalui OCR tidak masuk hitungan ini. Mengubah ekstraktor, pemenggalan kata, atau batas badan dapat mengubah angka. Karena itu pemeriksaan visual dan penilaian konteks tetap diperlukan.

## SnapStone: BPC-37 dan BPC-49

BPC-49 memakai nama berkas Pretty+Smart dan cover tim sekolah; badan tetap menyebut SnapStone. Kesamaan dapat dilokasikan pada isi yang lebih spesifik daripada topik “daur ulang plastik”.

| Isi yang diperiksa | BPC-37 | BPC-49 | Temuan terbatas |
|---|---:|---:|---|
| Latar belakang industri semen dan alternatif paving | 5 | 4 | Blok native identik 175 token; dimulai “Salah satu alternatif daur ulang limbah anorganik plastik…” dan berlanjut pada emisi semen serta manfaat bahan. |
| Pengenalan venture dan angka sampah | 4 | 3 | Blok 60 token, termasuk angka 23.733.245,04 “juta ton” dan 18,7%; satuan yang meragukan ikut berulang. |
| Urutan produksi | 8 | 10 | Blok 88 token: pengumpulan/pembersihan, pencacahan, pencucian, pengeringan, pelelehan, pencetakan, pendinginan. |
| Penyerapan air | 9 | 6 | Tabel visual memiliki empat komposisi dan 12 angka sama: 0,48/0,88/1,12/1,22; 0,44/0,68/0,91/1,30; 0,31/0,63/1,01/1,18. |
| Kuat tekan | 10 | 7 | Tabel visual sama: normal 8,3 MPa; campuran 3,7/4,3/4,8/4,6 MPa. |
| Flywheel dan target Jawa Barat/Jabodetabek | 14–15 | 8 | Gambar flywheel yang sama terlihat; uraian strategi pada 49 diringkas dan diatur ulang. |
| Model dan sumber pendapatan | 16 | 9 | Isi B2B/B2C dan beberapa sumber pendapatan sejalan; gambar berbeda: BMC rinci pada 37, diagram pelanggan/kontraktor pada 49. |
| Dokumentasi | 20 dan 9 | 14 | Tiga foto pada 37 halaman 20 serta foto perendaman halaman 9 muncul bersama pada 49 halaman 14. |

BPC-37 halaman 20 menampilkan keterangan “Sumber: (Hijjah 2022)” di bawah tiga foto. Pada BPC-49 halaman 14, empat foto tersebut terlihat tanpa keterangan sumber yang sama pada halaman itu. Ini temuan tampilan/attribution yang dapat diperiksa, bukan penetapan siapa yang mengambil foto atau bagaimana hak penggunaannya.

Bagian keuangan tidak identik. BPC-37 halaman 16–17 memuat proyeksi pendapatan Rp1.111.205.125, IRR 111,84%, NPV Rp475.048.584, ROI 127,35%; BPC-49 halaman 11 menyebut Rp1.041.205.125, 106,63%, sekitar Rp433.610.444, dan 115,85%. Tabel payback 37 halaman 17 menampilkan 1,57 tahun, sedangkan 49 halaman 12 menampilkan 1,67 tahun. Perubahan angka tidak membuktikan dasar bisnis baru; asumsi tiap model tetap harus diperiksa.

Implikasi craft-nya jelas. Kedua tabel kuat tekan justru menunjukkan pembanding normal lebih kuat daripada semua campuran; klaim bahwa produk lebih kuat dari paving semen tidak didukung tabel itu. Materi yang sama dapat membawa kelemahan argumen yang sama. Gunakan tabel untuk memutuskan spesifikasi dan batas penggunaan, pertahankan asal bukti, dan periksa ulang setiap perubahan angka, lokasi, jadwal, maupun janji hasil. Dua dokumen ini tidak menambah jumlah pengujian independen hanya karena cover dan panjangnya berbeda.

## BeeGuard: BPC-28 dan BPC-58

Kedua naskah mengusulkan sarang lebah digital BeeGuard dengan sensor, aplikasi, dan layanan terkait. BPC-58 menambah ruang untuk ringkasan, penjelasan, visual, dan lampiran; pertambahan halaman tidak dengan sendirinya berarti bukti lapangan baru.

| Isi yang diperiksa melalui teks aktual | BPC-28 | BPC-58 | Temuan terbatas |
|---|---:|---:|---|
| Latar belakang lebah, penyerbukan, dan masalah peternak | 3 | 5 | Blok identik 192 token, termasuk rujukan dan angka masalah. |
| SWOT | 5 | 9 | Blok identik 81 token tentang kekuatan IoT, keterbatasan tim/dana, peluang, dan ancaman. |
| Positioning | 11 | 14 | Blok identik 64 token tentang pemantauan koloni, stres/swarming, dan keberlanjutan. |
| Biaya variabel dan produksi bulanan | 14 | 16 | Blok 48 token mengulang Rp1.701.625/unit, 330 unit/bulan, dan Rp561.536.250. |
| Harga dan proyeksi volume | 15 | 17 | Blok 58 token mengulang Rp2,2 juta, 3.960/5.280/6.600 unit, serta Rp8,712/Rp11,616/Rp14,52 miliar. |
| BEP | 17 | 18 | Blok 76 token mengulang 62 unit, biaya tetap Rp28,12 juta, dan kontribusi Rp498.375. |
| Simpulan | 19 | 23 | Dua blok identik 182 dan 91 token merangkum operasi, pasar, kelayakan, payback 4,5 bulan, dan BEP 62 unit. |

Pengulangan driver dan simpulan harus dibaca bersama kelemahannya. Rp28,12 juta ÷ Rp498.375 = 56,42 unit, sehingga kebutuhan minimal menjadi 57 unit bila semua asumsi itu lengkap; angka 62 membutuhkan dasar tambahan. Biaya/modal dan beberapa hasil keuangan juga belum satu dasar. BPC-28 menyebut Rp2,1 juta di bagian harga halaman 12 tetapi Rp2,2 juta pada proyeksi halaman 15; BPC-58 memakai Rp2,2 juta dalam proyeksi halaman 17. Konsistensi harga yang lebih baik pada suatu bagian tidak membuktikan penjualan tercapai.

Untuk pembelajaran, kelompokkan keduanya sebagai contoh yang saling terkait. Ambil cara menghubungkan perangkat, perakitan/QC, pemesanan, dan purna jual; audit volume, modal, serta rumusnya dari awal. Jangan menjumlahkan dua dokumen menjadi dua survei, dua keberhasilan komersial, atau dua pengujian lapangan. Tidak ada kesimpulan mengenai urutan penulisan, hak, atau pelanggaran yang dapat ditetapkan dari perbandingan ini.

