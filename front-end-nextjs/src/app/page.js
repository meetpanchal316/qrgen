'use client'

export const dynamic = 'force-dynamic';

import { useState } from 'react';
import axios from 'axios';

// styles at top (important for prod build)
const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#121212',
    color: 'white',
  },
  title: {
    margin: '0',
    lineHeight: '1.15',
    fontSize: '4rem',
    textAlign: 'center',
  },
  input: {
    padding: '10px',
    borderRadius: '5px',
    border: 'none',
    marginTop: '20px',
    width: '300px',
    color: '#121212',
  },
  button: {
    padding: '10px 20px',
    marginTop: '20px',
    border: 'none',
    borderRadius: '5px',
    backgroundColor: '#0070f3',
    color: 'white',
    cursor: 'pointer',
  },
  qrCode: {
    marginTop: '20px',
    width: '256px',
    height: '256px',
    backgroundColor: 'white',
  },
};

export default function Home() {
  const [url, setUrl] = useState('');
  const [qrCodeUrl, setQrCodeUrl] = useState('');

  const BACKEND_URL = '';

const handleGenerate = async () => {
  try {
    console.log('Using BACKEND_URL =', BACKEND_URL);
    console.log('About to call backend with url =', url);

    const response = await axios.post(
      `${BACKEND_URL}/api/generate-qr/`,
      null,
      { params: { url } }
    );

    console.log('Backend response data =', response.data);
    setQrCodeUrl(response.data.qr_code_url);
  } catch (error) {
    console.error('Error generating QR Code:', error);
  }
};



  return (
    <div style={styles.container}>
      <h1 style={styles.title}>QR Code Generator</h1>

      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter URL like https://example.com"
        style={styles.input}
      />

      <button onClick={handleGenerate} style={styles.button}>
        Generate QR Code
      </button>

      {qrCodeUrl && (
        <img
          src={qrCodeUrl}
          alt="QR Code"
          style={styles.qrCode}
        />
      )}
    </div>
  );
}
