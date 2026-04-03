
import styles from "./CardPages.module.css";
import React, { useState  , useEffect , useRef} from 'react';
import $api from '../../api/auth';
import Comments from "../../components/Comments/Comments";
import { useParams, useLocation  , useNavigate} from 'react-router-dom';
import { formatDate } from '../utils/formatDate';
import { ClipLoader } from 'react-spinners';
import { jwtDecode } from "jwt-decode";
import BookmarkIcon from "../Icons/BookMark";
import TelegramIcons from '../Icons/TelegramIcon.jsx'
import { Helmet } from "react-helmet-async";

import ErrorBoundaryImage from '../ErrorBoundaryImage /ErrorBoundaryImage';




const API_MAP = {
    movie: '/animeFilm',
    card: '/animesTitleMine',
    tv:'/animesTitleMine',
    ova: '/animeOvaAll',
    top: '/animeTop',
    animeongoing: '/animes',
    ongoing : '/animes',
    anons: '/animeAnons',
    search: '/animeSearch'
  };


const CardPages = () => {

    const location = useLocation();
    const [message, setMessage] = useState('');
    const [likeCount, setLikeCount] = useState(0);
    const [disLikeCount, setDisLikeCount] = useState(0);
    const [viewCount, setViewCount] = useState(0);
    const [card, setCard] = useState(location.state?.data || null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showToast, setShowToast] = useState(false);
    const [toastMessage, setToastMessage] = useState("");
    const [isAdded, setIsAdded] = useState(false);
    const [user, setUser] = useState(null);
    const { ids, cardType } = useParams(); 
    const id = ids?.match(/(serial|movie|tv|ova)-\d+$/)?.[0] || ids;
    const navigate = useNavigate();
    const currentTimeRef = useRef(0);
    const durationRef = useRef(0);
    const episodeRef = useRef(null);
    const lastProgressRef = useRef(0);
    let lenArrayRelese = 0


    const [isRussian, setIsRussian] = useState(false);
    const [geoLoading, setGeoLoading] = useState(true);
    const [activeTab, setActiveTab] = useState("first");

    const [cardAl, setCardAl] = useState(null)

    useEffect(() => {
      const fetchGeo = async () => {
        try {
          const res = await $api.get("/geo-info");
          if (res.data.country === "RU") setIsRussian(true);
        } catch (err) {
          console.error("Ошибка при запросе гео:", err);
        } finally {
          setGeoLoading(false);
        }
      };
      fetchGeo();
    }, []);


    useEffect(() => {
      const token = localStorage.getItem("access_token");
      if (!token) return;

      try {
        const decoded = jwtDecode(token);
        const userId = decoded?.sub || null;
        setUser(userId);
      } catch (err) {
        console.error("Ошибка при декодировании токена:", err);
      }
  }, []);
  

    useEffect(() => {
      const fetchStatus = async () => {
        try {

          const token = localStorage.getItem("access_token");
   

          if (!token) {
            // Пользователь не авторизован — ничего не делаем
            return;
          }
          const res = await $api.get(`/watch-later/status/${id}`);
       
          setIsAdded(res.data.is_added);
        } catch (err) {
          console.error("Ошибка при загрузке watch-later:", err);
        }
      };
      if (id) {
        fetchStatus();
      }
    
    }, [id]);

    useEffect(() => {
      if (showToast) {
        const timer = setTimeout(() => setShowToast(false), 3000);
        return () => clearTimeout(timer);
      }
    }, [showToast]);


    
    const handleToggle = async () => {
      try {
        const token = localStorage.getItem("access_token");

        if (!token) {
          setToastMessage("Необходимо войти в аккаунт");
          setShowToast(true);
          return;
        }


        const api = API_MAP[cardType];
        if (!id || !cardType || !api) {
          console.warn("Недостаточно данных для запроса");
          return;
        }
    
        if (isAdded) {
          const res = await $api.delete(`/watch-later/remove/${id}`);
          if (res.data?.status === "removed") {
            setIsAdded(false);
            setToastMessage("Удалено из «Смотреть позже»");
          }
        } else {
          const res = await $api.post(`/watch-later/add/${id}`,
            { type: cardType, api },
            { headers: { "Content-Type": "application/json" } }
          );
          if (res.data?.status === "added") {
            setIsAdded(true);
            setToastMessage("Добавлено в «Смотреть позже»");
          }
        }

        setShowToast(true);
      } catch (err) {
        console.error("Ошибка при обновлении watch-later:", err);
      }
    };


    const scrollToPlayer = () => {
        const player = document.getElementById('videoPlayer');
        if (player) {
            player.scrollIntoView({ behavior: 'smooth' });
        }
       };


       useEffect(() => {
        const fetchCard = async () => {
          try {
            setLoading(true);

            if (card) {
              setLoading(false);
              return;
            }

            const endpoint = API_MAP[cardType];
           
            if (!endpoint || endpoint === '/animeAnons') {
              setError('Неверный тип карточки');
              navigate('/');
              return;
            }
        
            const response = await $api.get(`${endpoint}/${id}`);
            
            setCard(response.data.card);
            setCardAl(response.data.al_ongoing)
          } catch (err) {
            setError('Тайтл не найден');
          } finally {
            setLoading(false);
          }
        };
      
        if (id && cardType) {
          fetchCard();
        }
      }, [id, cardType]);


       const handleLike = async (artworkId) => {
        try {
        
          const response = await $api.post(`/like/${id}` ,{
            title: card.title_orig,
            user_id: user
          });
          setMessage(response.data.message);
          setLikeCount(response.data.like_count);
          setDisLikeCount(response.data.dislike_count)
  
        } catch (error) {
          console.error('Error:', error);
          setMessage('Something went wrong.');
        }
      };



      const handleDislike = async (artworkId) => {
        try {
          const response = await $api.post(`/dislike/${id}`, {
            title: card.title_orig,
            user_id: user
          });
          setMessage(response.data.message);
          setDisLikeCount(response.data.dislike_count)
          setLikeCount(response.data.like_count)
    
        } catch (error) {
          console.error('Error:', error);
          setMessage('Something went wrong.');
        }
      };


      useEffect(() => {
        const fetchStatus = async () => {
            try {
                if (!card?.title_orig) return;

                const response = await $api.post(`/status/${id}`, {
                    title: card.title_orig,
                    user_id: user
                });
           
                setLikeCount(response.data.like_count);
                setDisLikeCount(response.data.dislike_count);
                setViewCount(response.data.view_count);
            
                const viewResponse = await $api.post(`/view/${id}`, {
                    title: card.title_orig,
                    id: id,
                    user_id: user
                });
                setViewCount(viewResponse.data.view_count);
          
            } catch (error) {
                console.error('Error:', error);
            }
        };

        fetchStatus();
    }, [!card?.title_orig]);




    useEffect(() => {
      const startTime = Date.now();
    
      const handleUnload = () => {
        const endTime = Date.now();
        const timeSpent = Math.floor((endTime - startTime) / 1000);
    
        const token = localStorage.getItem("access_token");
        let userId = null;
    
        if (token) {
          try {
            const decoded = jwtDecode(token);
            userId = decoded?.sub || null;
          
          } catch {}
        }
    
        const payload = JSON.stringify({
          anime_id: id,
          user_id: userId,
          referer: window.location.pathname,
          time_spent: timeSpent,
          device_info: navigator.userAgent
        });
    
        const blob = new Blob([payload], { type: 'application/json' });
        navigator.sendBeacon("https://anidag.ru/api/track-time", blob);
      };
    
      window.addEventListener("unload", handleUnload);
    
      return () => {
        window.removeEventListener("unload", handleUnload);
      };
    }, [id]);
    

    useEffect(() => {
      const handleMessage = (event) => {
        const { key, value } = event.data || {};
    

        if (key === 'kodik_player_current_episode') {
          episodeRef.current = value.episode || null;
        }

        if (key === 'kodik_player_time_update') {
          currentTimeRef.current = value;
        }

        if (key === 'kodik_player_duration_update') {
          durationRef.current = value;
        }
      };

      window.addEventListener('message', handleMessage);
      return () => window.removeEventListener('message', handleMessage);
    }, []);




useEffect(() => {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  let userId = null;

  try {
    const decoded = jwtDecode(token);
    userId = decoded?.sub || null;
    setUser(userId)
  } catch (e) {}
  const apiPath = API_MAP[cardType] || null;

  const interval = setInterval(() => {
    const currentTime = currentTimeRef.current;
    const duration = durationRef.current;
    if (!duration || !currentTime) return;

    const progress = Math.floor((currentTime / duration) * 100);
    if (progress - lastProgressRef.current < 1) return;

    lastProgressRef.current = progress;

    // console.log(id, user, "ID === USER")

    $api.post("/watch-history", {
      user_id: user,
      anime_id: id,
      title: card?.title,
      current_time: currentTime,
      episode: episodeRef.current || 1,
      type: cardType,
      api: apiPath,
      duration,
      progress,
      updated_at: new Date().toISOString()
    }).catch(err => console.error("Не удалось сохранить прогресс:", err));
  }, 5000);

  return () => clearInterval(interval);
}, [id, card]);




    
    if (geoLoading) {
        return <div className={styles.clipLoader}><ClipLoader color="#eb4d4b" size={50} /></div>; // ждем пока определится страна
      }
      if (isRussian && card?.country === "RU") {
      return <h1 className={styles.clipLoader}>Тайтл в вашей стране не доступен</h1>;
    }

    if (loading) return <div className={styles.clipLoader}><ClipLoader color="#eb4d4b" size={50} /></div>;
    if (error) return <h1 className={styles.clipLoader}>{error}</h1>;
    // if (isRussian && card.country === 'RU') return <h1 className={styles.clipLoader}>Тайтл в вашей стране не доступен</h1>
    if (!card) return null; // или показать сообщение

    
return (
<> 
  {card ? (
   <div >
    <Helmet>
      <title>{card?.title}</title>
      <meta name="description" content={card?.description?.slice(0, 150)} />
    </Helmet>

                    <div key={card.id} className={styles.card_module}>
                        <div className={styles.card_wrapper_module}>
                                        <div className={styles.card_image_wrapper}>
                                     
                                                 <img className={styles.card_img} 
                                                 src={`${card.poster_url === undefined ? card.material_data.poster_url : card.poster_url }`} 
                                                 alt={card.material_data.title} 
                                                 onError={(e) => { e.target.src = "/anidag_default.png"; }}
                                                 />
                                                  {/* <ErrorBoundaryImage  
                                                  className={cssong.card_ongoing_img} 
                                                  src={item.poster_url} 
                                                  defaultSrc={url} 
                                                  alt={item.material_data.anime_title}/> */}
                                                <button className={styles.watch_button} onClick={scrollToPlayer}>Смотреть онлайн </button>
                                        </div>
                                        <div className={styles.card_content}>
                                                <div className={styles.card_title_container}>
                                                    <h1 className={styles.card_title}>{card.title}</h1>
                                                    <h3 className={styles.card_title_orig}>{card.title_orig}</h3>
                                                </div>
                                                <p className={styles.pRaiting}><span className={styles.span}>Рэйтинг:</span> <span className={styles.spanRaiting}>{card.material_data.kinopoisk_rating || card.material_data.shikimori_rating}</span> </p>
                                                <p><span className={styles.span}>Эпизоды:</span>  {card.last_episode}</p>
                                                <p><span className={styles.span}>Жанр:</span>  {card.material_data.anime_genres ? 
                                                        card.material_data.anime_genres.join(', ').toLowerCase() :
                                                        (card.material_data.anime_genres ? card.material_data.anime_genres.join(', ').toLowerCase(): 'Жанр не указаны')
                                                    }</p>
                                                <p className={styles.pStatus}><span className={styles.span}>
                                                    Статус:</span>
                                                    <span className={styles.status}>{card.material_data.anime_status === "released"? "Вышел" : card.material_data.anime_status || 
                                                    card.material_data.anime_status === "ongoing" ? "Онгоинг" : card.material_data.anime_status}
                                                    </span> </p>
                                                <p><span className={styles.span}>Длительность серии:</span> {card.material_data.duration}</p>
                                                <p><span className={styles.span}>Дата выхода:</span> {formatDate(card.created_at)}</p>
                                                <p> <span className={styles.span}>Рейтинг MPAA:</span> {card.material_data.rating_mpaa || '?'}</p>
                                                <p> <span className={styles.span}>Ограничения по возрасту:</span> {card.material_data.minimal_age ? `${card.material_data.minimal_age} +` : '?'}</p>
                                                <p> <span className={styles.span}>Страна:</span> {card.countries || 'Неизвестно'}</p>
                                        </div>       
                        </div>
                        <p className={styles.p}>{card.description}</p>  
                          
                        
                            <div className={`${styles.middle_content} ${lenArrayRelese !== 0 ?  '':  styles.middle_contenthidden}`}>
                                    <h3>Смотреть аниме {card.material_data.title}</h3>
                            </div>
                            <a href="https://t.me/anidagHD" target="_blank" rel="noopener noreferrer">
                            <div className={styles.container_tg}>
                               <p>Подписывайтесь на телеграм</p>
                                
                                      <TelegramIcons className={styles.icon_telegram}/>
                               
                            </div>
                             </a>

                            <div id='videoPlayer' className={styles.player_block}> 
                                    {/* <Player  hslink={hrlUrl}  /> */}
                                    {/*<div className={styles.player_player}>
                                       <iframe className={styles.player_block_iframe} src={card.link}  width="100%" height="100%" frameBorder="0" allowFullScreen allow="autoplay *; fullscreen *"></iframe>
                                    </div>*/}
                                        <div>
                                            {/* Табы-кнопки */}
                                            <div className={styles.tabButtons}>
                                              <button
                                                className={activeTab === "first" ? styles.activeTab : ""}
                                                onClick={() => setActiveTab("first")}
                                              >
                                                Плеер 1
                                              </button>
                                              <button
                                                className={activeTab === "second" ? styles.activeTab : ""}
                                                onClick={() => setActiveTab("second")}
                                              >
                                                Плеер 2
                                              </button>
                                            </div>

                                            {/* Контент табов */}
                                            <div className={styles.tabContent}>
                                              {activeTab === "first" && (
                                                <div className={styles.player_player}>
                                                  <iframe
                                                    className={styles.player_block_iframe}
                                                    src={card.link}
                                                    width="100%"
                                                    height="100%"
                                                    frameBorder="0"
                                                    allowFullScreen
                                                    allow="autoplay *; fullscreen *"
                                                  ></iframe>
                                                </div>
                                              )}

                                              {activeTab === "second" && (
                                                <div className={styles.player_player}>
                                                  {/* <iframe
                                                    className={styles.player_block_iframe}
                                                    src={card.iframe}
                                                    width="100%"
                                                    height="100%"
                                                    frameBorder="0"
                                                    allowFullScreen
                                                    allow="autoplay *; fullscreen *"
                                                  ></iframe> */}

                                                  {cardAl?.iframe ? (
                                                        <iframe
                                                          className={styles.player_block_iframe}
                                                          src={cardAl.iframe}
                                                          width="100%"
                                                          height="100%"
                                                          frameBorder="0"
                                                          allowFullScreen
                                                          allow="autoplay *; fullscreen *"
                                                        ></iframe>
                                                      ) : (
                                                        <div className={styles.player_fallback}>
                                                          <h3>Плеер недоступен 😔</h3>
                                                          {/* Можно добавить картинку или ссылку на альтернативный источник */}
                                                          {/* <img
                                                            src="/anidag.png"
                                                            alt="Плеер недоступен"
                                                            style={{ maxWidth: "100%", height: "auto" }}
                                                          /> */}
                                                        </div>
                                                      )}
                                                </div>
                                              )}
                                            </div>
                                          </div>
                        
                                
                                  
                                    <div className={styles.interaction}>
                                                            <div className={styles.item}>
                                                                    <div 
                                                                  onClick={(e) => {
                                                                      handleLike(1);
                                                                      e.currentTarget.blur(); // убираем фокус после клика
                                                                    }}
                                                                    className={styles.like}></div>
                                                                    <span className={styles.number}>{likeCount === undefined  || likeCount === null ? 0 : likeCount}</span>
                                                                </div>
                                                                <div className={styles.item}>
                                                                    <div onClick={(e) => {
                                                                        handleDislike(1);
                                                                        e.currentTarget.blur();
                                                                      }}  className={styles.dislike}></div>
                                                                    <span className={styles.number}>{disLikeCount === undefined || disLikeCount === null ? 0 : disLikeCount}</span>
                                                                </div>
                                                                <div className={styles.item}>
                                                                    <div className={styles.views}></div>
                                                                    <span className={styles.number}>{viewCount === undefined || viewCount === null ? 0 : viewCount }</span>
                                                                </div>
                                                                 <div className={styles.bookMark} 
                                                                onClick={handleToggle} 
                                                                title={isAdded ? "Удалить из 'Смотреть позже'" : "Добавить в 'Смотреть позже'"}>
                                                                    <BookmarkIcon className={styles.bookMarkIcon}
                                                                    fill={ isAdded ? "#FF30AC" : "#000" } />
                                                                    {showToast && (
                                                                    <div className={styles.toast}>
                                                                         {toastMessage}
                                                                     </div>)}
                                                                </div>  
                                    </div> 
                                    <Comments card={card.id} />

                            </div>
                    
                            </div>   
                  
                    </div>
                        //   ) : (
                        //     <>
                        //     <h1>Тайтл не найден</h1>
                        //      <button>
                        //             Вернуться на главную
                        //           <Link href="/" className={styles.logo}/>
                        //     </button>
                        //     </>
                    
                        //   )
        ) : (
          <div className={styles.clipLoader}><ClipLoader color="#eb4d4b" size={50} /></div>
        )
  }


      </>
                            // card &&  card.names && card.names.ru ? (
                 
                        );


}

export default CardPages