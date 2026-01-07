import React from 'react';
import { NavigationIndependentTree, NavigationContainer } from '@react-navigation/native';
import { ThemeProvider } from 'styled-components/native';

import theme from '../theme'; 
import { AuthRoutes } from '../routes/auth.routes';

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      {/* Para usar o React Navigation manual dentro do Expo Router, 
        é obrigatório envolver tudo no NavigationIndependentTree 
      */}
      <NavigationIndependentTree>
        <NavigationContainer>
          <AuthRoutes />
        </NavigationContainer>
      </NavigationIndependentTree>
    </ThemeProvider>
  );
}