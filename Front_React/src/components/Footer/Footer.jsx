// src/components/Footer/Footer.jsx
import styles from '../../pages/home.module.css';
import { Link } from 'react-router-dom';
import TelegramIcons from '../Icons/TelegramIcon.jsx'
import { Mail } from '../Icons/Mail.jsx';
import {Boosty } from '../Icons/Boosty.jsx'
import {Youtube} from '../Icons/Youtube.jsx'

export default function Footer() {
  return (
    <div className={styles.footerWrapper}>
      <footer className={styles.footer}>
        <div className={styles.container}>
          <div className={styles.links_footer}>
            {/* <Link to="/privacy-policy" className={styles.link_footer}>Конфиденциальность</Link> */}
            <Link to="/Terms" className={styles.link_footer}>Соглашение</Link>
            <Link to="/RightsHoldersPolicy" className={styles.link_footer}>
              Для правообладателей
            </Link>
          </div>

          <div className={styles.connection}>
                <a href="https://t.me/anidagHD" target="_blank" rel="noopener noreferrer">
                      <TelegramIcons className={styles.icon_telegram}/>
                </a>
                <a href="mailto:anidaghd@gmail.com" target="_blank" rel="noopener noreferrer">
                      <Mail className={styles.icon_telegram}/>
                </a>
                <a href="https://boosty.to/anidag" target="_blank" rel="noopener noreferrer">
                      <Boosty className={styles.icon_telegram}/>
                </a>    
                <a href="https://www.youtube.com/channel/UC6NX6iw50Vu4tnUA_u7h_fw" target="_blank" rel="noopener noreferrer">
                      <Youtube className={styles.icon_telegram}/>
                </a>
          </div>
          <p className={styles.copy}>© anidag.ru 2024 - 2026</p>
        </div>
      </footer>
    </div>
  );
}
