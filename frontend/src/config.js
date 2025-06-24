const config = {
  apiBaseUrl: import.meta.env.PROD 
    ? 'https://semantic-shapes-api-production.up.railway.app'
    : '',
}

export default config;