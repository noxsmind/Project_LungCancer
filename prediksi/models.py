from django.db import models
from django.contrib.auth.models import User 

class RiwayatDeteksi(models.Model):
    # Hubungkan riwayat ini ke akun User yang sedang login
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nama_pasien = models.CharField(max_length=100)
    tanggal_tes = models.DateTimeField(auto_now_add=True)
    
    # Gejala
    smoking = models.IntegerField()
    mental_stress = models.IntegerField()
    exposure_to_pollution = models.IntegerField()
    energy_level = models.IntegerField()
    immune_weakness = models.IntegerField()
    breathing_issue = models.IntegerField()
    throat_discomfort = models.IntegerField()
    family_history = models.IntegerField()
    smoking_family_history = models.IntegerField()
    stress_immune = models.IntegerField()
    
    hasil_prediksi = models.IntegerField(null=True, blank=True)

    def __str__(self):
        # PERBAIKAN: Cek dulu apakah user-nya ada. Jika tidak ada, beri nama "Anonim"
        nama_pengguna = self.user.username if self.user else "Anonim"
        return f"{nama_pengguna} - {self.nama_pasien} ({self.tanggal_tes.strftime('%d/%m/%Y')})"