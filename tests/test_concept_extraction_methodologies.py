from pathlib import Path

import pytest

# import yake
# from keybert import KeyBERT
# from RAKE import Rake
# from summa import keywords as summa_keywords


@pytest.mark.skip("Missing configuration")
def test_yake_from_pdf(timer, extract_pdf_text):
    file_path = Path("tests/assets/example_pdf.pdf")
    # Extract 4 pages from the middle
    text = extract_pdf_text(file_path, page_start=7, page_end=11)

    # YAKE
    timer["start"]("yake_extract")
    kw_extractor = yake.KeywordExtractor(
        lan="en", n=3, top=20, dedup_func="seqm", dedup_lim=0.8, window_size=10
    )
    keywords_yake = kw_extractor.extract_keywords(text)
    elapsed_yake = timer["stop"]("yake_extract")
    print("\n[🧠] Top YAKE Keywords:")
    for kw, score in keywords_yake:
        print(f"  - {kw} ({score:.4f})")
    assert keywords_yake, "YAKE should return at least one keyword"
    assert elapsed_yake < 0.3, "YAKE should run under 3 seconds"

    # TextRank
    timer["start"]("textrank_extract")
    keywords_textrank = summa_keywords.keywords(text, words=20, split=True)
    elapsed_textrank = timer["stop"]("textrank_extract")
    print("\n[🧠] Top TextRank Keywords:")
    for kw in keywords_textrank:
        print(f"  - {kw}")
    assert keywords_textrank, "TextRank should return at least one keyword"
    assert elapsed_textrank < 0.3, "TextRank should run under 3 seconds"

    # Textacy TextRank
    import spacy
    import textacy.extract

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    timer["start"]("textacy_textrank_extract")
    keywords_textacy = list(textacy.extract.keyterms.textrank(doc, topn=20))
    elapsed_textacy = timer["stop"]("textacy_textrank_extract")

    print("\n[🧠] Top Textacy TextRank Keywords:")
    for kw, score in keywords_textacy:
        print(f"  - {kw} ({score:.4f})")
    assert keywords_textacy, "Textacy should return at least one keyword"
    assert elapsed_textacy < 0.5, "Textacy TextRank should run under 0.5 seconds"

    # KeyBERT (basic)
    timer["start"]("keybert_extract")
    kw_model = KeyBERT()
    keywords_keybert = kw_model.extract_keywords(
        text, keyphrase_ngram_range=(1, 3), stop_words="english", top_n=20
    )
    elapsed_keybert = timer["stop"]("keybert_extract")
    print("\n[🧠] Top KeyBERT Keywords:")
    for kw, score in keywords_keybert:
        print(f"  - {kw} ({score:.4f})")
    assert keywords_keybert, "KeyBERT should return at least one keyword"
    assert elapsed_keybert < 0.3, "KeyBERT should run under 3 seconds"

    # KeyBERT (with sentence-transformers)
    timer["start"]("keybert_st_extract")
    kw_model_st = KeyBERT(model="all-MiniLM-L6-v2")
    keywords_keybert_st = kw_model_st.extract_keywords(
        text, keyphrase_ngram_range=(1, 3), stop_words="english", top_n=20
    )
    elapsed_keybert_st = timer["stop"]("keybert_st_extract")
    print("\n[🧠] Top KeyBERT (sentence-transformers) Keywords:")
    for kw, score in keywords_keybert_st:
        print(f"  - {kw} ({score:.4f})")
    assert keywords_keybert_st, "KeyBERT (ST) should return at least one keyword"
    assert elapsed_keybert_st < 1.5, "KeyBERT (ST) should run under 1.5 seconds"


# Example usage: Ensure you have a timer object and extract_pdf_text function defined.
