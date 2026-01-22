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
            documents.append(f"{teks} {keywords}")
            records.append(row)

        matrix = self.vectorizer.fit_transform(documents)
        return matrix, records

    def search(self, query, kbli=None, top_n=3):
        qs = PermenparDataset.objects.filter(status_aktif=True)

        # 🔥 FILTER UTAMA BERDASARKAN KBLI
        if kbli:
            qs = qs.filter(kbli=kbli)

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
            if score > 0.05:
                results.append({
                    "score": round(float(score), 3),
                    "data": records[idx]
                })

        return results
