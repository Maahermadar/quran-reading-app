import logging

# Setup logging
logger = logging.getLogger("uvicorn.error")

# Path to the dataset
# Assuming it's in the root of the project (one level above 'backend')
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "frontend", "assets", "data", "madani-muhsaf.json")

_data = None

def _load_data():
    global _data
    if _data is None:
        if os.path.exists(DATASET_PATH):
            try:
                # Log file size to verify it's not empty
                file_size = os.path.getsize(DATASET_PATH)
                logger.info(f"Loading Madani Mushaf data from {DATASET_PATH} ({file_size} bytes)")
                
                with open(DATASET_PATH, 'r', encoding='utf-8') as f:
                    _data = json.load(f)
                
                logger.info(f"Successfully loaded {len(_data)} pages of Madani Mushaf data")
            except Exception as e:
                logger.error(f"CRITICAL: Failed to parse Madani Mushaf JSON: {e}")
                _data = []
        else:
            logger.error(f"CRITICAL: Madani Mushaf dataset NOT FOUND at {DATASET_PATH}")
            _data = []

def get_data_for_page(page: int):
    global _data
    _load_data()
    
    # If _data is empty (failed to load), try one more time if it's the first real attempt
    if (not _data or len(_data) == 0) and os.path.exists(DATASET_PATH):
        _load_data()

    # page is 1-indexed, index 0 is empty in the dataset
    if _data and 1 <= page < len(_data):
        return _data[page]
    
    logger.warning(f"No data found for page {page} (Dataset size: {len(_data) if _data else 0})")
    return None

def get_surah_info_for_page(page: int):
    page_data = get_data_for_page(page)
    if not page_data:
        return None
    
    # Filter out "juzNumber" key to find surah keys
    surah_keys = [k for k in page_data.keys() if k != "juzNumber"]
    if not surah_keys:
        return None
    
    # Take the first surah on the page as requested
    first_surah_key = surah_keys[0]
    surah_data = page_data[first_surah_key]
    
    return {
        "name_en": surah_data.get("titleEn"),
        "name_ar": f"سورة {surah_data.get('titleAr')}",
        "number": surah_data.get("chapterNumber")
    }

def get_juz_for_page(page: int):
    page_data = get_data_for_page(page)
    if page_data and "juzNumber" in page_data:
        return page_data["juzNumber"]
    # Fallback to rough calculation if data missing
    return ((page - 1) // 20) + 1
