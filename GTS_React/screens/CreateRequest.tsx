import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useNavigate, useLocation } from 'react-router-dom';

const homeImg = require('@/assets/images/homeImg.svg');
const addImg = require('@/assets/images/addImg.svg');
const searchImg = require('@/assets/images/searchImg.svg');
const gwizzLogo = require('@/assets/images/glogo.png');

const CreateRequestScreen: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const getActiveTab = () => {
    switch (location.pathname) {
      case '/':
        return 'home';
      case '/create-ticket':
        return 'create';
      case '/view-tickets':
        return 'view';
      default:
        return '';
    }
  };

  const [activeTab, setActiveTab] = useState(getActiveTab);

  const handleTabPress = (tab: string, url: string) => {
    setActiveTab(tab);
    navigate(url);
  };

  const [email, setEmail] = useState('');
  const [request, setRequest] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    console.log('Button Pressed');
    setSubmitted(true);
  };

  return (
    <View style={styles.container}>
      <View style={styles.tabsContainer}>
        <TouchableOpacity onPress={() => handleTabPress('home', '/')}>
          <View style={[styles.tabItem, activeTab === 'home' && styles.activeTab]}>
            <Image source={homeImg} style={styles.tabImage} />
          </View>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => handleTabPress('create', '/create-ticket')}>
          <View style={[styles.tabItem, activeTab === 'create' && styles.activeTab]}>
            <Image source={addImg} style={styles.tabImage} />
          </View>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => handleTabPress('view', '/view-tickets')}>
          <View style={[styles.tabItem, activeTab === 'view' && styles.activeTab]}>
            <Image source={searchImg} style={styles.tabImage} />
          </View>
        </TouchableOpacity>
      </View>
      <View style={styles.content}>
        <Text style={styles.header}>Submit Your Request</Text>
        <View style={styles.formContainer}>
          <TextInput
            style={styles.input}
            placeholder="Your Email"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />
          <TextInput
            style={[styles.input, styles.textArea]}
            placeholder="Your Request"
            value={request}
            onChangeText={setRequest}
            multiline
          />
          <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
            <Text style={styles.submitButtonText}>Submit</Text>
          </TouchableOpacity>
          {submitted && (
            <Text style={styles.submittedMessage}>Your message has been submitted</Text>
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
  tabsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    backgroundColor: '#333',
    paddingVertical: "1%",
    width: '100%',
  },
  tabItem: {
    paddingVertical: 5,
    paddingHorizontal: 10,
  },
  activeTab: {
    borderBottomWidth: 2,
    borderBottomColor: '#00b8c9',
  },
  tabImage: {
    width: 40,
    height: 40,
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
    top: '10%',
    right: '2%',
  },
  gwizzLogo: {
    width: 80,
    height: 80,
  },
});

export default CreateRequestScreen;
