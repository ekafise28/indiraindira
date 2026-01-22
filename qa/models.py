from django.db import models

class PermenparDataset(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    regulasi = models.CharField(max_length=100)
    kbli = models.CharField(max_length=10)
    nama_kbli = models.CharField(max_length=255)
    tingkat_risiko = models.CharField(max_length=50, null=True, blank=True)

    bab = models.CharField(max_length=100, null=True, blank=True)
    pasal = models.CharField(max_length=20, null=True, blank=True)
    sub_pasal = models.CharField(max_length=20, null=True, blank=True)
    butir = models.CharField(max_length=20, null=True, blank=True)

    kategori = models.CharField(max_length=100, null=True, blank=True)
    sub_kategori = models.CharField(max_length=100, null=True, blank=True)

    teks = models.TextField()
    kata_kunci = models.TextField(null=True, blank=True)

    status_aktif = models.BooleanField(default=True)
    catatan = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "permenpar_dataset"
        managed = False

    def __str__(self):
        return f"{self.regulasi} Pasal {self.pasal}"
