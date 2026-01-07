import React from "react";
import {  View, Text, ScrollView, KeyboardAvoidingView, Platform, Alert } from 'react-native'
import { styles } from "./styles";

import { Input, Button, SelectOption } from "@/components";
import { authService } from "@/routes/auths.service";
import { RegisterRequest } from "@/types/auth.types";
import { useTheme } from "@react-navigation/native";

export function Register() {
  const theme = useTheme();
  const [loading, setLoading] = React.useState(false);

  const [form, setForm] = React.useState<RegisterRequest>({
    name: '',
    email: '',
    password: '',
    sex: 'male',
    birth_date: '',
    height_cm: 0,
    weight_kg: 0,
    activity_level: 'sedentary'
  })

  const updateForm = (key:keyof RegisterRequest, value:any) => {
    setForm(prev => ({...prev, [key]: value}) );
  }

  const handleRegister = async () => {
    try{
        setLoading(true);
        if (!form.name || !form.email || !form.password) {
            Alert.alert('Erro', 'Por favor, preencha todos os campos obrigatórios.');
        }

        setLoading(true);

        await authService.register({
            ...form,
            height_cm: Number(form.height_cm),
            weight_kg: Number(form.weight_kg),
        });
        
        Alert.alert('Sucesso', 'Registro realizado com sucesso!');
    }catch (error : any) {
        const message = error.response?.data?.detail || "Erro ao cadastrar.";
        Alert.alert("Falha no Cadastro", message);
    }finally{
        setLoading(false);
    }
  }
    return (
        <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
            <ScrollView contentContainerStyle={styles.content}>
        
        <View style={styles.header}>
          <Text style={styles.logoText}>KILOCAL</Text>
          <Text style={styles.subtitle}>Crie sua conta para começar</Text>
        </View>

        <View style={styles.form}>
          <Input 
            label="Nome"
            placeholder="Seu nome completo"
            onChangeText={(text) => setForm({...form, name: text})}
          />

          <Input 
            label="E-mail"
            placeholder="exemplo@email.com"
            keyboardType="email-address"
            onChangeText={(text) => setForm({...form, email: text})}
          />

          <Input 
            label="Senha"
            placeholder="Mínimo 8 caracteres"
            secureTextEntry
            onChangeText={(text) => setForm({...form, password: text})}
          />

          {/* Campos Biométricos exigidos pelo seu backend */}
          <Input 
            label="Nascimento"
            placeholder="AAAA-MM-DD"
            onChangeText={(text) => setForm({...form, birth_date: text})}
          />

          <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
            <View style={{ width: '48%' }}>
              <Input 
                label="Altura (cm)"
                placeholder="175"
                keyboardType="numeric"
                onChangeText={(text) => setForm({...form, height_cm: Number(text)})}
              />
            </View>
            <View style={{ width: '48%' }}>
              <Input 
                label="Peso (kg)"
                placeholder="70.5"
                keyboardType="numeric"
                onChangeText={(text) => setForm({...form, weight_kg: Number(text)})}
              />
            </View>
          </View>

          {/* Seletores baseados nos Enums do servidor */}
          <SelectOption 
            label="Sexo"
            options={[
              { label: 'Masculino', value: 'male' },
              { label: 'Feminino', value: 'female' }
            ]}
            selectedValue={form.sex}
            onSelect={(value) => setForm({...form, sex: value})}
          />

          <Button 
            title="CADASTRAR" 
            onPress={handleRegister} 
            isLoading={loading}
          />
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>Já tem uma conta? </Text>
          <Text style={[styles.footerText, { fontWeight: 'bold' }]}>Faça Login</Text>
        </View>

      </ScrollView>
        </KeyboardAvoidingView>
    );
}

export default Register;