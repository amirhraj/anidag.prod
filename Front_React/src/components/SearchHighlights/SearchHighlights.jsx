import React, { useRef, useState, useEffect} from 'react';
import styles from './SearchHighlights.module.css';
import $api from '../../api/auth';
import { Link } from 'react-router-dom';
import { ClipLoader } from 'react-spinners';

const SearchHighlights = () => {
  const scrollRef = useRef();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [skip, setSkip] = useState(0);
  const [limit] = useState(16);
  const [hasMore, setHasMore] = useState(true);
  const [isFetchingMore, setIsFetchingMore] = useState(false);




  const fetchHighlights = async (newSkip = skip) => {
  try {


    const response = await $api.get('/animeSearch/', {
      params: { skip: newSkip, limit },
    });

    const newItems = response.data;
    if (newItems.length < limit) {
      setHasMore(false); // больше данных нет
    }

    setItems((prev) => [...prev, ...newItems]);
    setSkip(newSkip + limit);
  } catch (error) {
    console.error('Ошибка при загрузке популярных тайтлов:', error);
  } finally {
    setLoading(false);
    setIsFetchingMore(false);
  }
};

useEffect(() => {
  fetchHighlights(0);
}, []);

  if (loading) return <div className={styles.clipLoader}><ClipLoader color="#eb4d4b" size={50} /></div>
  if (!items.length) return <div></div>;

  // const scroll = (direction) => {
  //   if (!scrollRef.current) return;

  //   const card = scrollRef.current.querySelector(`.${styles.card}`);
  //   const cardWidth = card?.offsetWidth || 120;
  //   const gap = 20;

  //   // Детекция по ширине экрана
  //   const cardsToScroll = window.innerWidth < 768 ? 1 : 5;
  //   const scrollAmount = (cardWidth + gap) * cardsToScroll;

  //   scrollRef.current.scrollBy({
  //     left: direction === "left" ? -scrollAmount : scrollAmount,
  //     behavior: "smooth",
  //   });
  // };


  
const scroll = (direction) => {
  if (!scrollRef.current) return;

  const container = scrollRef.current;
  const card = container.querySelector(`.${styles.card}`);
  const cardWidth = card?.offsetWidth || 120;
  const gap = 20;
  const cardsToScroll = window.innerWidth < 900 ? 1 : 5;
  const scrollAmount = (cardWidth + gap) * cardsToScroll;

  // 👇 Проверка ДО скролла, если мы уже почти у конца
  const nearEnd = container.scrollLeft + container.clientWidth >= container.scrollWidth - scrollAmount;

  if (direction === "right") {
    container.scrollBy({
      left: scrollAmount,
      behavior: "smooth",
    });

    // если мы почти у конца — сразу загружаем новую порцию
    if (nearEnd && hasMore && !isFetchingMore) {
      setIsFetchingMore(true);
      fetchHighlights();
    }
  } else {
    container.scrollBy({
      left: -scrollAmount,
      behavior: "smooth",
    });
  }
};

  return (
    <div className={styles.carouselWrapper}>
      <h2 className={styles.title}>Что ищут прямо сейчас</h2>
      <div className={styles.carousel}>
        <button className={styles.arrowLeft} onClick={() => scroll('left')}>←</button>
        <div className={styles.track} ref={scrollRef}>
          {items.map((item, idx) => (
            <Link  to={`/card/${item.id}/seaarch`} target="_blank">
                    <div key={idx} className={styles.card}>
                    <img src={item.poster_url || item.anime_poster_url} alt={item.title} onError={(e) => { e.target.src = "/anidag_default.png"; }}/>
                    <p>{item.title}</p>
                    </div>
            </Link>
          ))}
        </div>
        <button className={styles.arrowRight} onClick={() => scroll('right')}>→</button>
      </div>
    </div>
  );
};

export default SearchHighlights;
