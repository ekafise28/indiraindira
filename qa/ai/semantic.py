from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from qa.models import PermenparDataset


class SemanticSearchAI:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000
        )

    def _build_index(self, queryset):
        documents = []
        records = []

        for row in queryset:
            teks = row.teks or ""
            keywords = row.kata_kunci or ""

            documents.append(
                f"{row.kategori or ''} "
                f"{row.sub_kategori or ''} "
                f"{teks} "
                f"{keywords}"
            )
            records.append(row)

        matrix = self.vectorizer.fit_transform(documents)
        return matrix, records

    def detect_kategori(self, query):
        q = query.lower()

        if any(k in q for k in ["wajib", "kewajiban", "harus"]):
            return "kewajiban"

        if any(k in q for k in ["izin", "persyaratan", "syarat"]):
            return "persyaratan"

        if any(k in q for k in ["definisi", "pengertian"]):
            return "definisi"

        if any(k in q for k in ["sdm", "tenaga kerja"]):
            return "SDM"

        if any(k in q for k in ["sarana", "prasarana"]):
            return "sarana"

        if any(k in q for k in ["manajemen"]):
            return "manajemen"

        return None

    def search(self, query, kbli=None, top_n=3):
        qs = PermenparDataset.objects.filter(status_aktif=True)

        if kbli:
            qs = qs.filter(kbli__icontains=kbli)

        kategori = self.detect_kategori(query)
        if kategori:
            qs = qs.filter(kategori__icontains=kategori)

            # 🎯 Perkuat dengan sub_kategori bila ada
            if qs.filter(sub_kategori__icontains=kategori).exists():
                qs = qs.filter(sub_kategori__icontains=kategori)

        if not qs.exists():
            return []

        matrix, records = self._build_index(qs)
        query_vec = self.vectorizer.transform([query])
        similarity = cosine_similarity(query_vec, matrix)[0]

        ranked = sorted(
            enumerate(similarity),
            key=lambda x: x[1],
            reverse=True
        )

        results = []
        for idx, score in ranked[:top_n]:
            if score > 0.01:
                results.append({
                    "score": round(float(score), 3),
                    "data": records[idx]
                })

        if not results and records:
            results.append({
                "score": 0.0,
                "data": records[0]
            })

        return results
