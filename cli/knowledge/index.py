"""Document indexing and search functionality for Document Library."""

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional
import math

# Document Library path (relative to project root)
DOCUMENT_LIBRARY_PATH = Path("docs/library")
INDEX_CACHE_PATH = Path("config/knowledge_index.json")


@dataclass
class IndexEntry:
    """A single indexed document."""
    name: str
    path: str
    doc_type: str  # 'markdown' or 'docx'
    title: str
    content: str
    terms: Dict[str, int] = field(default_factory=dict)  # term -> frequency


@dataclass
class SearchResult:
    """A search result with relevance score."""
    name: str
    path: str
    title: str
    score: float
    snippet: str


class DocumentIndex:
    """Index for searching Document Library contents."""

    def __init__(self):
        self.entries: Dict[str, IndexEntry] = {}
        self.idf: Dict[str, float] = {}  # Inverse document frequency
        self._loaded = False

    def build_index(self, force: bool = False) -> int:
        """Build or rebuild the document index.

        Returns the number of documents indexed.
        """
        if not DOCUMENT_LIBRARY_PATH.exists():
            return 0

        self.entries = {}

        # Index markdown files
        for md_file in DOCUMENT_LIBRARY_PATH.glob("*.md"):
            entry = self._index_markdown(md_file)
            if entry:
                self.entries[entry.name] = entry

        # Index Word documents
        for docx_file in DOCUMENT_LIBRARY_PATH.glob("*.docx"):
            entry = self._index_docx(docx_file)
            if entry:
                self.entries[entry.name] = entry

        # Calculate IDF scores
        self._calculate_idf()

        # Cache the index
        self._save_cache()
        self._loaded = True

        return len(self.entries)

    def _index_markdown(self, path: Path) -> Optional[IndexEntry]:
        """Index a markdown file."""
        try:
            content = path.read_text(encoding="utf-8")
            title = self._extract_title(content, path.stem)
            terms = self._tokenize(content)

            return IndexEntry(
                name=path.name,
                path=str(path),
                doc_type="markdown",
                title=title,
                content=content,
                terms=terms
            )
        except Exception:
            return None

    def _index_docx(self, path: Path) -> Optional[IndexEntry]:
        """Index a Word document using python-docx."""
        try:
            from docx import Document
            doc = Document(str(path))

            # Extract text from paragraphs
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            content = "\n".join(paragraphs)

            # Use first paragraph or filename as title
            title = paragraphs[0][:100] if paragraphs else path.stem
            terms = self._tokenize(content)

            return IndexEntry(
                name=path.name,
                path=str(path),
                doc_type="docx",
                title=title,
                content=content,
                terms=terms
            )
        except ImportError:
            # python-docx not installed, create placeholder entry
            return IndexEntry(
                name=path.name,
                path=str(path),
                doc_type="docx",
                title=path.stem,
                content=f"[Word document - install python-docx to index: {path.name}]",
                terms={}
            )
        except Exception:
            return None

    def _extract_title(self, content: str, fallback: str) -> str:
        """Extract title from markdown content."""
        # Look for # heading
        for line in content.split("\n")[:10]:
            if line.startswith("# "):
                return line[2:].strip()
        return fallback

    def _tokenize(self, text: str) -> Dict[str, int]:
        """Tokenize text and return term frequencies."""
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-z][a-z0-9]+\b', text.lower())
        # Filter stopwords
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                     'can', 'and', 'or', 'but', 'if', 'then', 'else', 'when',
                     'at', 'by', 'for', 'with', 'about', 'against', 'between',
                     'into', 'through', 'during', 'before', 'after', 'above',
                     'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on',
                     'off', 'over', 'under', 'again', 'further', 'then', 'once',
                     'here', 'there', 'all', 'each', 'few', 'more', 'most',
                     'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                     'same', 'so', 'than', 'too', 'very', 'just', 'this', 'that'}
        filtered = [w for w in words if w not in stopwords and len(w) > 2]
        return Counter(filtered)

    def _calculate_idf(self):
        """Calculate inverse document frequency for all terms."""
        if not self.entries:
            return

        num_docs = len(self.entries)
        term_doc_count: Dict[str, int] = Counter()

        for entry in self.entries.values():
            for term in entry.terms:
                term_doc_count[term] += 1

        self.idf = {
            term: math.log(num_docs / count)
            for term, count in term_doc_count.items()
        }

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search documents using TF-IDF scoring."""
        self._ensure_loaded()

        if not self.entries:
            return []

        query_terms = self._tokenize(query)
        if not query_terms:
            # If no valid tokens, do substring search
            return self._substring_search(query, top_k)

        results = []
        for entry in self.entries.values():
            score = self._calculate_score(query_terms, entry)
            if score > 0:
                snippet = self._extract_snippet(entry.content, list(query_terms.keys()))
                results.append(SearchResult(
                    name=entry.name,
                    path=entry.path,
                    title=entry.title,
                    score=score,
                    snippet=snippet
                ))

        # Sort by score descending
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def _substring_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Fallback substring search for short queries."""
        query_lower = query.lower()
        results = []

        for entry in self.entries.values():
            if query_lower in entry.content.lower():
                snippet = self._extract_snippet(entry.content, [query])
                results.append(SearchResult(
                    name=entry.name,
                    path=entry.path,
                    title=entry.title,
                    score=1.0,
                    snippet=snippet
                ))

        return results[:top_k]

    def _calculate_score(self, query_terms: Dict[str, int], entry: IndexEntry) -> float:
        """Calculate TF-IDF score for a document against query."""
        score = 0.0
        for term, query_freq in query_terms.items():
            if term in entry.terms:
                tf = entry.terms[term]
                idf = self.idf.get(term, 0)
                score += tf * idf * query_freq
        return score

    def _extract_snippet(self, content: str, terms: List[str], max_len: int = 150) -> str:
        """Extract a relevant snippet containing search terms."""
        content_lower = content.lower()

        # Find first occurrence of any term
        best_pos = len(content)
        for term in terms:
            pos = content_lower.find(term.lower())
            if 0 <= pos < best_pos:
                best_pos = pos

        if best_pos == len(content):
            # No term found, return beginning
            best_pos = 0

        # Extract snippet around the term
        start = max(0, best_pos - 30)
        end = min(len(content), start + max_len)

        snippet = content[start:end]

        # Clean up snippet
        snippet = " ".join(snippet.split())  # Normalize whitespace
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."

        return snippet

    def get_document(self, name: str) -> Optional[str]:
        """Get full content of a document by name."""
        self._ensure_loaded()

        # Try exact match
        if name in self.entries:
            return self.entries[name].content

        # Try case-insensitive match
        name_lower = name.lower()
        for entry_name, entry in self.entries.items():
            if entry_name.lower() == name_lower:
                return entry.content

        # Try partial match
        for entry_name, entry in self.entries.items():
            if name_lower in entry_name.lower():
                return entry.content

        return None

    def list_documents(self) -> List[Dict[str, str]]:
        """List all indexed documents."""
        self._ensure_loaded()

        return [
            {
                "name": entry.name,
                "title": entry.title,
                "type": entry.doc_type
            }
            for entry in self.entries.values()
        ]

    def _ensure_loaded(self):
        """Ensure the index is loaded."""
        if not self._loaded:
            if not self._load_cache():
                self.build_index()

    def _save_cache(self):
        """Save index to cache file."""
        try:
            INDEX_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            cache_data = {
                "entries": {
                    name: {
                        "name": e.name,
                        "path": e.path,
                        "doc_type": e.doc_type,
                        "title": e.title,
                        "content": e.content,
                        "terms": e.terms
                    }
                    for name, e in self.entries.items()
                },
                "idf": self.idf
            }
            INDEX_CACHE_PATH.write_text(json.dumps(cache_data, indent=2), encoding="utf-8")
        except Exception:
            pass  # Cache is optional

    def _load_cache(self) -> bool:
        """Load index from cache file."""
        try:
            if not INDEX_CACHE_PATH.exists():
                return False

            cache_data = json.loads(INDEX_CACHE_PATH.read_text(encoding="utf-8"))

            self.entries = {
                name: IndexEntry(**data)
                for name, data in cache_data.get("entries", {}).items()
            }
            self.idf = cache_data.get("idf", {})
            self._loaded = True
            return True
        except Exception:
            return False


# Module-level singleton
_index: Optional[DocumentIndex] = None


def _get_index() -> DocumentIndex:
    """Get or create the document index singleton."""
    global _index
    if _index is None:
        _index = DocumentIndex()
    return _index


def search_documents(query: str, top_k: int = 5) -> List[SearchResult]:
    """Search Document Library for matching documents."""
    return _get_index().search(query, top_k)


def get_document(name: str) -> Optional[str]:
    """Get full content of a document by name."""
    return _get_index().get_document(name)


def list_documents() -> List[Dict[str, str]]:
    """List all documents in the Document Library."""
    return _get_index().list_documents()


def refresh_index() -> int:
    """Rebuild the document index. Returns number of documents indexed."""
    return _get_index().build_index(force=True)
