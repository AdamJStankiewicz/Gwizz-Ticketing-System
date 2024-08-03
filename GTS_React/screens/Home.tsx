import React, { useState } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { useNavigate, useLocation } from 'react-router-dom';

const homeImg = require('@/assets/images/homeImg.svg');
const addImg = require('@/assets/images/addImg.svg');
const searchImg = require('@/assets/images/searchImg.svg');
const gwizzLogo = require('@/assets/images/glogo.png');

const HomeScreen: React.FC = () => {
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
        <Text style={styles.header}>Welcome to the Gwizz Ticketing System</Text>
        <View style={styles.descriptionContainer}>
          <Text style={styles.description}>
            Insert what you want to say in here. Write what you do and that kind of stuff. Say like, click on left=home, mid=add one, and right=search for tabs.
          </Text>
        </View>
      </View>
      <TouchableOpacity style={styles.gwizzLogoContainer} onPress={() => navigate('https://www.youtube.com/@Gwizz1027')}>
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
  descriptionContainer: {
    alignItems: 'center',
    marginTop: '5%',
  },
  description: {
    fontSize: 16,
    color: '#a9a9a9',
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

export default HomeScreen;
