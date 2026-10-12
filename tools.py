"""Tools module processing data lookup with local mock overrides."""

from typing import Dict, Any, Optional
from config import MOCK_RESEARCH


class CompanySearchTool:
    """Enterprise mock fallback lookups to guarantee deterministic testing execution states."""

    @staticmethod
    def search(query: str, target_company: Optional[str] = None) -> Dict[str, Any]:
        """Queries the internal registry or mimics an automated extraction parsing mechanism."""
        if not target_company:
            # Simple heuristic matching fallback if company isn't cleanly isolated in metadata
            normalized_query = query.lower()
            if "apple" in normalized_query:
                target_company = "apple"
            elif "tesla" in normalized_query:
                target_company = "tesla"
            elif "google" in normalized_query:
                target_company = "google"
            else:
                return {
                    "error": "No exact matching company portfolio discovered in the data repository.",
                    "query_received": query
                }

        lookup_key = target_company.lower().strip()
        if lookup_key in MOCK_RESEARCH:
            return {
                "status": "success",
                "data": MOCK_RESEARCH[lookup_key]
            }

        return {
            "status": "partial_success",
            "data": {
                "company_name": target_company.capitalize(),
                "recent_news": "No verified press index found for this identifier.",
                "stock_info": "Market capital metrics currently unavailable.",
                "key_developments": f"General structural search query executed for: {query}"
            }
        }
