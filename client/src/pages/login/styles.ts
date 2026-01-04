import { StyleSheet } from 'react-native';
import { COLORS, SIZES } from '../../theme';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    // Usamos flexGrow em ScrollViews para garantir que o conteúdo preencha a tela
    flexGrow: 1, 
    paddingHorizontal: SIZES.padding,
    justifyContent: 'center',
    paddingBottom: 30, // Espaço extra para não colar no fim da tela
  },
  header: {
    marginBottom: 50,
    alignItems: 'center',
  },
  logoText: {
    fontSize: 40,
    fontWeight: '900',
    color: COLORS.white,
    letterSpacing: 2,
  },
  subtitle: {
    color: COLORS.gray,
    fontSize: SIZES.fontSmall,
    marginTop: 5,
  },
  form: {
    width: '100%',
  },
  forgotPass: {
    marginTop: 20,
    alignItems: 'center',
  },
  forgotPassText: {
    color: COLORS.gray,
    fontSize: SIZES.fontSmall,
    textDecorationLine: 'underline',
  },
  
  // --- AS PROPRIEDADES QUE ESTAVAM FALTANDO ---
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 40,
  },
  footerText: {
    color: COLORS.gray,
    fontSize: SIZES.fontSmall,
  },
});