import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './carousel.css'; // замените на путь к вашему CSS в React

const CarouselComponent = () => {
    const [currentIndex, setCurrentIndex] = useState(0);

    const items = [
        {
            id: 1,
            image: '/постер_фрирен_2.jfif',
            title: 'Фрирен',
            link: '/serial1',
        },
        {
            id: 2,
            image: '/Пожарная_Бригада.jfif',
            title: 'Пожарная бригада',
            link: '/serial2',
        },
        {
            id: 3,
            image: '/Магическая_битва.jfif',
            title: 'Магическая битва',
            link: '/serial3',
        },
        {
            id: 4,
            image: '/ataktitnov_slajd.webp',
            title: 'Атака Титанов',
            link: '/serial4',
        },
        {
            id: 5,
            image: '/naruto__slajd.webp',
            title: 'Наруто',
            link: '/serial5',
        },
        {
            id: 6,
            image: '/onepiece_slajd.webp',
            title: 'Ван Пис',
            link: '/serial6',
        },

    ];

    const nextSlide = () => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % items.length);
    };

    const prevSlide = () => {
        setCurrentIndex((prevIndex) => (prevIndex - 1 + items.length) % items.length);
    };

    const goToSlide = (index) => {
        setCurrentIndex(index);
    };

    useEffect(() => {
        const interval = setInterval(() => {
          setCurrentIndex(prev => (prev + 1) % items.length);
        }, 5000); // каждые 5 секунд
        return () => clearInterval(interval);
      }, [items.length]);

    return (
        <div className="carousel">
            <div className="slides" 
             style={{ transform: `translateX(-${currentIndex * 100}%)` }}
            >
                {items.map((item, index) => (
                    <div
                        key={item.id}
                        className={`slide ${index === currentIndex ? 'active' : ''}`}
                        // style={{ transform: `translateX(-${currentIndex * 100}%)` }}
                    >
                        <img
                            src={item.image}
                            alt={item.title}
                            loading="lazy"
                            className="image"
                        />
                        <div className="content">
                            <h2>{item.title}</h2>
                            <Link to={`/search/${item.title}`} className="button">Смотреть</Link>
                        </div>
                    </div>
                ))}
            </div>
            <button className="prev" onClick={prevSlide}>‹</button>
            <button className="next" onClick={nextSlide}>›</button>
            <div className="dots">
                {items.map((_, index) => (
                    <span
                        key={index}
                        className={`dot ${index === currentIndex ? 'active' : ''}`}
                        onClick={() => goToSlide(index)}
                    ></span>
                ))}
            </div>
        </div>
    );
};

export default CarouselComponent;
