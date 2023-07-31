import type { AppProps } from 'next/app';
import { AuthProvider } from '../state-managemnt/app-state-context'; 

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}

export default MyApp;
