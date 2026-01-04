import { StyleSheet } from 'react-native';
import { COLORS, SIZES } from '../../theme';

export const styles = StyleSheet.create({
  container: {
    width: '100%',
    height: 56,
    borderRadius: SIZES.radiusMedium,
    overflow: 'hidden', // Garante que o gradiente não escape das bordas
    marginVertical: 10,
  },
  gradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'row',
  },
  text: {
    color: COLORS.white,
    fontSize: SIZES.fontMedium,
    fontWeight: 'bold',
    letterSpacing: 1.2,
    textTransform: 'uppercase',
  },
});