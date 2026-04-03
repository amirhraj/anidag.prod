// SearchResults.jsx
import styles from './SearchPage.module.css';
import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { ClipLoader } from 'react-spinners';
import $api from '../../api/auth';

// const API = import.meta.env.VITE_CODIK_URL;
// const TOKEN = import.meta.env.VITE_CODIK_TOKEN;

export default function SearchResults() {
  const { query } = useParams();
  const [card, setCard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isExpanded, setIsExpanded] = useState({});
  const navigate = useNavigate();

  const MAX_DESCRIPTION_LENGTH = 100;

  // useEffect(() => {
  //   const fetchSearch = async () => {
  //     try {
  //       const response = await axios.get(`${API}/search?token=${TOKEN}&type=anime,anime-serial&with_material_data=true&title=${query}`);
  //       setCard(response.data);
  //       // console.log(response.data, "RESPOn")
  //     } catch (err) {
  //       setError('Ошибка при загрузке данных');
  //     } finally {
  //       setLoading(false);
  //     }
  //   };

  //   if (query) fetchSearch();
  // }, [query]);


  useEffect(() => {
  const fetchSearch = async () => {
    try {
      const response = await $api.get(`/search/anime?query=${encodeURIComponent(query)}`);
      console.log(response.data, "SEARCH")
      setCard(response.data);
    } catch (err) {
      setError('Ошибка при загрузке данных');
    } finally {
      setLoading(false);
    }
  };

  if (query) fetchSearch();
}, [query]);


  const handleCardClick = async (item) => {
    try {
      await $api.post('/animeSearch/', {
        results: [item]
      });
 
    } catch (err) {
      console.error("Ошибка при логировании поиска:", err);
    }
  
    // Перенаправляем пользователя
    const itemId = item.id || 'unknown-id';
    navigate(`/anime/${itemId}/seaarch`, { state: { data: item } });
  };

  const handleToggle = (index) => {
    setIsExpanded((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

//   const handleCardClick = (item) => {
//     const itemId = item.id || 'movie-97770';
//     navigate(`/anime/${itemId}/cardOva`, { state: { data: item } });
//   };

  if (loading) return <div className={styles.clipLoader}><ClipLoader color="#eb4d4b" size={50} /></div>;
  if (error) return <p>{error}</p>;

  const uniqueValues = Object.values(card?.results || {}).filter((item, index, self) =>
    index === self.findIndex((t) => t.title === item.title && (t.type === 'anime-serial' || t.type === 'anime'))
  );

  return (
    <div className={styles.container}>
      {uniqueValues.map((item, index) => {
        const description = item.material_data?.description || '';
        const isItemExpanded = isExpanded[index] || false;
        const truncatedDescription =
          description.length > MAX_DESCRIPTION_LENGTH && !isItemExpanded
            ? `${description.substring(0, MAX_DESCRIPTION_LENGTH)}...`
            : description;

        return (
        //   <div key={index} className={styles.card} onClick={() => handleCardClick(item)}>
        <div key={index} className={styles.card} onClick={() => handleCardClick(item)} >
             {/* <Link to={`/anime/${item.id}/cardSearch`} state={{ data: item }}  className={styles.link} > */}
                <img src={item.material_data?.poster_url || item.material_data?.anime_poster_url} alt={item.title} className={styles.poster}  onError={(e) => { e.target.src = "/anidag_default.png"; }} />
                <div className={styles.rating}>{item.material_data?.shikimori_rating}</div>
                <h3 className={styles.title}>{item.title}</h3>
                <p className={styles.description}>{truncatedDescription}</p>
                {description.length > MAX_DESCRIPTION_LENGTH && (
                <button onClick={() => handleToggle(index)} className={styles.toggleButton}>
                    {isItemExpanded ? 'Скрыть' : 'Читать больше'}
                </button>
                )}
            {/* </Link> */}
          </div>
        );
      })}
    </div>
  );
}



