import React, { useState } from 'react';
import { View, Text, ScrollView, Button, StyleSheet, Switch } from 'react-native';

export default function ResultScreen({ route, navigation }) {
  const { extractedText, explanation } = route.params;
  const [showText, setShowText] = useState(false);

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.heading}>Legal Explanation:</Text>
      <Text style={styles.body}>
        {typeof explanation === 'string' ? explanation : JSON.stringify(explanation, null, 2)}
      </Text>

      <View style={styles.toggleContainer}>
        <Text>Show Extracted Text</Text>
        <Switch value={showText} onValueChange={setShowText} />
      </View>

      {showText && (
        <>
          <Text style={styles.heading}>📄Extracted Text:</Text>
          <Text style={styles.body}>{extractedText || 'N/A'}</Text>
        </>
      )}

      <View style={{ marginTop: 20 }}>
        <Button title="BACK TO HOME" onPress={() => navigation.replace('Home')} />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  heading: { fontSize: 18, fontWeight: 'bold', marginTop: 20 },
  body: { fontSize: 16, marginTop: 10, lineHeight: 22 },
  toggleContainer: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 20 }
});
