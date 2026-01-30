export interface Movie {
  id?: number;
  imdb_id: string;
  title: string;
  poster_path: string | null;
  release_year: string | null;
  status: 'to-watch' | 'watched';
  color?: string;
  actors?: string;
  description?: string;
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

export interface ColorScheme {
  id: string;
  class: string;
  ring: string;
  border: string;
  text: string;
}
