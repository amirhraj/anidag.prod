// src/components/GenresNavbar.jsx
import { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './navbar_genre.module.css'; // Или './GenresNavbar.css' если не используешь CSS-модули

export default function GenresNavbar() {
  const [activeIndex, setActiveIndex] = useState(0);

  const genres = [
    { type: 'genre', label: 'Экшен', value: 'action' },
    { type: 'genre', label: 'Комедия', value: 'comedy' },
    { type: 'genre', label: 'Драма', value: 'drama' },
    { type: 'genre', label: 'Фэнтези', value: 'fantasy' },
    { type: 'genre', label: 'Ужасы', value: 'horror' },
    { type: 'genre', label: 'Романтика', value: 'romance' },
    { type: 'genre', label: 'Фантастика', value: 'sci-fi' },
    { type: 'genre', label: 'Мистика', value: 'mystery' },
  ];


  // const genres = [
  //   { type: 'action', label: 'Экшен' },
  //   { type: 'comedy', label: 'Комедия' },
  //   { type: 'drama', label: 'Драма' },
  //   { type: 'fantasy', label: 'Фэнтези' },
  //   { type: 'horror', label: 'Ужасы' },
  //   { type: 'romance', label: 'Романтика' },
  //   { type: 'sci-fi', label: 'Фантастика' },
  //   { type: 'mystery', label: 'Мистика' },
  // ];


  return (
    <nav className={styles.nav_gen}>
      <ul className={styles.nav_menu_gen}>
        {genres.map((genre, index) => (
          <li
            key={index}
            className={`${styles.li_gen} ${activeIndex === index ? styles.isActive : ''}`}
            onClick={() => setActiveIndex(index)}
          >
            <Link 
            className={styles.link_gen} 
            to={`/category/${genre.type}/${genre.label}`}>
              {genre.label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
