import React from 'react';
import { TouchableOpacity, Text, View } from 'react-native';
import { styles } from './styles';

interface Option {
  label: string;
  value: string;
}

interface Props {
  label: string;
  options: Option[];
  selectedValue: string;
  onSelect: (value: any) => void;
}

export function SelectOption({ label, options, selectedValue, onSelect }: Props) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.optionsContainer}>
        {options.map((option) => (
          <TouchableOpacity
            key={option.value}
            style={[
              styles.option,
              selectedValue === option.value && styles.selectedOption
            ]}
            onPress={() => onSelect(option.value)}
          >
            <Text style={[
              styles.optionText,
              selectedValue === option.value && styles.selectedOptionText
            ]}>
              {option.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}