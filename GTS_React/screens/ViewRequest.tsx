import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, Image, TouchableOpacity, TextInput } from 'react-native';
import { useNavigate, useLocation } from 'react-router-dom';

const homeImg = require('@/assets/images/homeImg.svg');
const addImg = require('@/assets/images/addImg.svg');
const searchImg = require('@/assets/images/searchImg.svg');
const youtubeLogo = require('@/assets/images/youtubeLogo.png');
const gwizzLogo = require('@/assets/images/glogo.png');

interface RequestItem {
  id: string;
  request: string;
  youtubeLink: string;
}

const ViewRequestScreen: React.FC = () => {
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

  const [searchText, setSearchText] = useState('');
  const [originalData, setOriginalData] = useState<RequestItem[]>([]);
  const [filteredData, setFilteredData] = useState<RequestItem[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:1477/tickets/');
        const textData = await response.text();
        // Assuming the text data is JSON stringified
        const data: RequestItem[] = JSON.parse(textData);
        setOriginalData(data);
        setFilteredData(data);
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
    if (url.startsWith('http')) {
      window.open(url, '_blank');
    } else {
      navigate(url);
    }
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
    top: '10%',
    right: '2%',
  },
  gwizzLogo: {
    width: 80,
    height: 80,
  },
});

export default ViewRequestScreen;
