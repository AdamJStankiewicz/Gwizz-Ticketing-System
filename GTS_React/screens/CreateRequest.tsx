import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Image } from 'react-native';

const gwizzLogo = require('@/assets/images/glogo.png');

const CreateRequestScreen: React.FC = () => {
  const [email, setEmail] = useState('');
  const [request, setRequest] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async () => {
    console.log('Button Pressed');

    const data = { email, desc: request };
    const url = 'http://10.0.0.184:1477/upload'; // Replace with your actual IP address

    console.log('Request URL:', url);
    console.log('Request Body:', JSON.stringify(data));

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      console.log('Response Status:', response.status);
      const responseText = await response.text();
      console.log('Response Text:', responseText);

      let result;
      try {
        result = JSON.parse(responseText);
      } catch (e) {
        console.error('Failed to parse JSON:', e);
        setMessage('Failed to parse server response.');
        setSubmitted(true);
        return;
      }

      if (result.status === '0') {
        setMessage(`Ticket submitted! Here is your Ticket ID: ${result.id}`);
      } else if (result.status === '1') {
        setMessage(`Email already has an open ticket. Ticket ID: ${result.id}`);
      } else {
        setMessage('Something went wrong. Please try again.');
      }

      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting ticket:', error);
      setMessage('An error occurred while submitting your request. Please try again.');
      setSubmitted(true);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.header}>Submit Your Request</Text>
        <View style={styles.formContainer}>
          <TextInput
            style={styles.input}
            placeholder="Your Email"
            value={email}
            placeholderTextColor="#fff" 
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />
          <TextInput
            style={[styles.input, styles.textArea]}
            placeholder="Your Request"
            value={request}
            placeholderTextColor="#fff" 
            onChangeText={setRequest}
            multiline
          />
          <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
            <Text style={styles.submitButtonText}>Submit</Text>
          </TouchableOpacity>
          {submitted && (
            <Text style={styles.submittedMessage}>{message}</Text>
          )}
        </View>
      </View>
      <TouchableOpacity style={styles.gwizzLogoContainer} onPress={() => window.open('https://www.youtube.com/@Gwizz1027', '_blank')}>
        <Image source={gwizzLogo} style={styles.gwizzLogo} />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#282828',
  },
  content: {
    flex: 1,
    marginTop: '10%',
    width: '90%',
    alignSelf: 'center',
  },
  header: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#fff',
    textAlign: 'center',
  },
  formContainer: {
    marginTop: 20,
    width: '100%',
    alignItems: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#00b8c9',
    borderRadius: 5,
    padding: 10,
    marginBottom: 20,
    width: '70%',
    color: '#fff',
  },
  textArea: {
    height: 100,
  },
  submitButton: {
    backgroundColor: '#00b8c9',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 5,
    alignItems: 'center',
    marginTop: 20,
  },
  submitButtonText: {
    color: '#282828',
    fontSize: 18,
    fontWeight: 'bold',
  },
  submittedMessage: {
    color: '#fff',
    marginTop: 20,
    fontSize: 16,
  },
  gwizzLogoContainer: {
    position: 'absolute',
    top: '1%',
    right: '1%',
  },
  gwizzLogo: {
    width: 60,
    height: 60,
  },
});

export default CreateRequestScreen;


//when using the web: 127.0.0.1:1477
//when using android: 10.0.0.184:1477
