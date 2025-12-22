"""Tests for cli/knowledge/index.py module."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from cli.knowledge.index import (
    IndexEntry, SearchResult, DocumentIndex,
    search_documents, get_document, list_documents, refresh_index,
    _get_index, DOCUMENT_LIBRARY_PATH, INDEX_CACHE_PATH
)


class TestIndexEntry:
    """Tests for IndexEntry dataclass."""

    def test_index_entry_creation(self):
        """Test creating an IndexEntry instance."""
        entry = IndexEntry(
            name="test.md",
            path="/path/to/test.md",
            doc_type="markdown",
            title="Test Document",
            content="Test content here",
            terms={"test": 2, "content": 1}
        )
        assert entry.name == "test.md"
        assert entry.doc_type == "markdown"
        assert entry.terms["test"] == 2

    def test_index_entry_default_terms(self):
        """Test IndexEntry with default terms."""
        entry = IndexEntry(
            name="test.md",
            path="/path/to/test.md",
            doc_type="markdown",
            title="Test",
            content="Content"
        )
        assert entry.terms == {}


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_search_result_creation(self):
        """Test creating a SearchResult instance."""
        result = SearchResult(
            name="test.md",
            path="/path/to/test.md",
            title="Test Document",
            score=0.95,
            snippet="...relevant snippet..."
        )
        assert result.name == "test.md"
        assert result.score == 0.95
        assert "snippet" in result.snippet


class TestDocumentIndex:
    """Tests for DocumentIndex class."""

    def test_index_initialization(self):
        """Test DocumentIndex initialization."""
        index = DocumentIndex()
        assert index.entries == {}
        assert index.idf == {}
        assert index._loaded is False

    def test_tokenize_basic(self):
        """Test basic tokenization."""
        index = DocumentIndex()
        terms = index._tokenize("Hello World Testing")
        # "hello" is filtered (too short after lowercase), "world" and "testing" should be there
        assert "testing" in terms
        assert "world" in terms

    def test_tokenize_stopwords_filtered(self):
        """Test that stopwords are filtered."""
        index = DocumentIndex()
        terms = index._tokenize("the quick and the slow")
        # "the", "and" are stopwords
        assert "the" not in terms
        assert "and" not in terms
        assert "quick" in terms
        assert "slow" in terms

    def test_tokenize_short_words_filtered(self):
        """Test that short words (<=2 chars) are filtered."""
        index = DocumentIndex()
        terms = index._tokenize("a an it code")
        assert "code" in terms
        assert "a" not in terms
        assert "an" not in terms

    def test_tokenize_case_insensitive(self):
        """Test that tokenization is case-insensitive."""
        index = DocumentIndex()
        terms = index._tokenize("HELLO hello Hello")
        assert "hello" in terms
        assert terms["hello"] == 3

    def test_extract_title_with_heading(self):
        """Test title extraction from markdown with heading."""
        index = DocumentIndex()
        content = "# My Title\n\nSome content here"
        title = index._extract_title(content, "fallback")
        assert title == "My Title"

    def test_extract_title_fallback(self):
        """Test title extraction fallback."""
        index = DocumentIndex()
        content = "No heading here\nJust content"
        title = index._extract_title(content, "fallback_title")
        assert title == "fallback_title"

    def test_extract_snippet_with_term(self):
        """Test snippet extraction around a term."""
        index = DocumentIndex()
        content = "This is some content with important information in the middle of the text."
        snippet = index._extract_snippet(content, ["important"], max_len=50)
        assert "important" in snippet.lower()

    def test_extract_snippet_no_term_found(self):
        """Test snippet extraction when term not found."""
        index = DocumentIndex()
        content = "This is some content without the search term."
        snippet = index._extract_snippet(content, ["missing"], max_len=50)
        # Should return beginning of content
        assert "This" in snippet

    def test_build_index_empty_path(self, tmp_path, monkeypatch):
        """Test building index with non-existent path."""
        index = DocumentIndex()
        # Patch the DOCUMENT_LIBRARY_PATH
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', tmp_path / "nonexistent"):
            count = index.build_index()
            assert count == 0

    def test_build_index_with_markdown(self, temp_docs_library, monkeypatch):
        """Test building index with markdown files."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                count = index.build_index()
                assert count >= 1  # Should index at least one file
                assert index._loaded is True

    def test_index_markdown_file(self, temp_docs_library):
        """Test indexing a single markdown file."""
        index = DocumentIndex()
        md_file = temp_docs_library / "test_commands.md"
        entry = index._index_markdown(md_file)

        assert entry is not None
        assert entry.name == "test_commands.md"
        assert entry.doc_type == "markdown"
        assert "Test Commands Reference" in entry.title

    def test_search_with_results(self, temp_docs_library):
        """Test search returning results."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                index.build_index()
                # Search for "commands" which appears in the test fixture
                results = index.search("commands reference", top_k=5)
                assert len(results) > 0
                assert all(isinstance(r, SearchResult) for r in results)

    def test_search_no_results(self, temp_docs_library):
        """Test search with no matching results."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                index.build_index()
                results = index.search("xyznonexistent123", top_k=5)
                assert results == []

    def test_search_respects_top_k(self, temp_docs_library):
        """Test that search respects top_k limit."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                index.build_index()
                results = index.search("commands", top_k=1)
                assert len(results) <= 1

    def test_get_document_exact_match(self, temp_docs_library):
        """Test getting document by exact name."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                index.build_index()
                content = index.get_document("test_commands.md")
                assert content is not None
                assert "Claude CLI" in content

    def test_get_document_case_insensitive(self, temp_docs_library):
        """Test getting document case-insensitively."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                index.build_index()
                content = index.get_document("TEST_COMMANDS.MD")
                assert content is not None

    def test_get_document_partial_match(self, temp_docs_library):
        """Test getting document by partial name."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                index.build_index()
                content = index.get_document("commands")
                assert content is not None

    def test_get_document_not_found(self, temp_docs_library):
        """Test getting non-existent document."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                index.build_index()
                content = index.get_document("nonexistent.md")
                assert content is None

    def test_list_documents(self, temp_docs_library):
        """Test listing all documents."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                index.build_index()
                docs = index.list_documents()
                assert len(docs) >= 1
                assert all("name" in d and "title" in d and "type" in d for d in docs)

    def test_calculate_idf(self):
        """Test IDF calculation."""
        index = DocumentIndex()
        index.entries = {
            "doc1": IndexEntry(
                name="doc1", path="", doc_type="markdown",
                title="Doc 1", content="", terms={"common": 1, "unique1": 1}
            ),
            "doc2": IndexEntry(
                name="doc2", path="", doc_type="markdown",
                title="Doc 2", content="", terms={"common": 1, "unique2": 1}
            )
        }
        index._calculate_idf()

        # "common" appears in both docs, should have lower IDF
        # "unique1" and "unique2" appear in one doc each, should have higher IDF
        assert index.idf["common"] < index.idf["unique1"]
        assert index.idf["common"] < index.idf["unique2"]


