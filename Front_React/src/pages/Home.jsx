import CarouselComponent from "../components/Carusel/Carusel";
import Navbar from "../components/Navbar/Navbar_genre";
import Ongoing from "../components/Ongoing/Ongoing"
import CatalogSection from "../components/CatalogSection/CatalogSection"
import SearchHighlights from "../components/SearchHighlights/SearchHighlights";
import styles from './home.module.css';
import { Helmet } from "react-helmet-async";



const Home = () => {




  return (
      <div className={styles.body}>
     <Helmet>
        <title>Anidag (Анидаг) — смотреть аниме онлайн бесплатно</title>
        <meta
          name="description"
          content="Anidag (Анидаг) — сайт для просмотра аниме онлайн бесплатно в HD качестве. Большая библиотека, озвучка и субтитры."
        />
      </Helmet>

            <CarouselComponent />
            <SearchHighlights />
            <Navbar />
            <Ongoing />
            <CatalogSection />

    </div>
  );
};

export default Home;
