import React from "react";
import styles from  "./WatchLater.module.css"
import $api from "../../api/auth";
import { Link } from 'react-router-dom';

const AnimeList = ({ animeList , onRemoved }) => {


    const handleRemove = async (anime_id) => {
        try {
          const res = await $api.delete(`/watch-later/remove/${anime_id}`);
          if (res.data.status === "removed") {
            onRemoved(anime_id); // <-- обновляет список
          }
        } catch (err) {
          console.error("Ошибка при удалении:", err);
        }
      };

    return (
      <div className={styles.container}>
        {animeList.map((item) => {
          const anime = item.data;
        //   console.log(anime.id, "ANIME")
           const makeSlug = (text = "") => {
                  return text
                    .toLowerCase()
                    .trim()
                    .replace(/[^\p{L}\p{N}\s-]/gu, "")
                    .replace(/\s+/g, "-")
                    .replace(/-+/g, "-");
                };

                const titleForSlug =
                  anime.title_orig ??
                  "anime";
                const seoPart = `${makeSlug(titleForSlug)}-${item.id}`;

  
          return (
            <div className={styles.card}>

        
            <Link to={`/anime/${anime.id}/${item.type}`} target="_blank">

                            <div key={item.id} className={styles.card_content}>
                            <img
                                src={anime.poster_url || "/placeholder.jpg"}
                                alt={anime.title}
                                className={styles.thumbnail}
                            />
                            <div className={styles.info}> 
                                <h3 className={styles.title}>{anime.title}</h3>
                                <p className={styles.rating}>
                                ⭐ {anime.material_data?.kinopoisk_rating ||  anime.material_data.shikimori_rating}
                                </p>

                            </div>
                            </div>


            </Link>

                            <button
                                            className={styles.deleteButton}
                                            onClick={() => handleRemove(anime.id)}
                                        >
                                            Удалить
                            </button>
            </div>
                        );
                        })}
        </div>
    );
  };

export default AnimeList;
