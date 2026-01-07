import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TouchableOpacity, 
  KeyboardAvoidingView, 
  Platform, 
  ScrollView 
} from 'react-native';
import { styles } from './styles';
import { COLORS } from '@/theme';
import { Input, Button } from '@/components';
import { useNavigation } from '@react-navigation/native';


export default function LoginScreen() {
  const navigation = useNavigation<any>();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    
    // Simulação de chamada ao seu backend
    setTimeout(() => {
      setLoading(false);
      navigation.navigate('Home');
    }, 2000);
  };

  return (
    <View style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={{ flex: 1 }}
      >
        <ScrollView 
          contentContainerStyle={styles.content}
          keyboardShouldPersistTaps="handled"
        >
          {/* Cabeçalho */}
          <View style={styles.header}>
            <Text style={styles.logoText}>
              KILO<Text style={{ color: COLORS.primary }}>CAL</Text>
            </Text>
            <Text style={styles.subtitle}>Performance em tempo real</Text>
          </View>

          {/* Formulario usando os componentes reutilizáveis */}
          <View style={styles.form}>
            <Input
              label="E-mail"
              placeholder="atleta@exemplo.com"
              keyboardType="email-address"
              autoCapitalize="none"
              value={email}
              onChangeText={setEmail}
            />

            <Input
              label="Senha"
              placeholder="••••••••"
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />

            <Button 
              title="Entrar" 
              onPress={handleLogin} 
              isLoading={loading}
            />

            <TouchableOpacity 
              style={styles.forgotPass}
              onPress={() => console.log('Esqueci a senha')}
            >
              <Text style={styles.forgotPassText}>Esqueceu a senha?</Text>
            </TouchableOpacity>
          </View>

          {/* Rodapé de Registro */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>Não tem uma conta? </Text>

            <TouchableOpacity onPress={() => navigation.navigate('register')}>
              <Text style={[styles.footerText, { color: COLORS.primary, fontWeight: 'bold' }]}>
                Cadastre-se
              </Text>
            </TouchableOpacity>
          
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}
