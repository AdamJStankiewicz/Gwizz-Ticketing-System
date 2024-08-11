import React from 'react';
import { View, TouchableOpacity, Image, StyleSheet } from 'react-native';

const homeImg = require('@/assets/images/homeImg.png');
const addImg = require('@/assets/images/addImg.png');
const searchImg = require('@/assets/images/searchImg.png');


interface TabsProps {
  setCurrentView: (view: string) => void;
}

const Tabs: React.FC<TabsProps> = ({ setCurrentView }) => {
  return (
    <View style={styles.tabsContainer}>
      <TouchableOpacity onPress={() => setCurrentView('home')}>
        <View style={styles.tabItem}>
          <Image source={homeImg} style={styles.tabImage} />
        </View>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => setCurrentView('create-ticket')}>
        <View style={styles.tabItem}>
          <Image source={addImg} style={styles.tabImage} />
        </View>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => setCurrentView('view-tickets')}>
        <View style={styles.tabItem}>
          <Image source={searchImg} style={styles.tabImage} />
        </View>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
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
  tabImage: {
    width: 40,
    height: 40,
  },
});

export default Tabs;






