import React, { useState } from 'react';
import { View, Button, Text, StyleSheet, ActivityIndicator, Alert } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';
import { BASE_URL } from '../utils/config';
import { getToken } from '../utils/auth';

export default function UploadScreen({ navigation }) {
  const [fileName, setFileName] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (uri, name, type) => {
    setFileName(name);
    setLoading(true);

    try {
      const token = await getToken();
      console.log("🪪 Token being sent:", token);

      const formData = new FormData();
      formData.append('file', {
        uri,
        name,
        type,
      });

      const res = await axios.post(`${BASE_URL}/api/v1/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`,
        },
      });

      console.log("✅ Upload success:", res.data);

      navigation.navigate('Result', {
        extractedText: res.data.extracted_text,
        explanation: res.data.explanation,
      });
    } catch (err) {
      console.log('🚨 Upload error:', err?.response?.data || err.message);
      Alert.alert(
        'Upload Failed',
        err?.response?.data?.detail || err?.response?.data?.error || err.message
      );
    } finally {
      setLoading(false);
    }
  };

  const pickDocument = async () => {
    const result = await DocumentPicker.getDocumentAsync({ type: '*/*', copyToCacheDirectory: true });
    if (!result.canceled) {
      const file = result.assets[0];
      await handleUpload(file.uri, file.name, file.mimeType || 'application/octet-stream');
    }
  };

  const takePhoto = async () => {
    const permission = await ImagePicker.requestCameraPermissionsAsync();
    if (!permission.granted) {
      Alert.alert("Permission Denied", "Camera access is required.");
      return;
    }

    const result = await ImagePicker.launchCameraAsync({ quality: 1, base64: false });
    if (!result.canceled) {
      const image = result.assets[0];
      await handleUpload(image.uri, `photo.jpg`, 'image/jpeg');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Upload or Capture Legal Document</Text>
      <Button title="Select PDF or Image" onPress={pickDocument} />
      <View style={{ marginTop: 15 }} />
      <Button title="Take Photo with Camera" onPress={takePhoto} />
      {fileName && <Text style={{ marginTop: 20 }}>Selected: {fileName}</Text>}
      {loading && <ActivityIndicator size="large" style={{ marginTop: 20 }} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20 },
  heading: { fontSize: 20, textAlign: 'center', marginBottom: 30 },
});
