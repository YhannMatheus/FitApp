export const COLORS = {
  background: '#121212',
  surface: '#454545',
  surfaceSecondary: '#2C2C2E',
  primary: '#007AFF',
  primaryDark: '#0047AB',
  primaryLight: '#32ADE6',
  white: '#FFFFFF',
  gray: '#A1A1A1',
  black: '#000000',
  success: '#34C759',
  error: '#FF3B30',
  warning: '#FF9500',
  gradientBlue: ['#007AFF', '#0047AB'] as const, 
};

export const SIZES = {
  padding: 20,
  radiusSmall: 8,
  radiusMedium: 15,
  radiusLarge: 30,
  fontXLarge: 32,
  fontLarge: 24,
  fontMedium: 16,
  fontSmall: 14,
};

// Objeto unificado para o Styled Components e export default
const theme = {
  colors: COLORS,
  sizes: SIZES,
};

export default theme;