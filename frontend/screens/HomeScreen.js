import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';
import { deleteToken } from '../utils/auth';

export default function HomeScreen({ navigation }) {
  const handleLogout = async () => {
    await deleteToken();
    navigation.replace('Login');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📄 VakeelForms</Text>
      <Button title="📤 Upload Legal Document" onPress={() => navigation.navigate('Upload')} />
      <View style={{ marginTop: 20 }} />
      <Button title="🚪 Logout" onPress={handleLogout} color="red" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 28, fontWeight: 'bold', marginBottom: 40 }
});
 
