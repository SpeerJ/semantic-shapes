const config = {
  apiBaseUrl: import.meta.env.PROD 
    ? '' // todo: add production url
    : '',
}

export default config;