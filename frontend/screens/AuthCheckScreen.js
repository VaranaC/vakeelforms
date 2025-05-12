import React, { useEffect } from 'react';
import { ActivityIndicator, View } from 'react-native';
import { getToken } from '../utils/auth';

export default function AuthCheckScreen({ navigation }) {
  useEffect(() => {
    const check = async () => {
      const token = await getToken();
      if (token) {
        navigation.replace('Home');
      } else {
        navigation.replace('Login');
      }
    };
    check();
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <ActivityIndicator size="large" />
    </View>
  );
}
