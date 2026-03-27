// src/components/Card.jsx
// import styles from '../styles/Card.module.css';
import styles from '../CatalogSection/CatalogSection.module.css'
// import styles from '../CardContent/cardcontent.module.css'
import React, { useState } from 'react';
import ErrorBoundaryImage from '../ErrorBoundaryImage /ErrorBoundaryImage';

const Card = ({ href, title, image, rating, episode, description, minimal_age, rating_mpaa }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const MAX_DESCRIPTION_LENGTH = 100;

  const handleToggle = () => {
    setIsExpanded(!isExpanded);
  };

  const truncatedDescription = description.length > MAX_DESCRIPTION_LENGTH && !isExpanded
    ? `${description.substring(0, MAX_DESCRIPTION_LENGTH)}...`
    : description;

  const removeCharacterTags = (text) => {
    return text.replace(/\[(anime|character|person)=\d+\]/g, '').replace(/\[\/?(anime|character|person)\]/g, '');
  };

  const cleanedText = removeCharacterTags(truncatedDescription);

  return (
    <div className={styles.cardWrapper}>
      <a href={href} target="_blank" >
        <div className={styles.card}>
          <img
            src={image}
            alt={title}
            className={styles.image}
            loading="lazy"
            onError={(e) => { e.target.src = "/anidag_default.png"; }}
          />
            {/* <ErrorBoundaryImage  className={styles.image} src={image} defaultSrc={'/anidag_default.png'} alt={title}/> */}
          <div className={styles.overlay}>
            <div className={styles.rating}>{rating}</div>
            <div className={styles.episode}>Серия {episode}</div>
          </div>
        </div>
      </a>
      <div className={styles.description}>
        <div className={styles.title}><p className={styles.p}>{title}</p></div>
        {cleanedText}
        {description.length > MAX_DESCRIPTION_LENGTH && (
          <button onClick={handleToggle} className={styles.toggleButton}>
            {isExpanded ? 'Скрыть' : 'Читать больше'}
          </button>
        )}
      </div>
    </div>
  );
};

export default Card;
