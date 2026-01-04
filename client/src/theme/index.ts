export const COLORS = {
  // Cores de Fundo e Estrutura
  background: '#121212',      // Preto profundo do fundo principal
  surface: '#454545',         // Cinza dos cards (conforme a imagem)
  surfaceSecondary: '#2C2C2E', // Cinza mais escuro para variações
  
  // Paleta de Azuis (Extraídas do Gradiente)
  primary: '#007AFF',         // Azul principal vibrante
  primaryDark: '#0047AB',     // Azul escuro para o final do gradiente
  primaryLight: '#32ADE6',    // Azul claro para brilhos e bordas
  
  // Estados e Feedback
  white: '#FFFFFF',           // Texto principal e títulos
  gray: '#A1A1A1',            // Texto de rótulos (Days, Kg, Level)
  black: '#000000',           // Para sombras e elementos puros

  // Cores de Ação
  success: '#34C759',        // Verde para sucesso e confirmações
  error: '#FF3B30',          // Vermelho para erros e alertas
  warning: '#FF9500',        // Laranja para avisos
  
  // Variação de Gradiente (Para usar com LinearGradient)
  gradientBlue: ['#007AFF', '#0047AB'] as const, 
};

export const SIZES = {
  // Espaçamentos
  padding: 20,
  radiusSmall: 8,
  radiusMedium: 15,
  radiusLarge: 30, // Para botões estilo "pílula" e o card de progresso

  // Tipografia
  fontXLarge: 32, // Para o "50%" ou métricas principais
  fontLarge: 24,  // Para títulos como "PROGRESS"
  fontMedium: 16, // Para labels e texto de botões
  fontSmall: 14,  // Para sub-legendas
};

export const SHADOWS = {
  default: {
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 4.65,
    elevation: 8,
  }
};