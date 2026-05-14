let MEDIA_BASE_URL;

if (import.meta.env.MODE === 'development') {
  MEDIA_BASE_URL = '/api/media/';
} else if (import.meta.env.MODE === 'production') {
  MEDIA_BASE_URL = '/media/';
}

export { MEDIA_BASE_URL }
;