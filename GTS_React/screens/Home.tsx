import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';

const gwizzLogo = require('@/assets/images/glogo.png');

const HomeScreen: React.FC = () => {
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.header}>Gwizz Ticketing System</Text>
        <View style={styles.descriptionContainer}>
          <Text style={styles.description}>
          This platform is designed to help manage requests and tickets related to Godot, a popular open-source game engine. You can create your own ticket to request features or seek assistance. Additionally, you can view and track previous tickets to stay updated on any progress.

          Feel free to check out my YouTube channel by clicking on the icon in the top right corner and subscribe for more updates and content.

          </Text>
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
  descriptionContainer: {
    alignItems: 'center',
    marginTop: '5%',
  },
  description: {
    fontSize: 16,
    width: '70%',
    color: '#a9a9a9',
    textAlign: 'center',
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

export default HomeScreen;
