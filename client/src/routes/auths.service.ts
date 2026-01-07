import api from './api';
import { RegisterRequest, UserResponse } from '../types/auth.types';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const authService = {
  register: async (data: RegisterRequest): Promise<UserResponse> => {
    const response = await api.post<UserResponse>('/auth/register', data);
    return response.data;
  },

  login: async (email: string, password: string): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  getMe: async (): Promise<UserResponse> => {
    const response = await api.get<UserResponse>('/users/me');
    return response.data;
  }
};