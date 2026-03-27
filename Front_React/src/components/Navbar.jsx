import stylesNavbar from "./navbar.module.css";
import { useState } from 'react';
import { useLocation, Link } from 'react-router-dom';



export default function Navbar({nav}) {


    const location = useLocation();
    const [activeIndex, setActiveIndex] = useState(0);
  
    // Список ссылок
    // const navItems = [
    //   { href: '/', label: 'Все аниме' },
    //   { href: '/movie', label: 'Фильмы' },
    //   { href: '/TV', label: 'TV сериалы' },
    //   { href: '/OVA', label: 'OVA' },
    //   { href: '/TOP', label: 'ТОП-100' },
    //   { href: '/Ongoing_pages', label: 'Онгоинги' },
    //   { href: '/Anons', label: 'Анонсы' },
    //   { href: '/schedule', label: 'Расписание' },
    // ];


    const navItems = [
      { href: '/', label: 'Все аниме' },
      { href: '/category/movie', label: 'Фильмы' },
      { href: '/category/tv', label: 'TV сериалы' },
      { href: '/category/ova', label: 'OVA' },
      { href: '/category/top', label: 'ТОП-100' },
      { href: '/category/ongoing', label: 'Онгоинги' },
      { href: '/category/anons', label: 'Анонсы' },
      { href: '/category/schedule', label: 'Расписание' },
      { href: '/category/news', label: 'Новости' },
    ];

    // useEffect(() => {
    //   const currentPath = router.pathname;
    //   const currentIndex = navItems.findIndex(item => item.href === currentPath);
    //   setActiveIndex(currentIndex);
    // }, [router.pathname]);

return(
                <nav className={`${stylesNavbar.nav} ${nav ? stylesNavbar.active : ''}` }>
                        <ul className={stylesNavbar.nav_menu}>
                                {navItems.map((item, index) => (
                                    <li
                                    key={index}
                                    className={`${stylesNavbar.li} ${location.pathname === item.href  ? stylesNavbar.isActive : ''}`}
                                    onClick={() => setActiveIndex(index)} // Обновляем активный индекс при клике
                                    >
                                    <Link className={stylesNavbar.link}  to={item.href}>
                                    {item.label}
                                    </Link>
                                    </li>
                                ))}
                        </ul>
                </nav>
)
}