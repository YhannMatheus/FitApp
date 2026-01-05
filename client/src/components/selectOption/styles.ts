import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: { width: '100%', marginBottom: 20 },
  label: { fontSize: 14, fontWeight: 'bold', color: '#333', marginBottom: 10 },
  optionsContainer: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  option: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#DDD',
    backgroundColor: '#FFF'
  },
  selectedOption: { backgroundColor: '#4A90E2', borderColor: '#4A90E2' },
  optionText: { color: '#666' },
  selectedOptionText: { color: '#FFF', fontWeight: 'bold' }
});