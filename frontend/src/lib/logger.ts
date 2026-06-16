export const logger = {
  error: (message: string, ...optionalParams: any[]) => {
    // Only log in non-production environments to prevent leaking sensitive info in UI console.
    // In the future, this can be integrated with tools like Sentry, Datadog, etc.
    if (!import.meta.env.PROD) {
      console.error(message, ...optionalParams);
    }
  },
  warn: (message: string, ...optionalParams: any[]) => {
    if (!import.meta.env.PROD) {
      console.warn(message, ...optionalParams);
    }
  },
  info: (message: string, ...optionalParams: any[]) => {
    if (!import.meta.env.PROD) {
      console.info(message, ...optionalParams);
    }
  },
  log: (message: string, ...optionalParams: any[]) => {
    if (!import.meta.env.PROD) {
      console.log(message, ...optionalParams);
    }
  }
};
