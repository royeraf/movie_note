"""
Movie search endpoint - Ultra-optimized version.
Uses only the search results (no extra API calls for details).
"""
import asyncio
import httpx
from fastapi import APIRouter
from api.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/")
async def search_movies(query: str):
    """
    Search for movies. Uses TMDB (Spanish) with OMDB fallback.
    Ultra-fast: uses only search results, no detail API calls.
    """
    # Try TMDB first for Spanish support
    if settings.TMDB_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                search_url = f"https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&language=es-ES&query={query}"
                response = await client.get(search_url)
                search_data = response.json()
                
                if "results" in search_data and search_data["results"]:
                    results = []
                    for item in search_data["results"][:8]:
                        release_date = item.get("release_date", "")
                        year = release_date.split("-")[0] if release_date else "N/A"
                        
                        results.append({
                            "imdbID": f"tmdb_{item['id']}",
                            "Title": item.get("title"),
                            "Year": year,
                            # w342 = 342px width, smaller = faster loading
                            "Poster": f"https://image.tmdb.org/t/p/w342{item.get('poster_path')}" if item.get("poster_path") else "N/A",
                            "Actors": "",  # Not available in search, will be populated if needed
                            "Plot": item.get("overview"),
                            "description": item.get("overview")
                        })
                    return {"Search": results}
        except Exception as e:
            print(f"TMDB Search failed: {e}")
    
    # Fallback to OMDB
    if not settings.OMDB_API_KEY:
        return {"error": "No API keys configured"}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&s={query}&type=movie"
            response = await client.get(url)
            search_data = response.json()
            
            if "Search" in search_data:
                # OMDB search doesn't include Plot, need to fetch details
                # Do it in parallel for speed
                async def fetch_detail(imdb_id: str) -> dict:
                    detail_url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&i={imdb_id}"
                    resp = await client.get(detail_url)
                    detail = resp.json()
                    if "Plot" in detail:
                        detail["description"] = detail["Plot"]
                    return detail
                
                tasks = [fetch_detail(item["imdbID"]) for item in search_data["Search"][:8]]
                detailed = await asyncio.gather(*tasks, return_exceptions=True)
                
                results = [r for r in detailed if isinstance(r, dict)]
                return {"Search": results}
            
            return search_data
    except Exception as e:
        print(f"OMDB Search failed: {e}")
        return {"error": str(e)}


@router.get("/details/{movie_id}")
async def get_movie_details(movie_id: str):
    """
    Get full movie details including actors.
    Call this when user clicks on a movie for more info.
    """
    if movie_id.startswith("tmdb_"):
        # TMDB movie
        tmdb_id = movie_id.replace("tmdb_", "")
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={settings.TMDB_API_KEY}&language=es-ES&append_to_response=credits"
            response = await client.get(url)
            detail = response.json()
            
            actors = ", ".join([c["name"] for c in detail.get("credits", {}).get("cast", [])[:5]])
            release_date = detail.get("release_date", "")
            year = release_date.split("-")[0] if release_date else "N/A"
            
            return {
                "imdbID": movie_id,
                "Title": detail.get("title"),
                "Year": year,
                "Poster": f"https://image.tmdb.org/t/p/w500{detail.get('poster_path')}" if detail.get("poster_path") else "N/A",
                "Actors": actors,
                "Plot": detail.get("overview"),
                "description": detail.get("overview")
            }
    else:
        # OMDB movie
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&i={movie_id}"
            response = await client.get(url)
            detail = response.json()
            if "Plot" in detail:
                detail["description"] = detail["Plot"]
            return detail
