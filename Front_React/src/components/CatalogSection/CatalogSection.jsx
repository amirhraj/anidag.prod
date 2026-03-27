// MainTitlesSection.jsx
import { useState, useEffect } from 'react';
import styles from './CatalogSection.module.css';
import Card from '../CardContent/CardContent';
import { ClipLoader } from 'react-spinners';
import $api from '../../api/auth';

export default function MainTitlesSection() {
  const [loadings, setLoading] = useState(false);
  const [errors, setErrors] = useState(null);
  const [getAnime, setGetAnime] = useState([]);
  const [skip, setSkip] = useState(0);
  const [limit] = useState(25);

  useEffect(() => {
    getAnimeTitleMine();
  }, []);

  async function getAnimeTitleMine() {
    try {
      setLoading(true);
      const response = await $api.get(`/animesMainTitles?skip=${skip}&limit=${limit}`);

      const combinedSeries = [...getAnime, ...response.data];
      const uniqueSeries = combinedSeries.filter((anime, index, self) =>
        index === self.findIndex(
          (a) => a.title === anime.title && a.updated_at.split('T')[0] === anime.updated_at.split('T')[0]
        )
      );

      setGetAnime(uniqueSeries);
      setSkip((prevSkip) => prevSkip + limit);
    } catch (err) {
      setErrors(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    
    <div className={styles.main_content}>
            <div className={styles.sect_title_sub}>
                    <h1 className={styles.sect_title_name}>Смотреть аниме</h1>
            </div>
      <div className={styles.cardContainer}>
        {getAnime.map((item) => {
          let url =
            item.material_data.anime_poster_url ===
            'https://shikimori.one/assets/globals/missing_original.jpg'
              ? item.worldart_link
              : item.material_data.anime_poster_url;

          if (url === item.worldart_link && url) {
            const params = url.split('?id=')[1];
            url = `http://www.world-art.ru/animation/img/13000/${params}/1.jpg`;
          }

          return (
            <Card
              key={item.id}
              href={`/card/${item.id}/card`}
              title={item.title}
              image={item.poster_url || "/anidag_default.png"
              }
              rating={item.material_data.kinopoisk_rating || item.material_data.shikimori_rating}
              episode={item.material_data.episodes_total}
              description={item.material_data.description || ' '}
              minimal_age={item.material_data.minimal_age}
              rating_mpaa={item.material_data.rating_mpaa}
            />
          );
        })}
      </div>

      <div className={styles.buttonContainer}>
        {loadings ? (
          <ClipLoader color="#eb4d4b" size={50} />
        ) : (
          <button onClick={getAnimeTitleMine} className={styles.loadMoreButton}>
            Показать больше
          </button>
        )}
      </div>

      {errors && <p className={styles.errorText}>Ошибка: {errors.message}</p>}
      <div className={styles.text_anime}>
                              <p><span className={styles.text_word}>Аниме</span> — это целая вселенная, где границы между реальностью и фантазией стираются, открывая тебе двери в удивительные миры. Это не просто мультфильмы, это искусство, способное вызвать бурю эмоций — от искреннего смеха до слёз, от напряжённого ожидания до глубоких размышлений.</p>
  
                              <p>Представь себе, что ты попадаешь в мир, где обычные школьники могут обладать невероятными способностями, где эпические сражения за судьбу мира разворачиваются на фоне философских размышлений о жизни и морали. Или, может быть, тебя больше заинтересуют нежные истории о дружбе и любви, которые рассказываются так искренне, что ты словно сам становишься частью этой истории.</p>
                              
                              <p>В аниме найдётся всё: загадочные детективы, магия и приключения, научная фантастика и постапокалиптические миры, и даже трогательные истории о повседневной жизни, которые заставляют увидеть красоту в простых моментах. Каждый найдёт что-то своё, что затронет душу.</p>
                              
                              <p>Это мир, где каждый кадр — произведение искусства, а музыка и озвучка настолько тонко передают настроение, что ты буквально ощущаешь себя героем этой истории. Аниме — это портал в мир безграничного воображения, который ждёт, чтобы ты открыл его для себя. Готов ли ты отправиться в это увлекательное путешествие?</p>
        </div>
    </div>
  );
}
