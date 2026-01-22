from qa.models import PermenparDataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class KBLIDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=3000
        )
        self._build_index()

    def _build_index(self):
        self.records = []
        documents = []

        qs = PermenparDataset.objects.filter(status_aktif=True)

        for row in qs:
            text = f"{row.nama_kbli or ''} {row.kata_kunci or ''} {row.teks or ''}"
            documents.append(text)
            self.records.append(row.kbli)

        self.matrix = self.vectorizer.fit_transform(documents)

    def detect(self, query):
        query_vec = self.vectorizer.transform([query])
        similarity = cosine_similarity(query_vec, self.matrix)[0]

        best_idx = similarity.argmax()
        best_score = similarity[best_idx]

        if best_score < 0.05:
            return None

        return self.records[best_idx]
