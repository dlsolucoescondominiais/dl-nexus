/**
 * DL Nexus - Centralized Logger Utility
 * Ensures that console logs are suppressed in production environments
 * to prevent leaking sensitive information or cluttering the console.
 */

export const logger = {
  error: (...args: any[]) => {
    if (import.meta.env.MODE !== 'production') {
      console.error(...args);
    }
  },
  warn: (...args: any[]) => {
    if (import.meta.env.MODE !== 'production') {
      console.warn(...args);
    }
  },
  info: (...args: any[]) => {
    if (import.meta.env.MODE !== 'production') {
      console.info(...args);
    }
  },
  log: (...args: any[]) => {
    if (import.meta.env.MODE !== 'production') {
      console.log(...args);
    }
  }
};
