from rest_framework.decorators import api_view
from rest_framework.response import Response
from qa.ai.semantic import SemanticSearchAI
from qa.ai.formatter import format_jawaban

ai_engine = SemanticSearchAI()


@api_view(["POST"])
def tanya_ai(request):
    pertanyaan = request.data.get("pertanyaan")
    kbli = request.data.get("kbli")

    if not pertanyaan:
        return Response(
            {"error": "Pertanyaan tidak boleh kosong"},
            status=400
        )

    if not kbli:
        return Response(
            {"error": "KBLI wajib diisi"},
            status=400
        )

    results = ai_engine.search(
        query=pertanyaan,
        kbli=kbli
    )

    output = format_jawaban(results, pertanyaan)
    output["kbli"] = kbli

    return Response(output)
