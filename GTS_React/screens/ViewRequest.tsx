import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, Image, TouchableOpacity, TextInput } from 'react-native';

const youtubeLogo = require('@/assets/images/youtubeLogo.png');
const gwizzLogo = require('@/assets/images/glogo.png');

interface RequestItem {
  id: string;
  request: string;
  youtubeLink: string;
}

const defaultYouTubeLink = 'https://www.youtube.com/@Gwizz1027';

const ViewRequestScreen: React.FC = () => {
  const [searchText, setSearchText] = useState('');
  const [originalData, setOriginalData] = useState<RequestItem[]>([]);
  const [filteredData, setFilteredData] = useState<RequestItem[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://10.0.0.184:1477/tickets/');
        const textData = await response.text();
        const dataObject = JSON.parse(textData);

        const dataArray: RequestItem[] = Object.keys(dataObject).map(key => ({
          id: key,
          request: dataObject[key].desc,
          youtubeLink: dataObject[key].url || defaultYouTubeLink,
        }));

        setOriginalData(dataArray);
        setFilteredData(dataArray);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleSearch = (text: string) => {
    setSearchText(text);
    if (text) {
      const filtered = originalData.filter(item =>
        item.request.toLowerCase().includes(text.toLowerCase())
      );
      setFilteredData(filtered);
    } else {
      setFilteredData(originalData);
    }
  };

  const handleNavigation = (url: string) => {
    const finalUrl = url.startsWith('http') ? url : defaultYouTubeLink;
    window.open(finalUrl, '_blank');
  };

  const renderItem = ({ item }: { item: RequestItem }) => (
    <View style={styles.itemContainer}>
      <Text style={styles.request}>{item.request}</Text>
      <TouchableOpacity onPress={() => handleNavigation(item.youtubeLink)}>
        <Image source={youtubeLogo} style={styles.logo} />
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.header}>Request Previews</Text>
        <Text style={styles.subHeader}>In order to see the completed request, click on the YouTube icon.</Text>
        <TextInput
          style={styles.searchBar}
          placeholder="Search requests..."
          placeholderTextColor="#fff"
          value={searchText}
          onChangeText={handleSearch}
        />
        <FlatList
          data={filteredData}
          renderItem={renderItem}
          keyExtractor={item => item.id}
          contentContainerStyle={styles.listContainer}
        />
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
  subHeader: {
    fontSize: 16,
    color: '#a9a9a9',
    textAlign: 'center',
    marginBottom: 20,
  },
  searchBar: {
    height: 40,
    borderColor: '#00b8c9',
    borderWidth: 1,
    borderRadius: 8,
    paddingLeft: 10,
    marginBottom: 20,
    color: '#fff',
  },
  listContainer: {
    width: '100%',
  },
  itemContainer: {
    padding: 15,
    marginVertical: 10,
    backgroundColor: '#282828',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#00b8c9',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    flexDirection: 'row',
    alignItems: 'center',
  },
  request: {
    fontSize: 16,
    color: '#fff',
    flex: 1,
  },
  logo: {
    width: 24,
    height: 24,
    marginLeft: 10,
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

export default ViewRequestScreen;


//when using the web: 127.0.0.1:1477
//when using android: 10.0.0.184:1477
