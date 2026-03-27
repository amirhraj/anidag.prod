import CarouselComponent from "../components/Carusel/Carusel";
import Navbar from "../components/Navbar/Navbar_genre";
import Ongoing from "../components/Ongoing/Ongoing"
import CatalogSection from "../components/CatalogSection/CatalogSection"
import SearchHighlights from "../components/SearchHighlights/SearchHighlights";
import styles from './home.module.css';
import { useEffect } from "react";


const Home = () => {

  useEffect(() => {
  document.title = "Смотреть аниме онлайн бесплатно вместе!";

  const setMeta = (name, content, isProperty = false) => {
    const selector = isProperty
      ? `meta[property="${name}"]`
      : `meta[name="${name}"]`;

    let meta = document.querySelector(selector);
    if (!meta) {
      meta = document.createElement("meta");
      isProperty
        ? meta.setAttribute("property", name)
        : meta.setAttribute("name", name);
      document.head.appendChild(meta);
    }
    meta.setAttribute("content", content);
  };

  setMeta(
    "description",
    "Смотрите лучшие аниме онлайн бесплатно в HD качестве. Огромная библиотека с субтитрами и озвучкой, удобный поиск по жанрам и популярные новинки. Наслаждайтесь любимыми сериалами без регистрации!"
  );

  setMeta("og:title", "Anidag - Смотри аниме онлайн", true);
}, []);


  return (
      <div className={styles.body}>
              <header className={styles.seoHeader}>
                    {/* <h1>Anidag — Анидаг</h1> */}
                      <title>Anidag (Анидаг) — смотреть аниме онлайн бесплатно</title>
                <meta name="description" content="Смотрите лучшие аниме онлайн бесплатно в HD качестве. Огромная библиотека с субтитрами и озвучкой, удобный поиск по жанрам и популярные новинки. Наслаждайтесь любимыми сериалами без регистрации!" />
                <meta property="og:title" content="Anidag (Анидаг)- Смотри аниме онлайн" />
              </header>
            <CarouselComponent />
            <SearchHighlights />
            <Navbar />
            <Ongoing />
            <CatalogSection />

    </div>
  );
};

export default Home;
