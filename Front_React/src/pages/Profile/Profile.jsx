import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
// import Footer from "../../components/Footer";
import Modal from "../../components/Modal";
import stylesProfile from "./profile.module.css"; // убедись в правильном пути
import $api from "../../api/auth";
import { ClipLoader } from 'react-spinners';
import WatchLater from '../../components/WatchLater/WatchLater.jsx'
import { Link } from 'react-router-dom';
import { useUser } from "../../components/UserContext.jsx";



const animateNumber = (target, duration, setter) => {
  const startTime = performance.now();
  const frameRate = 60; // кадров в секунду
  const totalFrames = Math.round((duration / 1000) * frameRate);
  let frame = 0;

  const step = () => {
    frame++;
    const progress = frame / totalFrames;
    const current = Math.round(target * progress);

    setter(current);

    if (frame < totalFrames) {
      requestAnimationFrame(step);
    } else {
      setter(target); // на всякий случай точно устанавливаем конечное значение
    }
  };

  requestAnimationFrame(step);
};


const Profile = () => {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [activeModal, setActiveModal] = useState(false);
  const fileInputRef = useRef();
  const [userId, setUserId] = useState("");
  const [userLogin, setUserLogin] = useState("");
  const [userData, setUserData] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [animatedViews, setAnimatedViews] = useState(0);
  const [animatedLikes, setAnimatedLikes] = useState(0);
  const [animatedDislikes, setAnimatedDislikes] = useState(0);
  const [watchLaterList, setWatchLaterList] = useState([]);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [page, setPage] = useState(0);
  const [total, setTotal] = useState(0);
  const limit = 6;
  const [user, setUser] = useState(null);
  const { userData: userDataContext } = useUser();




  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);


  const navigate = useNavigate();


  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setAccessToken(token);
  
    if (!token) {
      navigate("/");
      return;
    }
  
    try {
      const user = jwtDecode(token);
      setUserLogin(user.login);
      setUserId(user.sub);
    } catch (err) {
      console.error("Ошибка при декодировании токена:", err);
      localStorage.removeItem("access_token");
      navigate("/");
    }
  }, [navigate]);

  useEffect(() => {
    if (!userId) return; 
    // const token = localStorage.getItem("access_token");
    // setAccessToken(token)

    // if (!token) {
    //   navigate("/");
    //   return;
    // }

    // try {
    //   const user = jwtDecode(token);
    //   setUserLogin(user.login);
    //   setUserId(user.sub);
    // } catch (err) {
    //   console.error("Ошибка при декодировании токена:", err);
    //   navigate("/");
    // }

    const checkToken = async () => {
      try {
        const response = await $api.get("/check-token/"
          // withCredentials: true
        );

        const userResponse = await $api.get(`/user/${userId}`);
        
          
        const data = userResponse.data;  
        setUserData(userResponse.data);

        if (typeof data.views === "number") {
          animateNumber(data.views, 2500, setAnimatedViews);
        }
        if (typeof data.likes === "number") {
          animateNumber(data.likes, 1500, setAnimatedLikes);
        }
        if (typeof data.dislikes === "number") {
          animateNumber(data.dislikes, 1500, setAnimatedDislikes);
        }


        setMessage(`Ты авторизовался: ${response.data.status}`);
      } catch (error) {
        console.error("Ошибка при проверке токена:", error);
        localStorage.removeItem("access_token");
        navigate("/");
      } finally {
        setLoading(false);
      }
    };

    checkToken();
  }, [userId]);



  useEffect(() => {
    const fetchWatchLater = async () => {
      try {
        const response = await $api.get("/watch-later/");
        setWatchLaterList(response.data);
      } catch (err) {
        console.error("Ошибка при получении списка 'Смотреть позже':", err);
        setError(err);
      }
    };

    fetchWatchLater();
  }, []);



  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    // console.log("Файл выбран:", file); 
    if (!file) return;

    if (!userId) {
      alert("Пожалуйста, подождите, пока загрузится профиль.");
      return;
    }

    if (!["image/png", "image/jpeg"].includes(file.type)) {
      alert("Можно загружать только PNG или JPEG!");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert("Файл слишком большой! Максимум 5 MB.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);

    try {
      // console.log("Отправка файла", {
      //   fileName: file.name,
      //   userId,
      //   formDataContent: formData.get("file"),
      // });
      await $api.post("/upload-avatar", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const userResponse = await $api.get(`/user/${userId}`);
      setUserData(userResponse.data);
    
      // const normalizedPath = userResponse.data.avatar_url?.replace(/\\/g, "/");
      // console.log(normalizedPath, "Преобразованный путь");
      // setUserData(normalizedPath);
    } catch (error) {
      console.error("Ошибка при загрузке:", error);
    }
    event.target.value = null;
  };




  //   useEffect(() => {
  //   const token = localStorage.getItem("access_token");
  //   if (!token) return;

  //   const decoded = jwtDecode(token);
  //   const userId = decoded?.sub;

  //   const fetchHistory = async () => {
  //     try {
  //       const res = await $api.get(`/watch-history/${userId}`);
  //       setUser(res.data.user);
  //       setHistory(res.data.history);
       
  //     } catch (err) {
  //       console.error("Ошибка получения истории:", err);
  //     }
  //   };

  //   fetchHistory();
  // }, []);


    useEffect(() => {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  const decoded = jwtDecode(token);
  const userId = decoded?.sub;

  const fetchHistory = async () => {
    try {
      const res = await $api.get(`/watch-history/${userId}`, {
        params: { limit, offset: page * limit }
      });
      setHistory(res.data.history);
      setTotal(res.data.total);
      setUser(res.data.user);
    } catch (err) {
      console.error("Ошибка получения истории:", err);
    }
  };

  fetchHistory();
}, [page]);



  // Новый блок истории просмотров


  // useEffect(() => {
  //   fetchHistory(1);
  // }, []);

  // const fetchHistory = async (page) => {
  //   const token = localStorage.getItem("access_token");
  //   if (!token) return;

  //   const decoded = jwtDecode(token);
  //   const userId = decoded?.sub;

  //   try {
  //     setLoading(true);
  //     const res = await $api.get(`/watch-history/${userId}?page=${page}&limit=6`);
      
  //     if (page === 1) {
  //       setHistory(res.data.history);
  //     } else {
  //       setHistory(prev => [...prev, ...res.data.history]);
  //     }
      
  //     setUser(res.data.user);
  //     setTotalPages(res.data.pagination.total_pages);
  //     setCurrentPage(page);
  //   } catch (err) {
  //     console.error("Ошибка получения истории:", err);
  //   } finally {
  //     setLoading(false);
  //   }
  // };

  // const loadMore = () => {
  //   if (currentPage < totalPages && !loading) {
  //     fetchHistory(currentPage + 1);
  //   }
  // };

  // const loadPrev = () => {
  //   if (currentPage > 1 && !loading) {
  //     fetchHistory(currentPage - 1);
  //   }
  // };


  if (loading) return <div className={stylesProfile.clipLoader}><ClipLoader color="#eb4d4b"  size={50} /></div>;
  // if (loading) return <div >Загрузка....</div>;


  // const debugUpload = (
  //   <div style={{ padding: "2rem", border: "1px solid red", marginBottom: "2rem" }}>
  //     <h3>Тест загрузки файла</h3>
  //     <input
  //       type="file"
  //       onChange={(e) => {
  //         const file = e.target.files[0];
  //         console.log("Файл выбран:", file);
  //         if (file) alert(`Вы выбрали: ${file.name}`);
  //       }}
  //       accept="image/png, image/jpeg"
  //     />
  //   </div>
  // );
  
  return (
    <div className={stylesProfile.profile_container2}>
{/* {debugUpload} */}
      {/* <h1 className={stylesProfile.h1_text}>Здесь ведутся работы</h1> */}
      <div className={stylesProfile.profile_container}>
        <div className={stylesProfile.profile_content}>
                    <div className={stylesProfile.back_fon} >
          
            <img
            className={stylesProfile.img_back}
              src={
                userDataContext?.background?.bk_image
                  ? `https://anidag.ru/api${userDataContext.background.bk_image.replace(/\\/g, "/")}`
                   :  userData?.bk_image
                    ? `https://anidag.ru/api${userData.bk_image.replace(/\\/g, "/")}`
                    : "/anime-wallpaper-Anime-Wallpapers-evergarden-sky.png"
              }
            alt="banner"
          />
          </div>

          <div className={stylesProfile.contain_img}>
         

            <img
            src={
              userData?.avatar_url
                ? `https://anidag.ru/api/${userData.avatar_url.replace(/\\/g, "/")}`
                : "/profile.png"
            }
              alt="Фото профиля"
              className={stylesProfile.image}
              width={150}
              height={150}
              loading="lazy"
              onClick={() => setActiveModal(true)}
            />
          
          </div>

          <Modal activeModal={activeModal} setActiveModal={setActiveModal}>
            <div>
              <h1>Установка аватарки</h1>
              <ul>
                <li>Разрешены только .png и .jpg</li>
                <li>Без 18+, насилия и нарушений</li>
                <li>Размер до 5 MB</li>
              </ul>
              <p><strong>Нарушения — бан аккаунта</strong></p>
              <button className={stylesProfile.btn_upload} onClick={handleButtonClick}>Загрузить</button>
            </div>
          </Modal>

          <input
            type="file"
            ref={fileInputRef}
            style={{ display: "none" }}
            accept="image/png, image/jpeg"
            onChange={handleFileChange}
          />

         <div className={stylesProfile.profileHeader}>
              <div className={stylesProfile.contain_nickname}>
                <h3>{userData.name}</h3>

              </div>

              <div className={stylesProfile.statsContainer}>
                        <div className={stylesProfile.statItem}>  
                            <div className={stylesProfile.statValue}>{animatedLikes}</div>
                            <div className={stylesProfile.statLabel}>like</div>
                        </div>
                        <div className={stylesProfile.statItem}>
                          <div className={stylesProfile.statValue}>{animatedDislikes}</div>
                          <div className={stylesProfile.statLabel}>Dislike</div>
                        </div>
                        <div className={stylesProfile.statItem}>
                          <div className={stylesProfile.statValue}>{animatedViews.toLocaleString()}</div>
                          <div className={stylesProfile.statLabel}>Views</div>
                        </div>
               </div>
        </div>


 <div className={stylesProfile.scroll_container}>
  {history.length === 0 ? (
    <p style={{ paddingLeft: "1rem" }}>Нет просмотренных эпизодов</p>
  ) : (
    history.map((item) => (
      <Link 
        key={`${item.anime_id}-${item.episode}`} 
        to={`/anime/${item.anime_id}/${item.type}`}  
        className={stylesProfile.link}
        target="_blank"
      >
        <div className={stylesProfile.history_card}>
          <img src={item.poster_url || "/default-poster.jpg"} alt={item.title} />
          <div className={stylesProfile.progress_bar_wrapper}>
            <div
              className={stylesProfile.progress_bar}
              style={{ width: `${item.progress}%` }}
            />
          </div>
          <p>{item.title}</p>
          <p>Серия {item.episode}</p>
        </div>
      </Link>
    ))
  )}
</div>

<div className={stylesProfile.pagination}>
  <button 
    onClick={() => setPage((p) => Math.max(p - 1, 0))} 
    disabled={page === 0}
  >
    ← Назад
  </button>
  <span>Страница {page + 1} из {Math.ceil(total / limit)}</span>
  <button 
    onClick={() => setPage((p) => (p + 1 < Math.ceil(total / limit) ? p + 1 : p))} 
    disabled={page + 1 >= Math.ceil(total / limit)}
  >
    Вперёд →
  </button>
</div>



{/* <div>
      <div className={stylesProfile.healine_text}>
        <p>История просмотров</p>
      </div>

      <div className={stylesProfile.scroll_container}>
        {history.length === 0 ? (
          <p style={{ paddingLeft: "1rem" }}>Нет просмотренных эпизодов</p>
        ) : (
          <>
            {history.map((item) => (
              <Link 
                to={`/anime/${item.anime_id}/${item.type}`}  
                className={stylesProfile.link}
                key={`${item.anime_id}-${item.episode}-${item.updated_at}`}
              >
                <div className={stylesProfile.history_card}>
                  <img src={item.poster_url || "/default-poster.jpg"} alt={item.title} />
                  <div className={stylesProfile.progress_bar_wrapper}>
                    <div
                      className={stylesProfile.progress_bar}
                      style={{ width: `${item.progress}%` }}
                    />
                  </div>
                  <p>{item.title}</p>
                  <p>Серия {item.episode}</p>
                </div>
              </Link>
            ))}
          </>
        )}
      </div>

    
      {totalPages > 1 && (
        <div className={stylesProfile.pagination}>
          <button 
            onClick={loadPrev} 
            disabled={currentPage === 1 || loading}
            className={stylesProfile.paginationButton}
          >
            ← Назад
          </button>
          
          <span className={stylesProfile.pageInfo}>
            Страница {currentPage} из {totalPages}
          </span>
          
          <button 
            onClick={loadMore} 
            disabled={currentPage === totalPages || loading}
            className={stylesProfile.paginationButton}
          >
            Вперед →
          </button>
        </div>
      )}

      {loading && <p>Загрузка...</p>}
    </div> */}
        
          <div className={stylesProfile.bookmark}>
            <div className={stylesProfile.bookmark_headline}>
              <div className={stylesProfile.healine_text}>
                <p>Тайтлы в закладках</p>
              </div>
              <WatchLater  animeList={watchLaterList}   
                onRemoved={(removedAnimeId) =>
                  setWatchLaterList((prev) => {
                    const updated = prev.filter((item )=> {
                      return item.data.id !== removedAnimeId 
                    });
                    return updated;
                  })} />
            </div>
          </div>
        </div>
      </div>


    </div>
  );
};

export default Profile;
