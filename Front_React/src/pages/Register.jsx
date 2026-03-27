import styleRegistre from './Register.module.css'
import { useState, useEffect } from "react";
import {  useNavigate} from 'react-router-dom';
import $api from "../api/auth";



export default function Register() {
 const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);

  const handleSubmit = async (event) => {

    
    event.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setIsSubmitting(true); // Блокируем кнопку


    try {
      const response = await $api.post('/register', {
        username,
        email,
        password,
      });
      // Предположим, что сервер возвращает 200 OK при успешной регистрации
      // console.log(response, "ReSPONSE")
      const accessToken = response.data.access_token;
      localStorage.setItem('access_token', accessToken);

      if (typeof window !== 'undefined') {
       
        localStorage.setItem('access_token', accessToken);
        // setAccessToken(token);
      }
      // console.log(response.data.registration        , "Ответ после регитсрации")
      if (response.status === 200) {
    
        setError(response.data.message)
        setTimeout(() => navigate("/"), 4000);
      }

   
    } catch (error) {
     
        const detail = error?.response?.data?.detail;

        if (Array.isArray(detail) && detail.length > 0) {
          // пример: "Пароль должен содержать минимум 8 символов."
          setError(detail[0].msg);
        } else {
          // запасной вариант
          setError('Произошла ошибка при регистрации');
        }
      
      
    //  console.log(error.response?.data?.detail)

  

      

    } finally {
    setIsSubmitting(false); // Разблокируем кнопку в случае ошибки
  }
  };


  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth <= 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  return (
  <div>
    <div className={styleRegistre.middle_content}>
            <form className={styleRegistre.form} onSubmit={handleSubmit}>
            <h1>Регистрация нового пользователя</h1>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <div className={styleRegistre.conteiner_input_login}>
                <label className={styleRegistre.label}>Логин:</label>
                <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className={styleRegistre.input}
                />
            </div>
            <div className={styleRegistre.conteiner_input_email}>
                <label className={styleRegistre.label}>Email:</label>

                <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className={styleRegistre.input}
                />
            </div>
            <div className={styleRegistre.conteiner_input_password}>
                <label className={styleRegistre.label}>Пароль:</label>
                {/* <div className={styleRegistre.important}>
                <span className={styleRegistre.stars}>&#42;</span> (Пароль должен содержать минимум <b>8</b> символов, <b>одну цифру</b>, <b>одну заглавную букву</b> и <b>один специальный символ</b>)
                 </div>  */}
                <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className={styleRegistre.input}
                onFocus={() => isMobile && setShowTooltip(true)}
                onBlur={() => isMobile && setShowTooltip(false)}
                />
                    <div className={`${styleRegistre.tooltip} ${isMobile && !showTooltip ? styleRegistre.hidden : ""}`}>
                           <span className={styleRegistre.stars}>&#42;</span> Пароль должен содержать минимум <b>8</b> символов, <b>одну цифру</b>, <b>одну заглавную букву</b> и <b>один специальный символ</b>.
                    </div>
            </div>
            <div className={styleRegistre.conteiner_input_password}>
                <label className={styleRegistre.label}>Повтор пароля:</label>
                <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className={styleRegistre.input}
                />
            </div>
            <button className={styleRegistre.button} type="submit" disabled={isSubmitting}>{isSubmitting ? "Отправка..." : "Отправить"}</button>
            </form>

    </div>
 
   
  

 </div>
  );
}
