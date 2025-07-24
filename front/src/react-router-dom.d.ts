import * as ReactRouterDOM from 'react-router-dom';

declare global {
  interface Window {
    ReactRouterDOM: typeof ReactRouterDOM;
  }
}
