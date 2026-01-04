import { StyleSheet } from 'react-native';
import { COLORS, SIZES } from '../../theme';

export const styles = StyleSheet.create({
  container: {
    width: '100%',
    marginBottom: 20,
  },
  label: {
    color: COLORS.primary,
    fontSize: 12,
    fontWeight: 'bold',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  inputArea: {
    width: '100%',
    height: 56,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: SIZES.radiusSmall,
    paddingHorizontal: 16,
    borderWidth: 1,
    borderColor: '#333',
    color: COLORS.white,
    fontSize: SIZES.fontMedium,
  },
  inputFocused: {
    borderColor: COLORS.primary, // Brilho azul ao focar
  }
});