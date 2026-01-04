import React from 'react';
import { TouchableOpacity, Text, ActivityIndicator, TouchableOpacityProps } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS } from '../../theme';
import { styles } from './styles';

interface Props extends TouchableOpacityProps {
  title: string;
  isLoading?: boolean;
}

export function Button({ title, isLoading = false, ...rest }: Props) {
  return (
    <TouchableOpacity 
      style={styles.container} 
      activeOpacity={0.7} 
      disabled={isLoading}
      {...rest}
    >
      <LinearGradient
        colors={COLORS.gradientBlue}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        style={styles.gradient}
      >
        {isLoading ? (
          <ActivityIndicator color={COLORS.white} />
        ) : (
          <Text style={styles.text}>{title}</Text>
        )}
      </LinearGradient>
    </TouchableOpacity>
  );
}