class TestModuleFunctions:
    """Tests for module-level functions."""

    def test_search_documents(self, temp_docs_library):
        """Test search_documents function."""
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                with patch('cli.knowledge.index._index', None):
                    results = search_documents("workflow")
                    # Results depend on actual content
                    assert isinstance(results, list)

    def test_get_document_function(self, temp_docs_library):
        """Test get_document function."""
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                with patch('cli.knowledge.index._index', None):
                    content = get_document("test_commands.md")
                    # Content depends on fixture

    def test_list_documents_function(self, temp_docs_library):
        """Test list_documents function."""
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                with patch('cli.knowledge.index._index', None):
                    docs = list_documents()
                    assert isinstance(docs, list)

    def test_refresh_index(self, temp_docs_library):
        """Test refresh_index function."""
        with patch('cli.knowledge.index.DOCUMENT_LIBRARY_PATH', temp_docs_library):
            with patch('cli.knowledge.index.INDEX_CACHE_PATH', temp_docs_library / "cache.json"):
                with patch('cli.knowledge.index._index', None):
                    count = refresh_index()
                    assert count >= 1


class TestCaching:
    """Tests for index caching functionality."""

    def test_save_and_load_cache(self, tmp_path):
        """Test saving and loading cache."""
        cache_path = tmp_path / "cache.json"
        index = DocumentIndex()

        # Add some entries
        index.entries = {
            "test.md": IndexEntry(
                name="test.md", path="/test.md", doc_type="markdown",
                title="Test", content="Test content", terms={"test": 1}
            )
        }
        index.idf = {"test": 0.5}

        with patch('cli.knowledge.index.INDEX_CACHE_PATH', cache_path):
            index._save_cache()
            assert cache_path.exists()

            # Create new index and load
            index2 = DocumentIndex()
            loaded = index2._load_cache()
            assert loaded is True
            assert "test.md" in index2.entries

    def test_load_cache_missing_file(self, tmp_path):
        """Test loading cache when file doesn't exist."""
        index = DocumentIndex()
        with patch('cli.knowledge.index.INDEX_CACHE_PATH', tmp_path / "nonexistent.json"):
            loaded = index._load_cache()
            assert loaded is False
