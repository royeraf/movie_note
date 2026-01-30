export type MovieStatus = 'to-watch' | 'watched';

export interface Movie {
  id?: number;
  imdb_id: string;
  title: string;
  poster_path: string | null;
  release_year: string | null;
  status: MovieStatus;
  color?: string;
  actors?: string;
  description?: string;
  is_favorite?: boolean;
}

export interface OMDBMovie {
  imdbID: string;
  Title: string;
  Poster: string;
  Year: string;
  Actors?: string;
  Plot?: string;
  description?: string;
}

/** Película normalizada para mostrar en el modal */
export interface NormalizedMovie {
  title: string;
  poster: string | null;
  year: string | null;
  actors: string;
  description: string;
  status?: MovieStatus;
}

/** Película en resultados de búsqueda con flag de lista */
export interface SearchResultMovie extends OMDBMovie {
  isAlreadyInList?: boolean;
}

export interface ColorScheme {
  id: string;
  class: string;
  ring: string;
  border: string;
  text: string;
}
