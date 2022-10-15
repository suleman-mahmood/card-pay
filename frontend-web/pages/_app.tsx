import '../styles/globals.css';
import React from 'react';
import { wrapper } from '../store/store';
import type { AppProps } from 'next/app';

function MyApp({ Component, pageProps }: AppProps) {
	return <Component {...pageProps} />;
}

export default wrapper.withRedux(MyApp);
