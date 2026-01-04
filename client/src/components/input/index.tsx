import React, { useState } from 'react';
import { View, Text, TextInput, TextInputProps } from 'react-native';
import { COLORS } from '../../theme';
import { styles } from './style';

interface Props extends TextInputProps {
  label: string;
}

export function Input({ label, ...rest }: Props) {
  const [isFocused, setIsFocused] = useState(false);

  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        style={[
          styles.inputArea,
          isFocused && styles.inputFocused
        ]}
        placeholderTextColor={COLORS.gray}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        {...rest}
      />
    </View>
  );
}