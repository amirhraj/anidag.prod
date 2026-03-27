import { useState, useEffect } from 'react';
import $api from '../../api/auth';
import cssong from './Ongoing.module.css';
import { Link } from 'react-router-dom';
import { ClipLoader } from 'react-spinners';
import ErrorBoundaryImage from '../ErrorBoundaryImage /ErrorBoundaryImage';

function OngoingSection() {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [visibleCount, setVisibleCount] = useState(10);
  const [skip, setSkip] = useState(0);
  const limit = 16;

  useEffect(() => {
    fetchData(); // первичный запрос
  
    const interval = setInterval(() => {
      fetchData(); // автообновление
    }, 30 * 60 * 1000); // 30 минут в миллисекундах
  
    return () => clearInterval(interval); // очистка при размонтировании
  }, []);

  async function fetchData() {
    try {
      setLoading(true);
      const response = await $api   .get(`/animes?skip=${skip}&limit=${limit}`);
      const combinedSeries = [...series, ...response.data];
      const uniqueSeries = combinedSeries.filter((anime, index, self) =>
        index === self.findIndex((a) => a.title === anime.title && a.updated_at.split('T')[0] === anime.updated_at.split('T')[0])
      );
      setSeries(uniqueSeries);
      setSkip((prev) => prev + limit);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={cssong.ongoing_content}>
      <div className={cssong.title}>
        <h1 className={cssong.title_text}>Онгоинги</h1>
      </div>
      <div className={cssong.ongoing_wrepper}>
        {series.map((item, index) => {
          let url = '/anidag_default.png';
          // if (url === 'https://shikimori.one/assets/globals/missing_original.jpg' && item.worldart_link) {
          //   const params = item.worldart_link.split('?id=')[1];
          //   url = `http://www.world-art.ru/animation/img/13000/${params}/1.jpg`;
          // }

          return (
            <div className={cssong.card_ongoing} key={index}>
              <Link className={cssong.link} to={`/card/${item.id}/cardOngoing`} target="_blank">
                {/* <img
                  src={item.poster_url || url}
                  alt={item.material_data.anime_title}
                  width={70}
                  height={90}
                  loading="lazy"
                  className={cssong.card_ongoing_img}
                /> */}
                <div className={cssong.card_ongoing_container_img}>
                   <ErrorBoundaryImage  className={cssong.card_ongoing_img} src={item.poster_url} defaultSrc={'/anidag_default.png'} alt={item.material_data.anime_title}/>
                </div>

                <h3 className={cssong.card_ongoing_name}>{item.title}</h3>
                <div className={cssong.date_update}>{item.updated_at.split('T')[0]}</div>
                <div className={cssong.raiting}>{item.material_data.shikimori_rating}</div>
                <div className={cssong.card_ongoing_title}>
                  <h3 className={cssong.card_ongoing_episode}>{item.episodes_count}</h3>
                  <p className={cssong.card_ongoing_episode_name}>Серия</p>
                </div>
              </Link>
            </div>
          );
        })}
      </div>

      <div className={cssong.spiner}>{loading && <ClipLoader color="#eb4d4b" size={50} />}</div>
      {error && <p>Ошибка загрузки данных: {error.message}</p>}
      <div className={cssong.button_wrap}>
        <button onClick={fetchData} className={cssong.loadMoreButton}>
          Показать больше
        </button>
      </div>
    </div>
  );
}

export default OngoingSection;
