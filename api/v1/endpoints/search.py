import requests
from fastapi import APIRouter, Depends
from api.core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/")
def search_movies(query: str):
    # Try TMDB first for Spanish support if key is available
    if settings.TMDB_API_KEY:
        try:
            # Search on TMDB
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&language=es-ES&query={query}"
            search_data = requests.get(search_url).json()
            
            if "results" in search_data:
                detailed_results = []
                # Take top 8
                for item in search_data["results"][:8]:
                    movie_id = item["id"]
                    # Get details (including actors/credits)
                    detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}&language=es-ES&append_to_response=credits"
                    detail = requests.get(detail_url).json()
                    
                    # Map TMDB to OMDB-like format for frontend compatibility
                    actors = ", ".join([c["name"] for c in detail.get("credits", {}).get("cast", [])[:5]])
                    release_date = detail.get("release_date", "")
                    year = release_date.split("-")[0] if release_date else "N/A"
                    
                    mapped = {
                        "imdbID": f"tmdb_{movie_id}", # Prefix to distinguish
                        "Title": detail.get("title"),
                        "Year": year,
                        "Poster": f"https://image.tmdb.org/t/p/w500{detail.get('poster_path')}" if detail.get("poster_path") else "N/A",
                        "Actors": actors,
                        "Plot": detail.get("overview"),
                        "description": detail.get("overview")
                    }
                    detailed_results.append(mapped)
                return {"Search": detailed_results}
        except Exception as e:
            print(f"TMDB Search failed: {e}")

    # Fallback to OMDB
    if not settings.OMDB_API_KEY:
        return {"error": "No API keys configured"}
    
    url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&s={query}&type=movie"
    search_response = requests.get(url).json()
    
    if "Search" in search_response:
        results = search_response["Search"][:8]
        detailed_results = []
        for item in results:
            detail_url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&i={item['imdbID']}"
            detail = requests.get(detail_url).json()
            # Map OMDB Plot to description
            if "Plot" in detail:
                 detail["description"] = detail["Plot"]
            detailed_results.append(detail)
        return {"Search": detailed_results}
        
    return search_response
