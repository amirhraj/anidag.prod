import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; // используем :type в URL
import { ClipLoader } from 'react-spinners';
import $api from '../../api/auth';
import styles from './AnimeCard.module.css';
import { Link } from 'react-router-dom';
import { useRef } from 'react';

const API_MAP = {
  ova: '/animeOvaAll',
  movie: '/animeFilms',
  tv: '/animesMainTitlesTV',
  top: '/animeTop',
  ongoing: '/animes',
  anons: '/animesAnons',
  genre: '/animeGenres'
};

export default function AnimeListPage() {
  const { type, value } = useParams(); // например: /category/ova → type = "ova"
  const [series, setSeries] = useState([]);
  const [listLoading, setListLoading] = useState(false);   // загрузка карточек
  const [buttonLoading, setButtonLoading] = useState(false); // загрузка кнопки
  const [skip, setSkip] = useState(0);
  const [limit] = useState(40);
  const [error, setError] = useState(null);
  const [isExpanded, setIsExpanded] = useState({});
  const loaderRef = useRef(null);

 useEffect(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting && !buttonLoading) {
        fetchData(skip, true);
      }
    },
    { threshold: 1 }
  );

  if (loaderRef.current) {
    observer.observe(loaderRef.current);
  }

  return () => observer.disconnect();
}, [skip, buttonLoading]);

    const handleToggle = (index) => {
    setIsExpanded((prev) => ({
        ...prev,
        [index]: !prev[index],
    }));
    };

  const MAX_DESCRIPTION_LENGTH = 100;

  useEffect(() => {
    document.title = type?.toUpperCase() || 'Аниме';
    setSeries([]);
    setSkip(0);
    fetchData(0); // При смене типа сбрасываем список
  }, [type]);

  const fetchData = async (currentSkip, isLoadMore = false) => {
    const endpoint = API_MAP[type];
    if (!endpoint) return setError(`Неизвестный тип: ${type}`);

    try {
        if (isLoadMore) {
          setButtonLoading(true);
        } else {
          setListLoading(true);
        }

            
      if (type === 'genre') {
        const res = await $api.get(
          `${endpoint}/${encodeURIComponent(value)}?skip=${currentSkip}&limit=${limit}`
        );

        setSeries((prev) => [...prev, ...res.data]);
        setSkip((prev) => prev + limit);
        return
      }
  
      const res = await $api.get(`${endpoint}?skip=${currentSkip}&limit=${limit}`);
      setSeries((prev) => [...prev, ...res.data]);
      setSkip((prev) => prev + limit);

      // console.log('API response:', res.data);
    } catch (err) {
      setError('Ошибка загрузки');
    } finally {
          setListLoading(false);
          setButtonLoading(false);
    }
  };

  return (
 
        <div>
    {listLoading && series.length === 0 ? (
      <div className={styles.cardsLoader}>
        <ClipLoader color="#eb4d4b" size={50} />
      </div>
    ) : (  <div>

     <div className={styles.container}>
       {series.map((item, index) => {
         const description = item.description || ''; // Описание
         const isItemExpanded = isExpanded[index] || false;
         const truncatedDescription =
           description.length > MAX_DESCRIPTION_LENGTH && !isItemExpanded
             ? `${description.substring(0, MAX_DESCRIPTION_LENGTH)}...`
             : description;

             const makeSlug = (text = "") => {
                  return text
                    .toLowerCase()
                    .trim()
                    .replace(/[^\p{L}\p{N}\s-]/gu, "")
                    .replace(/\s+/g, "-")
                    .replace(/-+/g, "-");
                };

                const titleForSlug =
                  item.title_orig ??
                  "anime";
                const seoPart = `${makeSlug(titleForSlug)}-${item.id}`;

         return (
           <div key={index} className={styles.card}>
             <Link to={`/anime/${seoPart}/${type === 'genre' ? 'ongoing' : type}`}  className={styles.link} target="_blank">
            
                    <img src={item.poster_url ?? item.poster.original} alt={item.title} className={styles.poster} onError={(e) => { e.target.src = "/anidag_default.png"; }} />
                    <div className={styles.rating}>
                                {item.material_data?.shikimori_rating !== undefined
                                    ? item.material_data.shikimori_rating
                                    : 0}
                    </div>

                     <h3 className={styles.title}>{item.title ?? item.russian_name}</h3>
                     <p className={styles.description}>{truncatedDescription}</p>
                     <p className={styles.aired_at}>
                        {/* {console.log(item)} */}
                           Дата выхода: {item.created_at ? item.created_at.split(' ')[0] : '—'}
                      </p>
                     {description.length > MAX_DESCRIPTION_LENGTH && (
                       <button onClick={() => handleToggle(index)} className={styles.toggleButton}>
                         {isItemExpanded ? 'Скрыть' : 'Читать больше'}
                       </button>
                     )}
             </Link>

           </div>
         );
       })}
     </div>
     <div className={styles.buttonContainer}>
                       {/* {buttonLoading ? (
                           <div className={styles.loadClip}>
                               <ClipLoader   color="#eb4d4b" size={50} />
                           </div>
                       ) : (
                       <button               onClick={() => fetchData(skip, true)}
                         className={styles.loadMoreButton}>
                           Показать больше
                       </button>
                       )} */}

                       
            <div ref={loaderRef} style={{ height: '50px' }}></div>
                    {buttonLoading && (
            <div className={styles.loadClip}>
              <ClipLoader color="#eb4d4b" size={40} />
            </div>)}
       </div>
   </div>)}
    </div>
  
  );
}
