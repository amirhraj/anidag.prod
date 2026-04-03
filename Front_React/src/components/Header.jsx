
import stylesHeader from "./Header.module.css";
import Navbar from './Navbar.jsx'
import Modal from "./Modal.jsx";
import  ThemeToggle from "../pages/ThemeToggle.jsx"
import { useState, useEffect } from "react";
import $api from "../api/auth.js";
import CookieConsert from './CookieConsert.jsx'
// import jwtDecode from "jwt-decode";
// import jwt_decode from "jwt-decode"; // Используйте это
import { jwtDecode } from 'jwt-decode';
import { Link, useNavigate , useLocation} from 'react-router-dom';
import { useUser } from './UserContext.jsx';




export default function Headers() {
  // const accessToken = localStorage.getItem('access_token');
  // console.log(accessToken, "TOKEn")
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState('');
  const [nav, setNav] = useState(false)
  const [activeModal, setActiveModal] = useState(false)
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [chekLogin, setChekLogin] = useState('')
  const [accessToken, setAccessToken] = useState(null);
  const [loginSuccess, setLoginSuccess] = useState(false);
  const [userData, setUserData] = useState('');
  const [userId, setUserId] = useState("");
  // const [isLoading, setIsLoading] = useState(true); 
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [user, setUser] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [showModalCastomization, setShowModalCastomization] = useState(false);
  const [backgrounds, setBackgrounds] = useState([]);
  const { setUserData: setUserDataContext } = useUser();

  const [backgroundTarget, setBackgroundTarget] = useState("profile");

  // useEffect(() => {

  //     const token = localStorage.getItem('access_token');
  //     const user = token ? jwtDecode(token) : '';
  //     setUser(user.login)

      
  //     setAccessToken(token);
  //     // setIsLoading(false);

  // }, []);





  useEffect(() => {
    const syncAuthState = () => {
      const token = localStorage.getItem("access_token");
      const decoded = token ? jwtDecode(token) : null;
   
  
      setAccessToken(token);
      setUser(decoded?.login || "");
      setUserId(decoded?.sub || "");
    };
  
    syncAuthState(); // начальная проверка
  
    const handleStorage = (e) => {
      if (e.key === "access_token") {
        syncAuthState(); // обновить токен при любом изменении
      }
    };
  
    window.addEventListener("storage", handleStorage);
  
    return () => {
      window.removeEventListener("storage", handleStorage);
    };
  }, []);
  

   useEffect(() => {
    if (!userId) return; 
    const checkToken = async () => {
        const userResponse = await $api.get(`/user/${userId}`); 
        setUserData(userResponse.data);
    };

    checkToken();
  }, [userId]);
  
  
  useEffect(() => {
    setActiveModal(false); // закрыть модалку при любом переходе
  }, [location.pathname]);


  const handleSubmitModal =  async (event) => {
    event.preventDefault();   
    setIsSubmitting(true);
    try{
      const response = await $api.post('/login', {
        email,
        password
      },{
        headers: {
          'Content-Type': 'application/json'
        }
      } 
      );
      const accessToken = response.data.access_token;
     
      setUserData(response.data)

      localStorage.setItem('access_token', accessToken);
      // console.log("Access token saved:", localStorage.getItem("access_token"));
      const token = localStorage.getItem('access_token');
      const user = token ? jwtDecode(token) : '';
      // document.cookie = `refresh_token=${refreshToken}; path=/; httponly`;
      setAccessToken(accessToken); 

       if (response.status === 200) {
          // setLoginSuccess(true)
         

          setAccessToken(accessToken); 
          setUser(user.login);
          navigate(`/profile/${user.login}`);
   
        // router.push('/profile');
      }
    }catch(error){
          const detail = error?.response?.data?.detail;
    
          let message = 'Произошла ошибка';
        
          if (typeof detail === 'string') {
            message = detail; // обычная строка
          } else if (Array.isArray(detail) && detail[0]?.msg) {
            message = detail[0].msg; // список ошибок от валидации Pydantic
          } else if (typeof detail === 'object' && detail?.msg) {
            message = detail.msg; // иногда приходит как объект с msg
          }
        
          setError(message);

    }finally {
      setIsSubmitting(false); // 🔹 Разблокируем кнопку после завершения запроса
    }



  };



  const handleInputChange = (event) => {

      setSearchQuery(event.target.value)

  };


  const handleSubmit = (e) => {
    e.preventDefault(); // чтобы не перезагружалась страница
    if (searchQuery.trim()) {
      navigate(`/search/${searchQuery}`);
    }
  };




  const handleLogout = async () => {
    try {
      const accessToken = localStorage.getItem('access_token');
  
      const response = await $api.get('/logout', {
        headers: {
          Authorization: `Bearer ${accessToken}`
        },
        withCredentials: true
      });
  
   
  
      if (response.status === 200) {
        localStorage.removeItem('access_token');
        setAccessToken(false);
        navigate('/');
      }
    } catch (error) {
      console.error("Ошибка при логауте:", error);
    }
  };
  

    useEffect(() => {
    if (showModalCastomization) {
      $api.get('/backgrounds').then(res => {
        setBackgrounds(res.data);
      });
    }
  }, [showModalCastomization]);


//   const chooseBackground = async (backgroundId) => {
//   const token = localStorage.getItem('access_token');
//   try {
//     const res = await $api.post('/backgrounds/set', null, {
//       params: { background_id: backgroundId },
//       headers: {
//         Authorization: `Bearer ${token}`
//       }
//     });

//     // 🟢 После успешного выбора — обновляем контекст
//     const updatedBackground = res.data?.background;
//     if (updatedBackground) {
//       setUserDataContext(prev => ({
//         ...prev,
//         background: {
//           ...prev?.background,
//           bk_image: updatedBackground.image_url
//         }
//       }));
//     }

//   } catch (error) {
//     console.error('Ошибка при выборе фона:', error);
//   }
// };


const chooseBackground = async (backgroundId) => {
  const token = localStorage.getItem('access_token');
  try {
    const res = await $api.post('/backgrounds/set', null, {
      params: { background_id: backgroundId },
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    // 🟢 После успешного выбора — обновляем контекст
    const updatedBackground = res.data?.background;
    if (updatedBackground) {
      setUserDataContext(prev => ({
        ...prev,
        background: {
          ...prev?.background,
          bk_image: updatedBackground.image_url
        }
      }));
    }

  } catch (error) {
    console.error('Ошибка при выборе фона:', error);
  }
};




const chooseProfileBackground = async (backgroundId) => {
  const token = localStorage.getItem("access_token");

  try {
    const res = await $api.post("/backgrounds/set", null, {
      params: { background_id: backgroundId },
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const updatedBackground = res.data?.background;

    if (updatedBackground) {
      setUserDataContext((prev) => ({
        ...prev,
        background_id: updatedBackground.id,
        background: {
          ...prev?.background,
          bk_image: updatedBackground.image_url,
          image_url: updatedBackground.image_url,
          name: updatedBackground.name,
          id: updatedBackground.id,
        },
      }));
    }
  } catch (error) {
    console.error("Ошибка при выборе фона профиля:", error);
  }
};

const chooseGlobalBackground = async (backgroundId) => {
  const token = localStorage.getItem("access_token");

  try {
    const res = await $api.post("/global-backgrounds/set", null, {
      params: { background_id: backgroundId },
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const updatedBackground = res.data?.background;

    if (updatedBackground) {
      setUserDataContext((prev) => ({
        ...prev,
        gl_background_id: updatedBackground.id,
        global_background: {
          ...prev?.global_background,
          bk_image: updatedBackground.image_url,
          image_url: updatedBackground.image_url,
          name: updatedBackground.name,
          id: updatedBackground.id,
        },
      }));
    }
  } catch (error) {
    console.error("Ошибка при выборе глобального фона:", error);
  }
};

const handleChooseBackground = async (backgroundId) => {
  if (backgroundTarget === "profile") {
    await chooseProfileBackground(backgroundId);
  } else {
    await chooseGlobalBackground(backgroundId);
  }
};




  return (
   



                    <header className={stylesHeader.header}>
                              <div className={stylesHeader.header_main}>
                                  <Link to="/" className={stylesHeader.logo}>
                                    <div className={stylesHeader.img_logo}> </div>
                                    
                                     {/* <img className={stylesHeader.img_logo} src="/anidag.svg" alt="Логотип" /> */}
                                  </Link>
                                  <div className= {stylesHeader.header_search}>
                                        {/* <form  onSubmit={handleSubmit} action="">
                                          <input type="hidden" name="do" value="search"/>
                                          <input type="hidden" name="subaction" value="search"/>
                                          <input onChange={handleInputChange} className={stylesHeader.search_block__input} id="story" name="story" placeholder="Поиск на сайте..." type="text" autoComplete="off"/>
                                          <Link to={searchQuery ? `/anime/${searchQuery}/cardSearch` : '#'} className={stylesHeader.logo}>
                                               <button className={stylesHeader.search_block__btn}   aria-label="Искать" type="submit"></button>
                                          </Link>
                                        </form> */}
                                         <form onSubmit={handleSubmit}>
                                            <input
                                              type="text"
                                              name="story"
                                              id="story"
                                              value={searchQuery}
                                              onChange={handleInputChange}
                                              placeholder="Поиск на сайте..."
                                              autoComplete="off"
                                              className={stylesHeader.search_block__input}
                                            />
                                            <button
                                              className={stylesHeader.search_block__btn}
                                              aria-label="Искать"
                                              type="submit"
                                            ></button>
                                          </form>
                                        {accessToken ? 
                                        (<div className={stylesHeader.entity_div_link}></div>)
                                        :
                                        (<Link to="/register" rel="nofollow" className={`${stylesHeader.header__link } ${stylesHeader.btn}`} >Зарегистрироваться</Link>)}
                                         <ThemeToggle />
                                         {/* <Link to="/register" rel="nofollow" className={`${stylesHeader.jutsu_header__link } ${stylesHeader.btn}`} >Зарегистрироваться</Link> */}
                                        {accessToken ? (
                                        
                                          <div  className={stylesHeader.img_profile_container}>
                                                <img 
                                                className={stylesHeader.img_profile} 
                                                src={
                                                                userData?.avatar_url
                                                                  ? `https://anidag.ru/api/${userData.avatar_url.replace(/\\/g, "/")}`
                                                                  : "/profile.png"
                                                              }
                                                alt="Профиль" 
                                                onClick={() => setShowModal(true)} 
                                                />

                                              {showModal && (
                                              <div className={stylesHeader.modalOverlay} onClick={() => setShowModal(false)}>
                                                <div className={stylesHeader.modalWindow} onClick={(e) => e.stopPropagation()}>
                                                  <Link className={stylesHeader.profileLink} to={`/profile/${user}`}><p>Профиль</p></Link>
                                                  <p className={stylesHeader.customButton} onClick={() => setShowModalCastomization(true)}>Кастомизация</p>
                                                  <button className={stylesHeader.modalClose} onClick={() => setShowModal(false)}>
                                                    Закрыть
                                                  </button>

                                                </div>
                                              </div>
                                            )}

                                         <Modal activeModal={showModalCastomization} setActiveModal={setShowModalCastomization}>
                                                {/* <div className={stylesHeader.backgroundScrollContainer}>
                                                  {backgrounds.map((bg) => (
                                                    <div 
                                                    key={bg.id} className={stylesHeader.backgroundCard} 
                                                    onClick={() => chooseBackground(bg.id)}>
                                                      <img
                                                        src={`https://anidag.ru/api${bg.image_url.replace(/\\/g, "/")}`}
                                                        alt={bg.name}
                                                        width="200"
                                                      />
                                                      <p>{bg.name}</p>
                                                    </div>
                                                  ))}
                                                </div> */}
                                           <div className={stylesHeader.backgroundModeBlock}>
                                                <label className={stylesHeader.modeLabel}>
                                                  <input
                                                    type="radio"
                                                    name="backgroundTarget"
                                                    value="profile"
                                                    checked={backgroundTarget === "profile"}
                                                    onChange={(e) => setBackgroundTarget(e.target.value)}
                                                  />
                                                  Для профиля
                                                </label>

                                                <label className={stylesHeader.modeLabel}>
                                                  <input
                                                    type="radio"
                                                    name="backgroundTarget"
                                                    value="global"
                                                    checked={backgroundTarget === "global"}
                                                    onChange={(e) => setBackgroundTarget(e.target.value)}
                                                  />
                                                  Глобальный фон
                                                </label>
                                              </div>

                                              <div className={stylesHeader.backgroundScrollContainer}>
                                                {backgrounds.map((bg) => (
                                                  <div
                                                    key={bg.id}
                                                    className={stylesHeader.backgroundCard}
                                                    onClick={() => handleChooseBackground(bg.id)}
                                                  >
                                                    <img
                                                      src={`https://anidag.ru/api${bg.image_url.replace(/\\/g, "/")}`}
                                                      alt={bg.name}
                                                      width="200"
                                                    />
                                                    <p>{bg.name}</p>
                                                  </div>
                                                ))}
                                              </div>
                                          </Modal>
                                          </div>
                                      

                                        ):(<Link to='/'>
                                          </Link>)

                                        }
                                        {accessToken ? 
                                        ( <button className= {`${stylesHeader.header__btn_theme_toggle} ${stylesHeader.icon} ${stylesHeader.icon_moon}` } onClick={handleLogout } aria-label="Выйти с сайт">Выйти</button>

                                        ) 
                                        : 
                                        ( <button className= {`${stylesHeader.header__btn_theme_toggle} ${stylesHeader.icon} ${stylesHeader.icon_moon}` } onClick={() => setActiveModal(true)} aria-label="Войти на сайт">Войти</button>)

                                        }
                                      
                                        <Modal  activeModal={activeModal} setActiveModal={ setActiveModal}>
                                        
                                            <div className={stylesHeader.modal_content_header}>
                                                <Link className={stylesHeader.link_modal} to="/register">
                                                      Зарегистрироваться
                                                </Link>
                                                <h2 className={stylesHeader.open_login}>Войти</h2>
                                                <button className={stylesHeader.btn_close} type="button" onClick={() => setActiveModal(false)}></button>
                                            </div>
                                                <div className={stylesHeader.modal_content}>
                                                 
                                                  <form className={stylesHeader.modal_content_form} onSubmit={handleSubmitModal}>
                                                    <div className={stylesHeader.conteiner_input_email}>
                                                      <label>E-mail:</label>
                                                      <input
                                                        type="text"
                                                        value={email}
                                                        onChange={(e) => setEmail(e.target.value)}
                                                        required
                                                        placeholder="Ваш e-mail"
                                                        className={stylesHeader.input}
                                                      />
                                                    </div>
                                                    <div className={stylesHeader.conteiner_input_password}>
                                                      <label>Пароль:</label>
                                                      <input
                                                        type="password"
                                                        value={password}
                                                        onChange={(e) => setPassword(e.target.value)}
                                                        required
                                                        placeholder="Ваш пароль"
                                                        className={stylesHeader.input}
                                                      />
                                                    </div>

                                                    {/* <button className={stylesHeader.btn_login} type="submit">Вход</button> */}
                                                    <button className={stylesHeader.btn_login} type="submit" disabled={isSubmitting}>{isSubmitting ? "Отправка..." : "Отправить"}</button>
                                                    
                                                  </form>
                                                  {error && <p className={stylesHeader.ErrorP}>{error}</p>}
                                                </div>
                                        </Modal>
                                        {/* Эта кнопка мун пока не нужна */}
                                        {/* <button className= {`${stylesHeader.jutsu_header__btn_theme_toggle_moon} ${stylesHeader.icon} ${stylesHeader.icon_moon}`} title="Сменить цвет сайта" aria-label="Сменить цвет сайта">
                                          <img className={stylesHeader.jutsu_header__btn_theme_toggle_moon_img} src='/moon.png' alt="" />
                                        </button> */}
                                        <div onClick={() => setNav(!nav)} className={stylesHeader.mobuli_button}>
                                          { nav ?   <img className={stylesHeader.mobuli_button_img} src={'/calce.png'} alt=""/>:
                                            <img className={stylesHeader.mobuli_button_img} src={'/burger_menu.png'} alt="" /> } 
                                         
                                        </div>
                                        <CookieConsert/>
                                  </div>
                              </div>
                                <Navbar  nav={nav}/>
                      </header>

  );
}



