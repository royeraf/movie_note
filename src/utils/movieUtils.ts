import { COLORS } from '../constants';
import type { Movie, OMDBMovie, NormalizedMovie } from '../types';

/**
 * Normaliza una película (guardada o de búsqueda) al formato del modal
 */
export const normalizeMovie = (movie: Movie | OMDBMovie): NormalizedMovie => {
  const isStoredMovie = 'imdb_id' in movie;

  return {
    title: isStoredMovie ? movie.title : movie.Title,
    poster: isStoredMovie ? movie.poster_path : (movie.Poster === 'N/A' ? null : movie.Poster),
    year: isStoredMovie ? movie.release_year : movie.Year,
    actors: (isStoredMovie ? movie.actors : movie.Actors) || 'Sin información',
    description: (isStoredMovie ? movie.description : (movie.Plot || movie.description)) || 'No hay descripción disponible para esta película.',
    status: isStoredMovie ? movie.status : undefined,
  };
};

export const getPosterUrl = (path: string | null) => {
  if (!path || path === 'N/A') return 'https://via.placeholder.com/500x750?text=Sin+Poster';
  return path;
};

export const getColorClass = (colorId?: string | null) => {
  const color = COLORS.find(c => c.id === colorId);
  return color ? `ring-2 ${color.ring} border-transparent` : 'border-black/5 dark:border-white/10';
};

export const extractColor = (url: string): Promise<string> => {
  return new Promise((resolve) => {
    if (!url || url === 'N/A') return resolve('');
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.src = url;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = 1;
      canvas.height = 1;
      if (ctx) {
        ctx.drawImage(img, 0, 0, 1, 1);
        try {
          const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data;
          resolve(`rgb(${r}, ${g}, ${b})`);
        } catch (e) {
          // CORS probably
          resolve('');
        }
      } else {
        resolve('');
      }
    };
    img.onerror = () => resolve('');
  });
};
