import { useEffect, useState } from 'react';
import styles from "./toggle.module.css"
import { MoonIcon } from '../components/Icons/MoonIcon.jsx'
import {  SunIcon } from '../components/Icons/SunIcon.jsx'

export default function ThemeToggle() {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');

  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <button className={styles.toggle_btn} onClick={toggleTheme}>
           {theme === "light" ? <MoonIcon className={styles.MoonIcon} /> : <SunIcon className={styles.SunIcon} />}
    </button>
  );
}
