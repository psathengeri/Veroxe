import React from 'react';
import { ThemeProvider, createTheme, CssBaseline, Container } from '@mui/material';
import GCPFunctionTester from './components/GCPFunctionTester';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container>
        <GCPFunctionTester />
      </Container>
    </ThemeProvider>
  );
}

export default App; 