"""Configuration module containing mock knowledge bases and system settings."""

MOCK_RESEARCH = {
    "apple": {
        "company_name": "Apple Inc.",
        "recent_news": "Launched Vision Pro, expanding services revenue and spatial computing software ecosystems.",
        "stock_info": "Trading at $195, up 45% YTD with strong institutional inflows.",
        "key_developments": "Deep AI integration (Apple Intelligence) across iOS, iPadOS, and macOS product lines."
    },
    "tesla": {
        "company_name": "Tesla Inc.",
        "recent_news": "Cybertruck deliveries ramping up across North American production lines.",
        "stock_info": "Trading at $242, showing a volatile quarter but solid automotive gross margins.",
        "key_developments": "Full Self-Driving (FSD) v12 rollout expands; structural energy storage utility scaling rapidly."
    },
    "google": {
        "company_name": "Alphabet Inc. (Google)",
        "recent_news": "Gemini Ultra models integrated natively into core workspace suites and cloud infrastructures.",
        "stock_info": "Trading at $175, up 24% YTD driven by robust digital ads and Enterprise Cloud growth.",
        "key_developments": "Custom TPU v5p accelerators deployed across global AI hyper-computing data centers."
    }
}

# Thresholds and System Limits
MINIMUM_CONFIDENCE_SCORE = 6.0
MAXIMUM_RESEARCH_ATTEMPTS = 3
